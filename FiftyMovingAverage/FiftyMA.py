import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def custom_date_parser(date_str):
    # Define the input date format matching the example provided
    input_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, input_format)

    # Return the date in the desired format dd-mm-yyyy
    return date_obj


# Load your data
file_path = 'C:\\Users\\91974\\OneDrive\\Documents\\NWorth\\StockData\\ACE (20240618000000000 _ 20231228000000000).csv'
data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date', date_parser=custom_date_parser)

# Calculate 50-day moving average
data['50-Day MA'] = data['Close'].rolling(window=50).mean()

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Close')
plt.plot(data.index, data['50-Day MA'], label='50-Day MA', color='orange')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Prices with 50-Day Moving Average')
plt.legend()
plt.grid(True)

# Format the x-axis to display the date correctly
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))
plt.gcf().autofmt_xdate()

plt.show()
