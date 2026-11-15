# Gym Management System (GUI + Python Data Analytics)

A beginner-friendly desktop project built with Python Tkinter, Pandas, NumPy and Matplotlib.

## Features
- Add and delete gym members.
- Store member records in `members.csv`.
- Record payments and distinguish Paid/Pending transactions.
- Mark attendance once per member per day.
- View dashboard KPIs: total members, active members, paid revenue and attendance records.
- View payment-status and membership-plan charts.

## Technology
- Python 3.9+
- Tkinter (usually included with standard Python installations)
- Pandas
- NumPy
- Matplotlib
- CSV files for local storage

## Setup
1. Install Python 3.9 or later.
2. Open a terminal in this folder.
3. Install libraries:
   `pip install -r requirements.txt`
4. Run:
   `python GymManagementSystem.py`

On some systems use `python3 GymManagementSystem.py`.

## Sample data
The CSV files contain fictional sample records so the dashboard is not empty on first launch. Back up the CSV files before replacing or deleting sample data.

## Important project assumptions / limitations
- Membership expiry uses a simple 30-day-per-month approximation.
- The starter project stores data in local CSV files; it is not a multi-user cloud application.
- It does not process real online payments or store card/bank details.
- Sample names and phone numbers are fictional placeholders.
- This project is an educational prototype, not a production-ready gym billing system.

## Repository structure
```text
upskillcampus/
├── GymManagementSystem.py
├── members.csv
├── payments.csv
├── attendance.csv
├── requirements.txt
├── README.md
├── Internship_Report.pdf
└── outputs/
```

## GitHub repository
After creating the repository named `upskillcampus`, add its real URL here:
[PASTE YOUR ACTUAL GITHUB REPOSITORY URL HERE]
