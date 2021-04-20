from _pytest import main as pytest_main
from find_dependencies.dependency_finder import DependencyFinder, run_tests


def pytest_addoption(parser):
    group = parser.getgroup("find-dependencies")
    group.addoption(
        "--find-dependencies",
        action="store_true",
        dest="find_dependencies",
        help="""Find dependencies between tests""",
    )
    group.addoption(
        "--reversed-first",
        action="store_true",
        dest="reversed_first",
        help="""Run the test in reverse direction first""",
    )
    group.addoption(
        "--markers-to-ignore",
        action="store",
        dest="markers_to_ignore",
        help="""A comma separated list of markers of tests to ignore.""",
    )
    group.addoption(
        "--find-dependencies-internal",
        action="store_true",
        dest="find_dependencies_internal",
        help="""For internal use only""",
    )


def pytest_runtestloop(session):
    if session.config.getoption("find_dependencies_internal"):
        return run_tests(session)
    if not session.config.getoption("find_dependencies"):
        return pytest_main.pytest_runtestloop(session)

    if len(session.items) == 1:
        print("Only one test collected: ignoring option --find-dependencies")
        return pytest_main.pytest_runtestloop(session)

    if (session.testsfailed and
            not session.config.option.continue_on_collection_errors):
        raise session.Interrupted(
            "%d errors during collection" % session.testsfailed)

    if session.config.option.collectonly:
        return True

    DependencyFinder(session).find_dependencies()
    return True
