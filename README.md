# Real Estate Webform Auto Filler

An automation script to automatically fill out real estate web forms using Selenium. This repository contains a single Python script, webform_filler.py, that logs into a real estate platform and navigates through multiple form sections—entering data from a provided dataset—to complete property assessment forms.

## Features

- **Automated Login:** Logs into a specified real estate management portal using provided credentials.
- **Multi-Section Form Filling:** Automates the navigation and data entry for sections such as:
  - Building Details
  - Classification
  - General Information
  - Dimensions
  - Flats and Maisonettes
  - Walls, Windows, Doors, Floors, and Roofs
  - Heating Systems (Main, Secondary, Water Heating)
  - Special Features and Save/Exit Functionalities
 
  - **Dynamic Waiting & Error Handling:** Uses Selenium’s explicit waits and exception handling to manage page load times and potential element interaction issues.
  - **ChromeDriver Management:** Automatically installs and manages the ChromeDriver using `webdriver_manager`.
 
## Prerequisites
- Python 3.7+
- Google Chrome browser installed
- Python libraries:
  - `selenium`
  - `webdriver_manager`
  - `pandas`
  - `numpy`
 
## Installatio
