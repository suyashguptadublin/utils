import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('bank_database.db')
cursor = connection.cursor()

# Create the loans table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
        LoanType TEXT NOT NULL CHECK(LoanType IN ('Personal', 'Mortgage', 'Auto')),
        LoanAmount DECIMAL(10, 2) NOT NULL,
        InterestRate DECIMAL(10, 2) NOT NULL,
        Term INTEGER NOT NULL,
        StartDate DATE NOT NULL DEFAULT CURRENT_DATE,
        EndDate DATE NOT NULL
    )
""")

# Commit the changes
connection.commit()

# Close the connection
connection.close()





import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('bank_database.db')
cursor = connection.cursor()

# Insert sample data into the loans table
loans_data = [
    ('Personal', 10000.00, 6.00, 60, '2022-01-01', '2027-01-01'),
    ('Mortgage', 200000.00, 4.50, 360, '2022-01-01', '2052-01-01'),
    ('Auto', 30000.00, 5.00, 60, '2022-01-01', '2027-01-01')
]

cursor.executemany("""
    INSERT INTO loans (LoanType, LoanAmount, InterestRate, Term, StartDate, EndDate)
    VALUES (?, ?, ?, ?, ?, ?)
""", loans_data)

# Commit the changes
connection.commit()

# Close the connection
connection.close()



# features/loans.feature

Feature: Loans
  As a bank
  I want to manage loans
  So that I can track loan details

  Scenario: Insert a new loan
    Given the database is empty
    When I insert a new loan with type "Personal" and amount 10000.00
    Then the loan should be inserted successfully

  Scenario: Retrieve loan details
    Given the database contains a loan with type "Mortgage" and amount 200000.00
    When I retrieve the loan details
    Then the loan type should be "Mortgage" and amount should be 200000.00

  Scenario: Update loan details
    Given the database contains a loan with type "Auto" and amount 30000.00
    When I update the loan amount to 35000.00
    Then the loan amount should be updated to 35000.00



# features/steps/loans_steps.py

import sqlite3
from behave import given, when, then

@given("the database is empty")
def step_impl(context):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM loans")
    connection.commit()
    connection.close()

@when("I insert a new loan with type {loan_type} and amount {loan_amount}")
def step_impl(context, loan_type, loan_amount):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO loans (LoanType, LoanAmount, InterestRate, Term, StartDate, EndDate)
        VALUES (?, ?, 6.00, 60, '2022-01-01', '2027-01-01')
    """, (loan_type, float(loan_amount)))
    connection.commit()
    connection.close()

@then("the loan should be inserted successfully")
def step_impl(context):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loans")
    loans = cursor.fetchall()
    assert len(loans) == 1
    connection.close()

@given("the database contains a loan with type {loan_type} and amount {loan_amount}")
def step_impl(context, loan_type, loan_amount):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM loans WHERE LoanType = ? AND LoanAmount = ?
    """, (loan_type, float(loan_amount)))
    loan = cursor.fetchone()
    assert loan is not None
    connection.close()

@when("I retrieve the loan details")
def step_impl(context):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM loans WHERE LoanType = 'Mortgage' AND LoanAmount = 200000.00
    """)
    context.loan = cursor.fetchone()
    connection.close()

@then("the loan type should be {loan_type} and amount should be {loan_amount}")
def step_impl(context, loan_type, loan_amount):
    assert context.loan[1] == loan_type
    assert context.loan[2] == float(loan_amount)

@given("the database contains a loan with type {loan_type} and amount {loan_amount}")
def step_impl(context, loan_type, loan_amount):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM loans WHERE LoanType = ? AND LoanAmount = ?
    """, (loan_type, float(loan_amount)))
    loan = cursor.fetchone()
    assert loan is not None
    connection.close()

@when("I update the loan amount to {new_amount}")
def step_impl(context, new_amount):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE loans SET LoanAmount = ? WHERE LoanType = 'Auto'
    """, (float(new_amount),))
    connection.commit()
    connection.close()

@then("the loan amount should be updated to {new_amount}")
def step_impl(context, new_amount):
    connection = sqlite3.connect('bank_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT LoanAmount FROM loans WHERE LoanType = 'Auto'
    """)
    updated_amount = cursor.fetchone()[0]
    assert updated_amount == float(new_amount)
    connection.close()
