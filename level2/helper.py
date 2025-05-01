import pandas as pd
from numpy import nan
import unittest

def run_tests(test):
    # Load the test data from the csv file
    df = pd.read_csv(f"level2/data/{test.__name__}.csv", na_values=[""]).replace({nan: None})

    # Convert the DataFrame to a list of dictionaries
    test_data = df.to_dict(orient='records')
    for d in test_data:
        for key in d:
            if key[-2:] == "_s":
                d[key] = str(d[key]).split("|") if d[key] else []

    fields = pd.read_csv(f"level2/fields/{test.__name__}.csv", na_values=[""]).replace({nan: None}).to_dict(orient='records')[0]
    if "buttons_nums" in fields:
        fields['buttons_nums'] = [int(i) for i in str(fields['buttons_nums']).split("|") if i]
                
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add tests to the suite
    for data in test_data:
        suite.addTest(test(f'test', data, fields))
    
    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)