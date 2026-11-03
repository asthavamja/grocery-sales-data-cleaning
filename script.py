import pandas as pd

def load_data(path):
    df=pd.read_csv(path)
    return df

def clean_data(df):
    skip_cols = ["Contact", "Transaction_ID", "Store_ID", "Date"]
    for column in df.select_dtypes(include=str).columns:
        if column in skip_cols:
            continue
        df[column] = df[column].str.strip().str.title()

    df['Date']=pd.to_datetime(df["Date"],errors="coerce")
    df['Discount_Percent']=df["Discount_Percent"].fillna(0)

    calculated=(df["Quantity_Sold"] * df["Unit_Price"] * (1 - df["Discount_Percent"] / 100)).round(2)
    df["Total_Sales"]=df["Total_Sales"].fillna(calculated)

    df[["Contact_Name", "Email"]] = df["Contact"].str.split("-", n=1, expand=True)
    df["Contact_Name"] = df["Contact_Name"].str.strip().str.title()
    df["Email"] = df["Email"].str.strip().str.lower()

    return df

def validate_data(df):
    calculated = (
        df["Quantity_Sold"] * df["Unit_Price"]
        * (1 - df["Discount_Percent"] / 100)
    ).round(2)
    checks={
        "Quantity <= 0":df["Quantity_Sold"]<=0,
        "Unit Price <= 0":df["Unit_Price"]<=0,
        "bad_rating": df["Customer_Rating"].notna() & ~df["Customer_Rating"].between(1, 5),
        "Invalid Email":~df["Email"].str.match(r"^[\w.]+@[\w.]+\.\w+$"),
        "Contact name differ from employee name" : df["Contact_Name"] != df["Employee_Name"],
        "Discount out of range" : ~df["Discount_Percent"].between(0, 100),
        "Total Sales does not match calculation" : (df["Total_Sales"] - calculated).abs() > 0.02,
    }
    pieces = []
    for reason, mask in checks.items():
        found = df.loc[mask].copy()
        found["Reason"] = reason
        pieces.append(found)

    if pieces:
        all_flagged = pd.concat(pieces)
        if all_flagged.empty:
            print("No validation issues found.")
        else:
            print(all_flagged[["Transaction_ID", "Reason"]])
    return all_flagged


def summarize(df,all_flagged):
    print(f"Total rows: {len(df)}")
    print(f"Total sales: {df['Total_Sales'].sum():,.2f}")
    print(f"Average rating: {df['Customer_Rating'].mean():.2f}")
    print(f"Unrated orders: {df['Customer_Rating'].isna().sum()}")
    print(df.groupby("Store_Location")["Total_Sales"].sum())
    print(df.groupby("Product_Category")["Total_Sales"].sum().sort_values(ascending=False))
    print(df.groupby("Payment_Mode")["Total_Sales"].sum())
    print(f"Return rate: {(df["Returned"] == "Yes").mean() * 100}%")
    print(df["Payment_Mode"].value_counts())

def saved_files(df,all_flagged):
    df.to_csv("cleaned_data.csv", index=False)
    all_flagged.to_csv("flagged_rows.csv", index=False)

def main():
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "grocery_store_data.csv"
    df = load_data(path)
    df = clean_data(df)
    flagged = validate_data(df)
    summarize(df, flagged)
    saved_files(df, flagged)

if __name__ == "__main__":
    main()