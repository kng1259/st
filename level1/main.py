from ChangePassword import ChangePassword
from FilterDesktop import FilterDesktop
import pandas as pd
from numpy import nan
import unittest

if __name__ == "__main__":
    # Define the test classes
    tests = {
        # "ChangePassword": ChangePassword,
        "FilterDesktop": FilterDesktop
    }

    for test in tests:
        # Load the test data from the csv file
        df = pd.read_csv(f"data/{test}.csv", na_values=[""])
        df = df.replace({nan: None})
        
        # Convert the DataFrame to a list of dictionaries
        test_data = df.to_dict(orient='records')
        for d in test_data:
            for key in d:
                if key[-2:] == "_s":
                    d[key] = str(d[key]).split("|") if d[key] else []
                    
        # Create a test suite
        suite = unittest.TestSuite()
        
        # Add tests to the suite
        for data in test_data:
            suite.addTest(tests[test](f'test', data))
        
        # Run the tests
        runner = unittest.TextTestRunner()
        runner.run(suite)