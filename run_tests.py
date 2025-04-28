import pytest
import os
from datetime import datetime

def run_tests():
    """Run the specified test suite"""
    
    # Create results directory if it doesn't exist
    results_dir = "test_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate timestamp for the report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # List of tests to run
    test_list = [
        "tests/test_auth.py::TestAuthentication::test_successful_login",
        "tests/test_auth.py::TestAuthentication::test_invalid_password",
        "tests/test_auth.py::TestAuthentication::test_invalid_username",
        "tests/test_auth.py::TestAuthentication::test_empty_credentials",
        "tests/test_auth.py::TestAuthentication::test_remember_me"
    ]
    
    # Command line arguments for pytest
    pytest_args = [
        "-v",  # Verbose output
        "--html=test_results/report_{}.html".format(timestamp),  # HTML report
        "--self-contained-html",  # Self-contained HTML report
        "--alluredir=test_results/allure_{}".format(timestamp),  # Allure report directory
        "--reruns=2",  # Number of retries for failed tests
        "--reruns-delay=1",  # Delay between retries in seconds
        "-n=2"  # Run tests in parallel (2 workers)
    ]
    
    # Add test list to arguments
    pytest_args.extend(test_list)
    
    # Run the tests
    pytest.main(pytest_args)

if __name__ == "__main__":
    run_tests() 