Password Strength Checker

Description

This is a Python-based GUI application that helps users evaluate the strength of their passwords and check if they have been compromised using the "Have I Been Pwned" (HIBP) API. The application is built using Tkinter and provides real-time password strength assessment.

Features

Real-time password strength checking based on:

Minimum length of 8 characters

At least one uppercase letter

At least one lowercase letter

At least one digit

At least one special character

Show/hide password option

"Have I Been Pwned" integration to check if a password has been leaked in breaches

Reset button to clear input fields

Dark mode toggle for user preference

Installation

Prerequisites

Ensure you have Python installed on your system. You also need to install requests if not already installed.

pip install requests

Running the Application

Clone this repository:

git clone https://github.com/waqar373-ux/Password_Strength_Checker

Navigate to the project directory:

cd Password-Strength-Checker

Run the script:

python password_checker.py

How It Works

Enter a password in the text field.

The application evaluates its strength based on predefined criteria and provides instant feedback.

Clicking on "Have I Been Pwned" checks if the password has been exposed in data breaches:

The password is hashed using SHA-1.

Only the first 5 characters of the hash are sent to the HIBP API.

HIBP returns a list of matching hashes, and the application checks if the password appears in the leaked data.

The user can toggle between dark and bright modes.

Security Considerations:

Your password is never sent directly to any server.

Only a partial hash (first 5 characters) is shared with HIBP to ensure privacy.

The HIBP API returns multiple possible leaked hashes, preventing direct identification of the user's password.
