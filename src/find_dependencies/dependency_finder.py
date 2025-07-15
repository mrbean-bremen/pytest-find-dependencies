from multiprocessing import Process

import pytest

CACHE_KEY_IDS = "find_dependencies/node_ids"
CACHE_KEY_FAILED = "find_dependencies/failed_ids"


class DependencyFinder:
    """Tries to find dependencies between tests using direct and reverse
    execution first, and more test executions using binary search as needed
    to detect dependent tests."""

    def __init__(self, session):
        self.session = session
        self.dependent_items = {}
        self.permanently_failed_items = []
        self.test_runs = 0
        self.test_number = 0

    def find_dependencies(self):
        items = self.session.items
        ignored_markers = (
            self.session.config.getoption("markers_to_ignore") or ""
        ).split(",")
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

        if self.session.config.getoption("run_serially"):
            failed1 = self.run_tests(items1)
            failed2 = self.run_tests(items2)
        else:
            failed1, failed2 = self.run_tests_in_parallel([items1, items2])
        always_failing_items = failed1.intersection(failed2)

        # tests failing in both runs are not considered
        failed1, failed2 = failed1 - failed2, failed2 - failed1
        self.check_failed_items(sorted(failed1, key=str), [items1] * len(failed1))

        # tests failing in the second run have to be checked if they fail
        # permanently afterward - in this case we don't try to
        # find the dependency
        self.check_failed_items(
            sorted(failed2, key=str), [items2] * len(failed2), check_permanent=True
        )
        print()
        print("=" * 30, "Results", "=" * 31)
        print(f"Run dependency analysis for {len(items1)} tests.")
        print(f"Executed {self.test_number} tests in {self.test_runs} test runs.")
        if always_failing_items:
            print(
                "The following tests are always failing and "
                "are excluded from the analysis:"
            )
            for item in sorted(always_failing_items, key=str):
                print(f"  {item.nodeid}")

        failed = self.dependent_items or self.permanently_failed_items
        if not failed:
            print("No dependent tests found.")
            if always_failing_items and self.session.config.getoption(
                "fail_on_failed_tests"
            ):
                print("Failed because of failing tests.")
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
        self.set_exitstatus(always_failing_items)

    def set_exitstatus(self, always_failing_items):
        """Set the exitstatus to failed if dependent tests where found."""
        self.session.testsfailed = len(self.dependent_items) + len(
            self.permanently_failed_items
        )

        if always_failing_items and self.session.config.getoption(
            "fail_on_failed_tests"
        ):
            self.session.testsfailed += len(always_failing_items)
        if self.session.testsfailed:
            tests_failed = pytest.ExitCode.TESTS_FAILED
            self.session.exitstatus = tests_failed

    def check_failed_items(
        self, failed_items, item_lists, failed=None, check_permanent=False
    ):
        if not failed_items:
            return
        if check_permanent:
            if self.session.config.getoption("run_serially"):
                failed_item_list = [self.run_tests([item]) for item in failed_items]
            else:
                failed_item_list = self.run_tests_in_parallel(
                    [item] for item in failed_items
                )

            for failed_item_set in failed_item_list:
                if failed_item_set:
                    failed_item = failed_item_set.pop()
                    self.permanently_failed_items.append(failed_item)
                    # if failed_item in failed_items:
                    failed_items.remove(failed_item)

        items_to_run = []
        all_items = []
        for item_index, (failed_item, items) in enumerate(
            zip(failed_items, item_lists)
        ):
            index = items.index(failed_item)
            last_failed = failed is None
            if not last_failed:
                last_failed = failed[item_index]
            if last_failed:
                if index == 1:
                    self.dependent_items[failed_item] = items[0]
                    # if failed_item in failed_items:
                    failed_items.remove(failed_item)
                    continue
                mid_index = index // 2
                sub_items_to_run = items[:mid_index] + [items[index]]
                sub_items = sub_items_to_run + items[mid_index:index]
            else:
                if index == len(items) - 2:
                    self.dependent_items[failed_item] = items[index + 1]
                    failed_items.remove(failed_item)
                    continue
                mid_index = index + 1 + (len(items) - index - 1) // 2
                sub_items_to_run = items[index + 1 : mid_index] + [items[index]]
                sub_items = sub_items_to_run + items[mid_index:]
            items_to_run.append(sub_items_to_run)
            all_items.append(sub_items)

        if self.session.config.getoption("run_serially"):
            failed_item_list = [self.run_tests(item) for item in items_to_run]
        else:
            failed_item_list = self.run_tests_in_parallel(items_to_run)
        item_failed = [
            item in failed_items
            for item, failed_items in zip(failed_items, failed_item_list)
        ]
        self.check_failed_items(failed_items, all_items, item_failed)

    def run_tests_in_parallel(self, item_lists):
        processes = []
        item_ids = []
        for index, items in enumerate(item_lists):
            item_ids.append({item.nodeid: item for item in items})
            self.session.config.cache.set(
                f"{CACHE_KEY_IDS}{index}", list(item_ids[index].keys())
            )
            args = [
                "--find-dependencies-internal",
                f"--find-dependencies-index={index}",
            ]
            if hasattr(self.session.config, "initial_args"):
                args += self.session.config.initial_args
            print(f"Running pytest with arguments {' '.join(args)}")
            p = Process(target=pytest.main, args=[args])
            processes.append(p)
            p.start()
            self.test_runs += 1
            self.test_number += len(items)

        failed_items = []
        for index, p in enumerate(processes):
            p.join()
            failed_node_ids = self.session.config.cache.get(
                f"{CACHE_KEY_FAILED}{index}", []
            )
            items = item_ids[index]
            failed_items.append({items[key] for key in items if key in failed_node_ids})
        return failed_items

    def run_tests(self, items):
        return self.run_tests_in_parallel([items])[0]


def run_tests(session, run_index):
    all_items = {item.nodeid: item for item in session.items}
    node_ids = session.config.cache.get(f"{CACHE_KEY_IDS}{run_index}", [])
    items = [all_items[node_id] for node_id in node_ids if node_id in all_items]
    failed_node_ids = []
    for index, item in enumerate(items):
        test_failed = session.testsfailed
        next_item = items[index + 1] if index + 1 < len(items) else None
        item.config.hook.pytest_runtest_protocol(item=item, nextitem=next_item)
        if session.testsfailed > test_failed:
            failed_node_ids.append(item.nodeid)
    session.config.cache.set(f"{CACHE_KEY_FAILED}{run_index}", failed_node_ids)

    # clear the items - otherwise the tests will be run again by
    # pytest's own pytest_runtestloop
    session.items.clear()
