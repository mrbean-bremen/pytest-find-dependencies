from multiprocessing import Process

import pytest

CACHE_KEY_IDS = "find_dependencies/node_ids"
CACHE_KEY_FAILED = "find_dependencies/failed_ids"


class DependencyFinder:
    """Tries to find dependencies between tests using reverse executing
    first and more test executions using binary search to get dependent
    tests."""

    def __init__(self, session):
        self.session = session
        self.dependent_items = {}
        self.permanently_failed_items = []
        self.test_runs = 0
        self.test_number = 0

    def find_dependencies(self):
        items = self.session.items
        ignored_markers = (self.session.config.getoption(
            "markers_to_ignore") or "").split(",")
        if ignored_markers:
            ignored_items = []
            for item in items:
                for ignored_marker in ignored_markers:
                    if item.get_closest_marker(ignored_marker):
                        ignored_items.append(item)
                        break
            for ignored_item in ignored_items:
                items.remove(ignored_item)

        reversed_first = self.session.config.getoption("reversed_first")
        reversed_items = items[::-1]
        if reversed_first:
            items1, items2 = reversed_items, items
        else:
            items1, items2 = items, reversed_items
        failed1 = self.run_tests(items1)
        failed2 = self.run_tests(items2)
        always_failing_items = failed1.intersection(failed2)

        # tests failing in both runs are not considered
        failed1, failed2 = failed1 - failed2, failed2 - failed1
        for item in sorted(failed1, key=str):
            self.check_failed_item(item, items1)

        # tests failing in the second run have to checked if they fail
        # permanently afterwards - in this case the we don't try to
        # find the dependency
        for item in sorted(failed2, key=str):
            self.check_failed_item(item, items2, check_permanent=True)
        print()
        print("=" * 30, "Results", "=" * 31)
        print(f"Run dependency analysis for {len(items1)} tests.")
        print(f"Executed {self.test_number} tests in "
              f"{self.test_runs} test runs.")
        if always_failing_items:
            print("The following tests are always failing and "
                  "are excluded from the analysis:")
            for item in sorted(always_failing_items):
                print(f"  {item.nodeid}")

        failed = self.dependent_items or self.permanently_failed_items
        if not failed:
            print("No dependent tests found.")
        else:
            if self.permanently_failed_items:
                print("Tests failing permanently after all tests have run:")
                for item in self.permanently_failed_items:
                    print(f"  {item.nodeid}")
            if self.dependent_items:
                print("Dependent tests:")
                for item, dependent in self.dependent_items.items():
                    print(f"  {item.nodeid} depends on {dependent.nodeid}")
        print(f"\nDependency test {'FAILED' if failed else 'PASSED'}")
        print("=" * 70)
        self.set_exitstatus()

    def set_exitstatus(self):
        """Set the exitstatus to failed if dependent tests where found."""
        self.session.testsfailed = (len(self.dependent_items) +
                                    len(self.permanently_failed_items))
        if self.session.testsfailed:
            try:
                # pytest >= 5
                from pytest import ExitCode
                tests_failed = ExitCode.TESTS_FAILED
            except ImportError:
                # pytest < 5
                from _pytest.main import EXIT_TESTSFAILED
                tests_failed = EXIT_TESTSFAILED
            self.session.exitstatus = tests_failed

    def check_failed_item(self, item, items, failed=True,
                          check_permanent=False):
        if check_permanent and item in self.run_tests([item]):
            self.permanently_failed_items.append(item)
            return
        index = items.index(item)
        if failed:
            if index == 1:
                self.dependent_items[item] = items[0]
                return
            mid_index = index // 2
            sub_items_to_run = items[:mid_index] + [items[index]]
            sub_items = sub_items_to_run + items[mid_index:index]
        else:
            if index == len(items) - 2:
                self.dependent_items[item] = items[index + 1]
                return
            mid_index = index + 1 + (len(items) - index - 1) // 2
            sub_items_to_run = items[index + 1:mid_index] + [items[index]]
            sub_items = sub_items_to_run + items[mid_index:]

        failed_items = self.run_tests(sub_items_to_run)
        self.check_failed_item(item, sub_items, item in failed_items)

    def run_tests(self, items):
        items = {item.nodeid: item for item in items}
        self.session.config.cache.set(CACHE_KEY_IDS, list(items.keys()))
        args = ["--find-dependencies-internal"]
        if hasattr(self.session.config, "initial_args"):
            args += self.session.config.initial_args
        print(f"Running pytest with arguments {' '.join(args)}")
        p = Process(target=pytest.main, args=[args])
        p.start()
        p.join()
        failed_node_ids = self.session.config.cache.get(CACHE_KEY_FAILED, [])
        self.test_runs += 1
        self.test_number += len(items)
        return set(items[key] for key in items if key in failed_node_ids)


def run_tests(session):
    all_items = {item.nodeid: item for item in session.items}
    node_ids = session.config.cache.get(CACHE_KEY_IDS, [])
    items = [all_items[node_id] for node_id in node_ids
             if node_id in all_items]
    failed_node_ids = []
    for index, item in enumerate(items):
        test_failed = session.testsfailed
        next_item = items[index + 1] if index + 1 < len(items) else None
        item.config.hook.pytest_runtest_protocol(item=item,
                                                 nextitem=next_item)
        if session.testsfailed > test_failed:
            failed_node_ids.append(item.nodeid)
    session.config.cache.set(CACHE_KEY_FAILED, failed_node_ids)
    # clear the items - otherwise the tests will be run again by
    # pytest's own pytest_runtestloop
    session.items.clear()
