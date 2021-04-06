import sys

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
        "--find-dependencies-internal",
        action="store_true",
        dest="find_dependencies_internal",
        help="""For internal use only""",
    )


def pytest_cmdline_preparse(args):
    if "--find-dependencies" in args and "pytest_randomly" in sys.modules:
        args[:] = ["--randomly-dont-reorganize"] + args


def pytest_runtestloop(session):
    if session.config.getoption("find_dependencies_internal"):
        return run_tests(session)
    if not session.config.getoption("find_dependencies"):
        return pytest_main.pytest_runtestloop(session)

    if (session.testsfailed and
            not session.config.option.continue_on_collection_errors):
        raise session.Interrupted(
            "%d errors during collection" % session.testsfailed)

    if session.config.option.collectonly:
        return True

    DependencyFinder(session).find_dependencies()
    return True
