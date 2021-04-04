from _pytest import main as pytest_main
from find_dependencies.dependency_finder import DependencyFinder


def pytest_addoption(parser):
    group = parser.getgroup("find-dependencies")
    group.addoption(
        "--find-dependencies",
        action="store_true",
        dest="find_dependencies",
        help="""Find dependencies between tests""",
    )


def pytest_runtestloop(session):
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
