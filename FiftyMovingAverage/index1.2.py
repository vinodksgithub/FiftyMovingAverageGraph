import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, CheckButtons
from datetime import datetime


# download all the required data files for all stocks and run programme
# no changes needed to downloaded files

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
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(average_close.index, average_close, label='Average Close')
ax.plot(average_close_50_ma.index, average_close_50_ma, label='50-Day MA of Average Close', color='orange')

ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Average Stock Price and 50-Day Moving Average')
ax.legend()
ax.grid(True)

# Format the x-axis to display the date correctly
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))
fig.autofmt_xdate()

# Add a crosshair cursor
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

# Add a checkbox to enable/disable the crosshair
rax = plt.axes([0.8, 0.01, 0.1, 0.05])
check = CheckButtons(rax, ['Crosshair'], [True])


def toggle_cursor(label):
    if label == 'Crosshair':
        cursor.visible = not cursor.visible
        plt.draw()


check.on_clicked(toggle_cursor)

plt.show()
