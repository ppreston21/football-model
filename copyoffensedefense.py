import os
import pandas as pd

# Get the current working directory (where your script is located)
current_dir = os.getcwd()

# Step 1: Run the Python scripts located in the same folder
os.system(f'python "{os.path.join(current_dir, "2023offense.py")}"')
os.system(f'python "{os.path.join(current_dir, "2023defense.py")}"')

# Step 2 & 3: Copy data from CSVs to Excel tabs
file_path = os.path.join(current_dir, "nflgamedaymodel.xlsx")

# Load the entire workbook
with pd.ExcelFile(file_path, engine="openpyxl") as xls:
    all_sheets = {sheet_name: pd.read_excel(xls, sheet_name) for sheet_name in xls.sheet_names}

# Overwrite or add the offense and defense data
all_sheets['offense'] = pd.read_csv(os.path.join(current_dir, "nfl_2023__offense_stats.csv"))
all_sheets['defense'] = pd.read_csv(os.path.join(current_dir, "nfl_2023__defense_stats.csv"))

# Save the updated workbook
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for sheet_name, data in all_sheets.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

# Step 4: Open the Excel file
os.startfile(file_path)
