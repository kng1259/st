from level1.ChangePassword import ChangePassword
from level1.FilterDesktop import FilterDesktop
from level1.helper import run_tests

if __name__ == "__main__":
    # Define the test classes
    tests = {
        "ChangePassword": ChangePassword,
        "FilterDesktop": FilterDesktop
    }

    for test in tests:
        run_tests(tests[test])