import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def custom_date_parser(date_str):
    # Define the input date format matching the example provided
    input_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, input_format)

    # Return the date object
    return date_obj


# Directory containing the CSV files
folder_path = 'C:\\Users\\91974\\OneDrive\\Documents\\NWorth\\StockData\\'

# Initialize a list to store dataframes
stock_data_list = []

# Read each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Read the CSV file with custom date parser
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path, parse_dates=['Date'], date_parser=custom_date_parser, index_col='Date')

        # Append the dataframe to the list
        stock_data_list.append(data)

# Merge all dataframes on the Date index
all_data = pd.concat(stock_data_list, axis=1,
                     keys=[os.path.splitext(file_name)[0] for file_name in os.listdir(folder_path) if
                           file_name.endswith('.csv')])

# Calculate the average closing price across all stocks
average_close = all_data.xs('Close', level=1, axis=1).mean(axis=1)

# Calculate the 50-day moving average of the average closing price
average_close_50_ma = average_close.rolling(window=50).mean()

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(average_close.index, average_close, label='Average Close')
plt.plot(average_close_50_ma.index, average_close_50_ma, label='50-Day MA of Average Close', color='orange')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Average Stock Price and 50-Day Moving Average')
plt.legend()
plt.grid(True)

# Format the x-axis to display the date correctly
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))
plt.gcf().autofmt_xdate()

plt.show()
