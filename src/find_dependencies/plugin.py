import re
import sys
from typing import Optional

import pytest
from _pytest import main as pytest_main
from find_dependencies.dependency_finder import DependencyFinder, run_tests

try:
    import pytest.Parser as Parser
    import pytest.Config as Config
except ImportError:
    from _pytest.config.argparsing import Parser
    from _pytest.config import Config


def pytest_addoption(parser: Parser) -> None:
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
        "--run-serially",
        action="store_true",
        dest="run_serially",
        help="""Execute all test runs serially instead
         of using parallel processes""",
    )
    group.addoption(
        "--fail-on-failed-tests",
        action="store_true",
        dest="fail_on_failed_tests",
        help="""Let the dependency test also fail for always failing tests""",
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
    group.addoption(
        "--find-dependencies-index",
        action="store",
        dest="find_dependencies_index",
        help="""For internal use only""",
    )


def pytest_runtestloop(session: pytest.Session) -> Optional[object]:
    if session.config.getoption("find_dependencies_internal"):
        index = session.config.getoption("find_dependencies_index") or ""
        return run_tests(session, index)
    if not session.config.getoption("find_dependencies"):
        return pytest_main.pytest_runtestloop(session)

    if len(session.items) == 1:
        print("Only one test collected: ignoring option --find-dependencies")
        restore_verbosity(session.config)
        return pytest_main.pytest_runtestloop(session)

    if session.testsfailed and not session.config.option.continue_on_collection_errors:
        restore_verbosity(session.config)
        raise session.Interrupted("%d errors during collection" % session.testsfailed)

    DependencyFinder(session).find_dependencies()
    return True


def restore_verbosity(config: Config) -> None:
    verbosity = 0
    if hasattr(config, "initial_args"):
        for arg in config.initial_args:
            if arg.startswith("-v"):
                verbosity = len(arg) - 1
                break
            if arg.startswith("-q"):
                verbosity = 1 - len(arg)
                break
            if arg.startswith("--verbosity="):
                verbosity = int(arg[arg.index("=") + 1 :])
                break
    config.option.verbose = verbosity


def pytest_load_initial_conftests(early_config: Config, args: list[str]) -> None:
    """Saves initial arguments to be passed to the test runs."""
    if "--find-dependencies" in args:
        notest_options = ("--collect-only", "--setup-only", "--setup-plan")
        if any(option in args for option in notest_options):
            args.remove("--find-dependencies")
            return

        # make sure that xdist is not used for the tests
        if "xdist" in sys.modules:
            disable_xdist(args)
        early_config.initial_args = args[:]
        early_config.initial_args.remove("--find-dependencies")
        adapt_verbosity(args)


def adapt_verbosity(args: list[str]) -> None:
    """Removes verbosity arguments from the outer test and replaces them
    with -qq (very quiet) to avoid confusing information ("no tests run").
    The given verbosity will still be passed to the internal test runs."""
    if "--collect-only" not in args:
        for i, arg in enumerate(args):
            if arg.startswith(("-v", "-q", "--verbosity")):
                del args[i]
        args.insert(0, "-qq")


def disable_xdist(args: list[str]) -> None:
    for i, arg in enumerate(args):
        # remove -n # option
        if arg == "-n":
            del args[i]
            del args[i]
            break
        # remove -n# option
        if re.match(r"-n\d+", arg):
            del args[i]
            break
    args.insert(0, "-n0")
