import requests
import pandas as pd
import os

# API URL and Access Key
api_url = 'https://api.aviationstack.com/v1/flights?access_key=86f678a3dd155cafcd7a38906c522172'

# Fetch data from API
response = requests.get(api_url)

# Check if the response is successful
if response.status_code == 200:
    # If successful, try to parse JSON
    try:
        # Extract data
        data = response.json().get('data', [])
        
        if not data:
            print("No data found in the API response.")
        else:
            # Convert to DataFrame
            new_data_df = pd.json_normalize(data)

            # Excel file name
            excel_file = 'C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Aviation_Report/Aviation_Data.xlsx'

            # Check if file exists
            if os.path.exists(excel_file):
                # Load existing data
                existing_df = pd.read_excel(excel_file)

                # Define the column(s) that serve as unique identifiers
                unique_columns = ['flight.number']  # Replace with actual unique fields from your data

                # Merge data: Replace rows with matching keys and add new rows
                updated_df = pd.concat([existing_df, new_data_df]).drop_duplicates(subset=unique_columns, keep='last')

                # Save updated data back to CSV
                updated_df.to_excel(excel_file, index=False)
                print(f"Data updated in {excel_file}.")
            else:
                # Save new data to CSV
                new_data_df.to_excel(excel_file, index=False)
                print(f"Data saved to {excel_file}.")
    except Exception as e:
        print(f"Error decoding JSON: {e}")
else:
    # If response failed, print the error code and message
    print(f"Error: Unable to fetch data. Status code {response.status_code}")
    print(f"Response text: {response.text}")
