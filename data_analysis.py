import matplotlib.pyplot as plt
import pandas as pd
import csv
import re

house_data_fp = 'house_data.csv'

# Read the CSV file into a DataFrame ('df')
# - 'skiprows=1': Skip the first row, which is a header row.
df = pd.read_csv(house_data_fp, header=None, skiprows=1) # 'df' = Dataframe

# Define a function to clean up numerical values by removing decimal points
def clean_number(value):
      return int(value.replace('.',''))

# Apply the 'clean_number' function to the values in the third column of the DataFrame
df[2] = df[2].apply(clean_number)

# Splitting the third column based on '|'
split_columns = df[3].str.split('|', expand=True)

# Creating new columns for each part
df['room_info'] = split_columns[1].str.strip()  # Extracting room information, so we can use regular expression for cleaning
df['size_info'] = split_columns[2].str.strip()  # Extracting size information, so we can use regular expression for cleaning

# Drop the original column containing the extracted information
df.drop(columns=[3], inplace=True)

# Define the file path for the cleaned data CSV file
cleaned_file_path = 'house_data_cleaned.csv'

# Write the cleaned DataFrame to a new CSV file
# - 'index=False': Do not write the DataFrame index to the CSV file.
# - 'header=None': Do not include a header row in the CSV file.
df.to_csv(cleaned_file_path, index=False, header=None)

# Extract numeric values from the 'room_info' column
# str.extract(r'(\d+)').astype(int) | I use the pandas str.extract, to find the sepcific string of the coloumn
# (r'(\d+)'), i denote the string as raw, so backslashes are treated as literal characters. 
# so in the regular expression we, dont end up using them as an escape character
# \d : matches a digit and the '+', tells us that the preceding character is repeated at least once

df['room_numbers'] = df['room_info'].str.extract(r'(\d+)').astype(int) 

# Extract numeric values from the 'size_info' column
df['size_numbers'] = df['size_info'].str.extract(r'(\d+)').astype(int) 

# Scatter plot for house sizes vs. prices
plt.figure(figsize=(10, 8))
plt.scatter(df['size_numbers'], df[2], color='orange', alpha=0.7)
plt.title('House Sizes vs. Prices')
plt.xlabel('Size (m2)')
plt.ylabel('Price (in DKK)')
plt.show() 


