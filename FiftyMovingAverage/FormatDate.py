import pandas as pd
import glob
import os
from datetime import datetime


def convert_date_format(date_str):
    # Define the input and output date formats
    input_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"
    output_format = "%d/%m/%Y"

    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, input_format)

    # Format the datetime object to the desired output format
    return date_obj.strftime(output_format)


# Path to the directory containing the .csv files
directory_path = 'C:\\Users\\91974\\OneDrive\\Documents\\NWorth\\StockData\\'

# Use glob to get all .csv files in the directory
csv_files = glob.glob(os.path.join(directory_path, "*.csv"))

# Process each file
for file_path in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check if 'Date' column exists
    if 'Date' in df.columns:
        # Apply the date conversion to each element in the 'Date' column
        df['Date'] = df['Date'].apply(convert_date_format)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

print("Date conversion completed for all files.")
