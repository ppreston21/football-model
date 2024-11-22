import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define the URL of the web page you want to scrape
url = "https://www.pro-football-reference.com/years/2023/opp.htm#team_stats"

# Send an HTTP GET request to the URL
driver.get(url)

# Find the table body containing the team statistics using XPath
table_body = driver.find_element(By.XPATH, '//*[@id="team_stats"]/tbody')

# Get the HTML content of the table body
table_body_html = table_body.get_attribute("outerHTML")

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(table_body_html, "html.parser")

# Extract the rows and cells from the table
rows = soup.find_all("tr")
data = []
for row in rows:
    cells = row.find_all(["th", "td"])
    row_data = [cell.get_text(strip=True) for cell in cells]
    data.append(row_data)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data[1:], columns=data[0])

# Save the data to a CSV file
df.to_csv("nfl_2023__defense_stats.csv", index=False)

print("Data has been successfully scraped and saved as 'nfl_2023__defense_stats.csv'.")

# Close the WebDriver
driver.quit()
