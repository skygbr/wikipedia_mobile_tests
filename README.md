# Wikipedia Mobile App Authentication Tests

This project contains automated tests for the Wikipedia mobile app authentication functionality using Appium and Python.

## Prerequisites

- Python 3.8 or higher
- Appium Server
- Android SDK (for Android testing)
- Xcode (for iOS testing)
- iOS Simulator or Android Emulator
- Allure Command Line Tool

## Notes

- Tests are designed to be maintainable and follow Page Object Model pattern
- All sensitive data is stored in environment variables
- Cross-platform support for both iOS and Android
- Allure reports provide detailed test execution information with screenshots and logs

I've created a test automation project for the Wikipedia mobile app's authentication functionality. Here's a summary of what I've set up:

1. Project Structure:
tests/ - Contains test cases and configuration
pages/ - Contains page objects
utils/ - Contains driver configuration
Configuration files (requirements.txt, .gitignore)

2. Test Framework:
- Python with pytest
- Appium for mobile automation
- Page Object Model pattern
- Environment variables for sensitive data

3. Test Cases:
- Successful login with valid credentials
- Failed login with invalid password
- Failed login with invalid username
- Empty credentials validation
- Remember me functionality

4. Features:
- Cross-platform support (iOS and Android)
- Configurable through command line arguments
- HTML test reports
- Clean code organization
- Proper documentation
- Bypass prison Сaptcha

5. The code is organized following best practices:
- Page Object Model for maintainable test code
- Clear separation of concerns
- Proper error handling
- Configuration through environment variables
- Comprehensive documentation
- Cross-platform support

## Setup
1. Create virtual environment
```bash
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # for macOS/Linux
# or
.venv\Scripts\activate  # for Windows
# Create .env file
touch .env

# Add required variables to .env
echo "WIKIPEDIA_USERNAME=your_username" >> .env
echo "WIKIPEDIA_PASSWORD=your_password" >> .env
```
2. Install Python dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

3. Install and start Appium Server Setup:
```bash
npm install -g appium
# Install your project in development mode:
pip install -e
# Start Appium server
appium
```

4. Install Allure Command Line Tool:
```bash
# For macOS
brew install allure

# For Windows (using Scoop)
scoop install allure

# For Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

5. Start Appium server:
```bash
appium
```

6. Create a `.env` file in the project root with your test credentials:
```bash
WIKIPEDIA_USERNAME=your_test_username
WIKIPEDIA_PASSWORD=your_test_password
```
7. Start the iOS simulator:
```bash
xcrun simctl list devices | grep -i "iphone 14 pro max"
xcrun simctl boot 6D346A21-DB65-45A1-AEEE-0CD3925B13F2
open -a Simulator
# Launch a specific iOS simulator
# For iPhone 16 Pro
xcrun simctl boot "iPhone 16 Pro"
# For iPhone 14 Pro Max
xcrun simctl boot "iPhone 14 Pro Max"
# For iPad
xcrun simctl boot "iPad Pro (11-inch) (4th generation)"
# Open Simulator app:
open -a Simulator
# Common simulator management commands:
# Shutdown a simulator
xcrun simctl shutdown "iPhone 15 Pro"
# Erase a simulator
xcrun simctl erase "iPhone 15 Pro"
# Get simulator status
xcrun simctl list devices | grep Booted
# Install an app on simulator
xcrun simctl install booted /path/to/your.app
# Launch an app on simulator
xcrun simctl launch booted com.wikimedia.wikipedia
# Create a new simulator:
xcrun simctl create "My Custom iPhone" "iPhone 15 Pro" "iOS 17.2"
# Delete a simulator:
# First get the device UDID
xcrun simctl list devices
# Then delete using the UDID
xcrun simctl delete <UDID>
# Reset all simulators:
xcrun simctl erase all
# Take a screenshot:
xcrun simctl io booted screenshot screenshot.png
# Start video recording
xcrun simctl io booted recordVideo video.mp4
# Start recording
xcrun simctl io booted recordVideo video.mp4
#Set simulator location:
xcrun simctl location booted set 37.33233141 -122.0312186
```


## Android Setup

1. Install Android Studio and Android SDK
2. Set up environment variables:
   ```bash
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
   ```
3. Create an Android Virtual Device (AVD) or connect a physical device
4. Install the Wikipedia app on the device/emulator

## Project Structure

```
├── tests/
│   ├── conftest.py           # Test configuration and fixtures
│   └── test_auth.py          # Authentication test cases
├── pages/
│   └── auth_page.py          # Page object for authentication
├── utils/
│   └── driver.py             # Appium driver configuration
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## Running Tests

To run all tests:
```bash
pytest tests/ -v
```

# For iOS
```bash
pytest tests/ -v --platform=ios
```

# For Android
```bash
pytest tests/ -v --platform=android
```

## Generating Allure Reports

1. Run tests with Allure:
```bash
# For iOS
pytest tests/ -v --platform=ios --alluredir=./allure-results

# For Android
pytest tests/ -v --platform=android --alluredir=./allure-results
```

2. Generate and open Allure report:
```bash
allure serve ./allure-results
```

3. Generate static report:
```bash
allure generate ./allure-results -o ./allure-report --clean
```

4. Run specific tests tests with verbose output and Allure report:
```bash
pytest tests/test_auth.py::TestAuthentication::test_successful_login tests/test_auth.py::TestAuthentication::test_invalid_password tests/test_auth.py::TestAuthentication::test_invalid_username tests/test_auth.py::TestAuthentication::test_empty_credentials -v --platform=ios --alluredir=./allure-results
```

5. Project Cleanup:
```bash
# Remove pytest cache
rm -rf .pytest_cache
# Remove report directory
rm -rf allure-results
# Remove package metadata directory
rm -rf wikipedia_mobile_tests.egg-info
```

6. Debugging Commands:
```bash
# Run tests with debug logging
pytest -v --log-cli-level=DEBUG
# Run tests with stop on first failure
pytest -x
# Run tests with screenshots on failure
pytest --screenshot-on-failure
```

7. Сommands required to obtain Wikipedia.app through git:
```bash
# Clone the Wikipedia iOS repository:
git clone https://github.com/wikimedia/wikipedia-ios.git
# Navigate to the project directory:
cd wikipedia-ios
# Install dependencies using CocoaPods:
pod install
# Ensure CocoaPods is installed:
gem install cocoapods
#Open the project in Xcode:
open Wikipedia.xcworkspace
# Build the application:
# - In Xcode, select the "Wikipedia" scheme
# - Choose simulator or device
# - Press Cmd + B to build

#Locate the built .app file:
# For simulator builds
~/Library/Developer/Xcode/DerivedData/Wikipedia-*/Build/Products/Debug-iphonesimulator/Wikipedia.app

# For device builds
~/Library/Developer/Xcode/DerivedData/Wikipedia-*/Build/Products/Debug-iphoneos/Wikipedia.app

# Copy the .app file to your project directory:
cp -r ~/Library/Developer/Xcode/DerivedData/Wikipedia-*/Build/Products/Debug-iphonesimulator/Wikipedia.app /path/to/your/project/apps/
```

## Results of running the autotest
```bash
.venvskygbr@MacBookPro wikipedia_mobile_tests % pytest tests/test_auth.py::TestAuthentication::test_successful_login tests/test_auth.py::TestAuthentication::test_invalid_password tests/test_auth.py::TestAuthentication::test_invalid_username tests/test_auth.py::TestAuthentication::test_empty_credentials -v --platform=ios --alluredir=./allure-results
========================================= test session starts =========================================
platform darwin -- Python 3.13.1, pytest-7.4.3, pluggy-1.5.0 -- /Users/skygbr/wikipedia_mobile_tests/.venv/bin/python
cachedir: .pytest_cache
metadata: {'Python': '3.13.1', 'Platform': 'macOS-15.4.1-arm64-arm-64bit-Mach-O', 'Packages': {'pytest': '7.4.3', 'pluggy': '1.5.0'}, 'Plugins': {'html': '4.1.1', 'metadata': '3.1.1', 'allure-pytest': '2.13.2'}}
rootdir: /Users/skygbr/wikipedia_mobile_tests
plugins: html-4.1.1, metadata-3.1.1, allure-pytest-2.13.2
collected 4 items                                                                                     

tests/test_auth.py::TestAuthentication::test_successful_login PASSED                            [ 25%]
tests/test_auth.py::TestAuthentication::test_invalid_password PASSED                            [ 50%]
tests/test_auth.py::TestAuthentication::test_invalid_username PASSED                            [ 75%]
tests/test_auth.py::TestAuthentication::test_empty_credentials PASSED                           [100%]

========================== 4 passed in 56.18s (0:00:56) ========================
```
