from setuptools import setup, find_packages

setup(
    name="wikipedia_mobile_tests",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Appium-Python-Client==3.1.1",
        "pytest==7.4.3",
        "pytest-html==4.1.1",
        "selenium==4.15.2",
        "webdriver-manager==4.0.1",
        "python-dotenv==1.0.0",
        "allure-pytest==2.13.2",
        "allure-python-commons==2.13.2",
        "setuptools>=79.0.1"
    ],
    python_requires=">=3.8",
) 