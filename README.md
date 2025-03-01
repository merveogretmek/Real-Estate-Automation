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
 
## Installation

1. Clone the Repository:

```bash
git clone https://github.com/merveogretmek/real-estate-webform-auto-filler.git
cd real-estate-webform-auto-filler
```

2. Install Dependencies:

```bash
pip install selenium webdriver-manager pandas numpy
```

## Usage 

1. Configuration:
   
- Update the login credentials in `webform_filler.py` (replace `'username_here'` and `'password_here'` with your actual credentials).
- Ensure your input data is loaded into a pandas DataFrame named `data`. The script expects specific column names that correspond to each form field (e.g., "Postcode", "Assessment Date", "Tenure", etc.).

2. Run the Script:

```bash
python webform_filler.py
```

The script will:
- Open the target URL and log in.
- Navigate through the web form, filling out each section with data from the DataFrame.
- Handle common Selenium exceptions and move seamlessly between sections.
- Save and exit the form once all data has been submitted.

## Project Structure

```bash
RealEstateWebFormAutoFiller/
├── webform_filler.py   # Main automation script
└── README.md           # Project documentation
```


Contributions, issues, and feature requests are welcome! Please feel free to open an issue or submit a pull request.


