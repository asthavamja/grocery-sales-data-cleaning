# Grocery Sales Data Cleaning

A Python and pandas project that cleans grocery-store sales data, checks for common data-quality issues, prints sales summaries, and saves the results to CSV files.

## Features

- Cleans text fields and converts dates to datetime values.
- Fills missing discounts with `0` and calculates missing total sales.
- Splits the `Contact` field into contact name and email.
- Flags invalid quantities, prices, ratings, emails, discounts, contact names, and sales totals.
- Prints summary statistics and sales breakdowns.

## Requirements

- Python 3.9 or later
- pandas

Install pandas:

```powershell
python -m pip install pandas
```

## Run

From this project folder, run the script with the included sample data:

```powershell
python script.py
```

To use a different CSV file, provide its path:

```powershell
python script.py path\to\your_data.csv
```

The input CSV should contain the columns used by the script, including `Date`, `Discount_Percent`, `Quantity_Sold`, `Unit_Price`, `Total_Sales`, `Contact`, `Customer_Rating`, `Employee_Name`, `Transaction_ID`, `Store_Location`, `Product_Category`, `Payment_Mode`, and `Returned`.

## Output

The script writes these files in the current working directory:

- `cleaned_data.csv` — the cleaned dataset.
- `flagged_rows.csv` — rows that failed one or more validation checks, with a `Reason` column.

Running the script again overwrites these output files.
