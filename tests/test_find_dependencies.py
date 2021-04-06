import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def test_path(testdir):
    testdir.tmpdir.join("pytest.ini").write(
        "[pytest]\n" "console_output_style = classic"
    )
    yield testdir


def test_no_checks_if_not_configured(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        def test_b(): pass
        def test_c(): pass
        """
    )
    result = test_path.runpytest("-v", "-p", "no:randomly")
    result.assert_outcomes(passed=3, failed=0)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_c PASSED"
    ])


def test_no_dependencies(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        def test_b(): assert False
        def test_c(): pass
        """
    )

    result = test_path.runpytest("-v", "--find-dependencies")
    result.stdout.fnmatch_lines([
        "No dependent tests found."
    ])


def test_single_dependency_last_index(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        """
    )

    result = test_path.runpytest("--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 3 tests.",
        "Executed 6 tests in 2 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_c"
    ])


def test_single_dependency_first_index(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): global flag; flag = False
        def test_b(): assert flag
        def test_c(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 3 tests.",
        "Executed 6 tests in 2 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_a"
    ])


def test_single_dependency1(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        def test_d(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 4 tests.",
        "Executed 10 tests in 3 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_c"
    ])


def test_single_dependency2(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): pass
        def test_d(): pass
        def test_e(): pass
        def test_f(): pass
        def test_g(): global flag; flag = False
        def test_h(): pass
        def test_i(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 9 tests.",
        "Executed 26 tests in 5 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_g"
    ])


def test_single_dependency3(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): global flag; flag = False
        def test_c(): pass
        def test_d(): pass
        def test_e(): assert flag
        def test_f(): pass
        def test_g(): pass
        """
    )

    result = test_path.runpytest("-v", "--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 19 tests in 4 test runs.",
        "Dependent tests:",
        "test_one.py::test_e depends on test_one.py::test_b"
    ])


def test_two_dependencies(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): pass
        def test_d(): assert flag
        def test_e(): global flag; flag = False
        def test_f(): pass
        """
    )

    result = test_path.runpytest("-v", "--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 6 tests.",
        "Executed 19 tests in 5 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_e",
        "test_one.py::test_d depends on test_one.py::test_e"
    ])


def test_single_dependency_in_other_module1(test_path):
    test_path.makepyfile(
        test_one="""
        import util
        def test_a(): pass
        def test_b(): util.set_flag(False)
        def test_c(): pass
        def test_d(): pass
        def test_e(): assert util.flag
        def test_f(): pass
        def test_g(): pass
        """
    )
    test_path.makepyfile(
        util="""
        flag = True
        def set_flag(new_flag):
            global flag
            flag = new_flag
        """
    )

    result = test_path.runpytest("-v", "--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 19 tests in 4 test runs.",
        "Dependent tests:",
        "test_one.py::test_e depends on test_one.py::test_b"
    ])


def test_single_dependency_in_other_module2(test_path):
    test_path.makepyfile(
        test_one="""
        import util
        def test_a(): pass
        def test_b(): assert util.flag
        def test_c(): pass
        def test_d(): pass
        def test_e(): util.set_flag(False)
        def test_f(): pass
        def test_g(): pass
        """
    )
    test_path.makepyfile(
        util="""
        flag = True
        def set_flag(new_flag):
            global flag
            flag = new_flag
        """
    )
    result = test_path.runpytest("-v", "--find-dependencies")
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 19 tests in 4 test runs.",
        "Dependent tests:",
        "test_one.py::test_b depends on test_one.py::test_e"
    ])
