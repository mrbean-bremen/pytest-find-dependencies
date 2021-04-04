from importlib import reload


class DependencyFinder:
    """Tries to find dependencies between tests using reverse executing
    first and more test executions using binary search to get dependent
    tests."""
    def __init__(self, session):
        self.session = session
        self.dependent_items = {}

    def find_dependencies(self):
        failed1 = self.run_tests(self.session.items)
        if failed1:
            print("\nFailing test(s) on first run excluded from analysis")
        items = self.session.items[::-1]
        failed_items = self.run_tests(items) - failed1
        for item in failed_items:
            self.check_failed_item(item, items)

        if not self.dependent_items:
            print("\nNo dependent tests found.")
        else:
            print("\nDependent tests:")
            for dependent, item in self.dependent_items.items():
                print(f"{item.nodeid} -> {dependent.nodeid}")

    def check_failed_item(self, item, items, failed=True):
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

        modules = {item.module for item in sub_items}
        for module in modules:
            reload(module)
        failed_items = self.run_tests(sub_items_to_run)
        self.check_failed_item(item, sub_items, item in failed_items)

    def run_tests(self, items):
        failed_items = set()
        for index, item in enumerate(items):
            test_failed = self.session.testsfailed
            next_item = items[index + 1] if index + 1 < len(items) else None
            item.config.hook.pytest_runtest_protocol(item=item,
                                                     nextitem=next_item)
            if self.session.testsfailed > test_failed:
                failed_items.add(item)
        return failed_items
