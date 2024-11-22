import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Get the current working directory (where your script is located)
current_dir = os.getcwd()

# Step 1: Run the Python scripts located in the same folder
os.system(f'python "{os.path.join(current_dir, "2023offense.py")}"')
os.system(f'python "{os.path.join(current_dir, "2023defense.py")}"')

# Step 2: Scrape data from pro-football-reference.com
url = "https://www.pro-football-reference.com/"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the table with id 'scores'
    scores_table = soup.find('table', {'id': 'scores'})
    if scores_table:
        # Convert the table into a DataFrame
        scores_df = pd.read_html(str(scores_table))[0]
        print("Data successfully scraped from pro-football-reference.com")
    else:
        print("No table found with id 'scores'")
        scores_df = None
else:
    print(f"Failed to retrieve data from {url}")
    scores_df = None

# Step 3: Copy data from CSVs to Excel tabs
file_path = os.path.join(current_dir, "nflgamedaymodel.xlsx")

# Load the entire workbook
with pd.ExcelFile(file_path, engine="openpyxl") as xls:
    all_sheets = {sheet_name: pd.read_excel(xls, sheet_name) for sheet_name in xls.sheet_names}

# Overwrite or add the offense and defense data
all_sheets['offense'] = pd.read_csv(os.path.join(current_dir, "nfl_2023__offense_stats.csv"))
all_sheets['defense'] = pd.read_csv(os.path.join(current_dir, "nfl_2023__defense_stats.csv"))

# Step 4: Clear the content of Sheet2 and add new data if available
if scores_df is not None:
    # Clear Sheet2 by creating a blank DataFrame or removing it
    all_sheets['Sheet2'] = scores_df

# Step 5: Save the updated workbook
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for sheet_name, data in all_sheets.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Data successfully written to Excel.")

# Step 6: Open the Excel file
os.startfile(file_path)
