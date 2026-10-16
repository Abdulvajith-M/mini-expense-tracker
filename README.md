# Mini Expense Tracker

## Project Description

Mini Expense Tracker is a web application that helps users
record, view, update, and delete their daily expenses.

Users can categorize expenses, filter expenses by category,
and view the total amount of their expenses.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- Git and GitHub

## Features

- Add a new expense
- View all expenses
- Edit existing expenses
- Delete expenses with confirmation
- Filter expenses by category
- Calculate total expenses
- Validate user input
- Store expense data in an SQLite database

## Expense Fields

- Title: Required, maximum 100 characters
- Amount: Required and greater than zero
- Category: Food, Travel, Bills, Shopping, or Other
- Expense Date: Required and cannot be in the future
- Notes: Optional, maximum 250 characters

## Project Structure

project/
├── app.py
├── templates/
│   ├── index.html
│   └── edit.html
├── instance/
│   └── expenses.db
└── README.md

## Requirements

- Python 3
- pip

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in a terminal.
3. Create a virtual environment:

   python -m venv .venv

4. Activate the virtual environment on Windows:

   .venv\Scripts\activate

5. Install the required packages:

   pip install Flask Flask-SQLAlchemy

6. Run the application:

   python app.py

7. Open the following address in your browser:

   http://127.0.0.1:5000

## Database

The application uses SQLite to store expense records.
The database tables are created automatically when the
application starts.

## Validation

The application validates required fields, title length,
positive expense amounts, valid categories, date values,
future dates, and notes length.

## Sample Data

The application was tested with five sample expenses
across different categories.

## Assumptions

- No login or user authentication is required.
- Expense amounts must be greater than zero.
- Expense dates cannot be in the future.
- Users can select from the predefined expense categories.

## AI Usage Declaration

AI assistance was used during development to help with
debugging, understanding Flask routes, and implementing
application features.

All generated suggestions were reviewed and tested during
development.

## AI Mistake and Correction

During development, the Edit feature initially failed
because the edit route was not registered correctly.

The application returned a BuildError when trying to open
the Edit page.

This was fixed by correcting the route definition and
ensuring that the edit route was defined at the top level
of the Flask application. The route was then tested again.