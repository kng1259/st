from level2.ChangePassword import ChangePassword
from level2.FilterDesktop import FilterDesktop
from level2.helper import run_tests

if __name__ == "__main__":
    # Define the test classes
    tests = {
        "ChangePassword": ChangePassword,
        "FilterDesktop": FilterDesktop
    }

    for test in tests:
        run_tests(tests[test])