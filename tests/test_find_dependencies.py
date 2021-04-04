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
    result = test_path.runpytest("-v")
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
    result.assert_outcomes(passed=4, failed=2)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_a PASSED",
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

    result = test_path.runpytest("-v", "--find-dependencies")
    result.assert_outcomes(passed=5, failed=1)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_a PASSED",
        "Dependent tests:",
        "test_one.py::test_c -> test_one.py::test_b"
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

    result = test_path.runpytest("-v", "--find-dependencies")
    result.assert_outcomes(passed=9, failed=1)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_d PASSED",
        "test_one.py::test_d PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_a PASSED",
        "test_one.py::test_d PASSED",
        "test_one.py::test_b PASSED",
        "Dependent tests:",
        "test_one.py::test_c -> test_one.py::test_b"
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

    result = test_path.runpytest("-v", "--find-dependencies")
    result.assert_outcomes(passed=24, failed=2)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_d PASSED",
        "test_one.py::test_e PASSED",
        "test_one.py::test_f PASSED",
        "test_one.py::test_g PASSED",
        "test_one.py::test_h PASSED",
        "test_one.py::test_i PASSED",
        "test_one.py::test_i PASSED",
        "test_one.py::test_h PASSED",
        "test_one.py::test_g PASSED",
        "test_one.py::test_f PASSED",
        "test_one.py::test_e PASSED",
        "test_one.py::test_d PASSED",
        "test_one.py::test_c PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_a PASSED",
        "test_one.py::test_i PASSED",
        "test_one.py::test_h PASSED",
        "test_one.py::test_g PASSED",
        "test_one.py::test_b FAILED",
        "test_one.py::test_i PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_h PASSED",
        "test_one.py::test_b PASSED",
        "Dependent tests:",
        "test_one.py::test_g -> test_one.py::test_b"
    ])
