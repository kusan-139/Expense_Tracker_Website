
import pandas as pd

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.drop_duplicates()
    df = df.dropna(subset=['Date','Amount','Category','Type'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Category'] = df['Category'].astype(str).str.strip().str.title()
    df['Type'] = df['Type'].astype(str).str.strip().str.title()
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.day_name()
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    clean_data("data/expenses.csv", "data/cleaned_expenses.csv")
