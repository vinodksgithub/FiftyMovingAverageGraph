import os
import pandas as pd
import matplotlib.pyplot as plt


def rename(folder_path):
    # Iterate over each file in the directory
    for file_name in os.listdir(folder_path):
        # Check if the file name matches the pattern
        if file_name.endswith('.csv'):
            # Split the file name to extract the base name before the first parenthesis
            base_name = file_name.split(' (')[0]

            # Construct the new file name
            new_file_name = base_name + '.csv'

            # Construct full file paths
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {file_name} -> {new_file_name}')


# Directory containing the CSV files
folder_path = 'C:\\Users\\91974\\OneDrive\\Documents\\NWorth\\StockData\\'

#rename(folder_path)

# Initialize a list to store dataframes
stock_data_list = []

# Read each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Read the CSV file
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

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
plt.show()
