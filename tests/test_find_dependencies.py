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
    result = test_path.runpytest("-v", "-p", "no:randomly", "-W ignore")
    result.assert_outcomes(passed=3, failed=0)
    result.stdout.fnmatch_lines([
        "test_one.py::test_a PASSED",
        "test_one.py::test_b PASSED",
        "test_one.py::test_c PASSED"
    ])


def test_no_checks_for_single_test(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        """
    )
    result = test_path.runpytest("-v", "--find-dependencies", "-W ignore")
    result.assert_outcomes(passed=1, failed=0)
    result.stdout.fnmatch_lines([
        "Only one test collected: ignoring option --find-dependencies",
        "test_one.py::test_a PASSED",
    ])


def test_no_checks_if_collection_failed(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        def test_b(): pass
        """
    )
    test_path.makepyfile(
        conftest="""
        def pytest_collection(session):
            session.perform_collect()
            session.testsfailed = 1
        """
    )
    result = test_path.runpytest("--find-dependencies", "-W ignore")
    result.assert_outcomes(passed=0, failed=0)
    assert int(result.ret) == 2
    result.stdout.fnmatch_lines([
        "*Interrupted: 1 errors during collection*",
        "*no tests ran*"
    ])


def test_no_dependencies(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        def test_b(): assert False
        def test_c(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "The following tests are always failing and are "
        "excluded from the analysis:",
        "  test_one.py::test_b",
        "No dependent tests found."
    ])


def test_single_dependency_collect_only(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        """
    )

    result = test_path.runpytest("--find-dependencies", "--collect-only",
                                 "-p", "no:randomly")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "collected 3 items",
        "<Module test_one.py>",
        "  <Function test_a>",
        "  <Function test_b>",
        "  <Function test_c>"
    ])


def test_single_dependency_setup_only(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        """
    )

    result = test_path.runpytest("--find-dependencies", "--setup-only",
                                 "-p", "no:randomly")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "collected 3 items",
        "test_one.py*",
        "        test_one.py::test_a",
        "        test_one.py::test_b",
        "        test_one.py::test_c"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 3 tests.",
        "Executed 7 tests in 3 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_c"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 3 tests.",
        "Executed 6 tests in 2 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_a"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 4 tests.",
        "Executed 11 tests in 4 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_c"
    ])


def test_single_reversed_first(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        def test_d(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies", "--reversed-first",
                                 "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 4 tests.",
        "Executed 10 tests in 3 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_c"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 9 tests.",
        "Executed 27 tests in 6 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_g"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 19 tests in 4 test runs.",
        "Dependent tests:",
        "  test_one.py::test_e depends on test_one.py::test_b"
    ])


def test_single_dependency1_with_randomly(test_path):
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
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 4 tests.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_c"
    ])


def test_single_dependency2_with_randomly(test_path):
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 9 tests.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_g"
    ])


def test_single_dependency3_with_randomly(test_path):
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

    result = test_path.runpytest("--find-dependencies")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Dependent tests:",
        "  test_one.py::test_e depends on test_one.py::test_b"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 6 tests.",
        "Executed 21 tests in 7 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_e",
        "  test_one.py::test_d depends on test_one.py::test_e"
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

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 19 tests in 4 test runs.",
        "Dependent tests:",
        "  test_one.py::test_e depends on test_one.py::test_b"
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
    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 7 tests.",
        "Executed 20 tests in 5 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_e"
    ])


def test_permanent_dependency(test_path):
    test_path.makepyfile(
        test_one="""
        import util
        def test_a(): pass
        def test_b(): assert not util.lock_exists()
        def test_c(): pass
        def test_d(): util.create_lock()
        def test_e(): pass
        """
    )
    test_path.makepyfile(
        util="""
        import os
        def create_lock():
            with open("lock.lck", "w") as f:
                f.write("test")

        def lock_exists():
            return os.path.exists("lock.lck")
        """
    )
    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 5 tests.",
        "Executed 11 tests in 3 test runs.",
        "Tests failing permanently after all tests have run:",
        "  test_one.py::test_b"
    ])


def test_permanent_dependency_reversed_first(test_path):
    test_path.makepyfile(
        test_one="""
        import util
        def test_a(): pass
        def test_b(): assert not util.lock_exists()
        def test_c(): pass
        def test_d(): util.create_lock()
        def test_e(): pass
        """
    )
    test_path.makepyfile(
        util="""
        import os
        def create_lock():
            with open("lock1.lck", "w") as f:
                f.write("test")

        def lock_exists():
            return os.path.exists("lock1.lck")
        """
    )
    result = test_path.runpytest("--find-dependencies", "--reversed-first",
                                 "-p", "no:randomly")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 5 tests.",
        "Executed 10 tests in 2 test runs.",
        "The following tests are always failing and are "
        "excluded from the analysis:",
        "  test_one.py::test_b",
        "No dependent tests found."
    ])


def test_ignored_tests_with_marker_no_dependency(test_path):
    test_path.makepyfile(
        test_one="""
        import pytest

        def test_a(): pass
        @pytest.mark.order(2)
        def test_b(): pass
        def test_c(): pass
        def test_d(): pass
        @pytest.mark.order(1)
        def test_e(): pass
        @pytest.mark.dependency
        def test_f(): pass
        """
    )
    result = test_path.runpytest("--find-dependencies", "-vv",
                                 "--markers-to-ignore=order,dependency",
                                 "-p", "no:randomly")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 3 tests.",
        "Executed 6 tests in 2 test runs.",
        "No dependent tests found."
    ])


def test_filenames(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): print("one::a")
        def test_b(): print("one::b")
        """,
        test_two="""
        def test_c(): print("two::a")
        def test_d(): print("two::b")
        """,
        test_three="""
        def test_e(): print("three::a")
        def test_f(): print("three::b")
        """
    )

    result = test_path.runpytest(
        "--find-dependencies", "test_one.py", "test_three.py")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "Run dependency analysis for 4 tests.",
        "Executed 8 tests in 2 test runs.",
        "No dependent tests found."
    ])


def test_passed_arguments(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        """
    )

    result = test_path.runpytest("--find-dependencies", "-p", "no:randomly",
                                 "-v", "-s")
    assert int(result.ret) == 1
    result.stdout.fnmatch_lines([
        "Running pytest with arguments --find-dependencies-internal "
        "-n0 -p no:randomly -v -s *",
        "Run dependency analysis for 3 tests.",
        "Executed 7 tests in 3 test runs.",
        "Dependent tests:",
        "  test_one.py::test_b depends on test_one.py::test_c"
    ])


@pytest.mark.skipif(pytest.__version__ < "5.3.0",
                    reason="no_fnmatch_line not available")
def test_verbosity_ignored_in_outer_test(test_path):
    test_path.makepyfile(
        test_one="""
        flag = True
        def test_a(): pass
        def test_b(): assert flag
        def test_c(): global flag; flag = False
        """
    )

    result = test_path.runpytest("--find-dependencies", "-vv")
    assert int(result.ret) == 1
    result.stdout.no_fnmatch_line("* no tests ran *")

    result = test_path.runpytest("--find-dependencies", "-q")
    assert int(result.ret) == 1
    result.stdout.no_fnmatch_line("* no tests ran *")

    result = test_path.runpytest("--find-dependencies", "--verbosity=1")
    assert int(result.ret) == 1
    result.stdout.no_fnmatch_line("* no tests ran *")


def test_verbosity_restored_for_single_test(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): pass
        """
    )

    result = test_path.runpytest("--find-dependencies", "-vv")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines(["* 1 passed in *"])

    result = test_path.runpytest("--find-dependencies", "-q")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines(["*1 passed in *"])

    result = test_path.runpytest("--find-dependencies", "--verbosity=1")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines(["* 1 passed in *"])


def test_removed_xdist_args(test_path):
    test_path.makepyfile(
        test_one="""
        def test_a(): print("one::a")
        def test_b(): print("one::b")
        """,
        test_two="""
        def test_c(): print("two::a")
        def test_d(): print("two::b")
        """
    )

    result = test_path.runpytest(
        "--find-dependencies", "-n", "2", "-s")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "Running pytest with arguments --find-dependencies-internal -n0 -s *",
    ])

    result = test_path.runpytest(
        "--find-dependencies", "-n3", "-v")
    assert int(result.ret) == 0
    result.stdout.fnmatch_lines([
        "Running pytest with arguments --find-dependencies-internal -n0 -v *",
    ])
