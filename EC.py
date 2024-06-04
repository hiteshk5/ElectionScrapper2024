#%%
# Importing required libraries
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore")

#%%
# Set up the WebDriver
chrome_driver_path = r'chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
try:
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
except:
    s = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(options=chrome_options, service=s) 

# Navigate to the webpage
url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'
driver.get(url)

# Function to scrape the data
def scrape_data():
    driver.refresh()
    time.sleep(5)  # Allow some time for the page to load
    table = driver.find_element(By.CLASS_NAME, 'table')

    # Extract headers
    headers = [header.text for header in table.find_elements(By.XPATH, './/thead//th')]

    # Extract rows
    rows = table.find_elements(By.XPATH, './/tbody//tr')
    data = []
    for row in rows:
        columns = row.find_elements(By.XPATH, './/td')
        data.append([column.text for column in columns])

    return data

# Function to clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Loop to refresh every minute
try:
    while True:
        data = scrape_data()
        
        # Convert to DataFrame
        seats = pd.DataFrame(data, columns=['Party', 'Won', 'Leading', 'Total'])

        # Format as int
        seats['Won'] = seats['Won'].astype(int)
        seats['Leading'] = seats['Leading'].astype(int)
        seats['Total'] = seats['Total'].astype(int)

        nda = ['Bharatiya Janata Party', 'Telugu Desam - TDP', 'Janata Dal (United)', 'Shiv Sena - SHS', 
               'Pattali Makkal Katchi', 'Lok Janshakti Party', 'Nationalist Congress Party', 
               'Bharath Dharma Jana Sena', 'Janata Dal (Secular)', 'Tamil Maanila Congress', 
               'Amma Makkal Munnetra Kazhagam', 'Apna Dal (Soneylal)', 'Asom Gana Parishad', 
               'Jana Sena Party', 'National People\'s Party', 'Rashtriya Lok Dal', 'All Jharkhand Students Union', 
               'Hindustani Awam Morcha', 'Naga Peoples Front - NPF', 'Nationalist Democratic Progressive Party', 
               'Rashtriya Lok Morcha', 'Rashtriya Samaj Paksha', 'Suheldev Bharatiya Samaj Party', 
               'United People’s Party, Liberal - UPPL']
        
        india = ['Indian National Congress', 'Samajwadi Party', 'Rashtriya Janata Dal', 'Dravida Munnetra Kazhagam',
                 'Shiv Sena (Uddhav Balasaheb Thackrey)', 'Nationalist Congress Party (Sharadchandra Pawar)', 
                 'Aam Aadmi Party', 'Communist Party of India (Marxist)', 'Jharkhand Mukti Morcha', 
                 'Communist Party of India', 'Communist Party of India (Marxist–Leninist) Liberation',
                 'Jammu & Kashmir National Conference', 'Vikassheel Insaan Party', 'Viduthalai Chiruthaigal Katchi', 
                 'All India Forward Bloc', 'All India Trinamool Congress - AITC', 'Assam Jatiya Parishad', 
                 'Bharat Adivasi Party', 'Indian Union Muslim League', 'Kongunadu Makkal Desia Katchi', 
                 'Marumalarchi Dravida Munnetra Kazhagam', 'Rashtriya Loktantrik Party', 'Kerala Congress', 
                 'Kerala Congress (M)']
        
        independent = ['Independent']

        for i in range(len(seats)):
            party_name = seats['Party'][i].strip().casefold()
            if any(x.casefold() in party_name for x in nda):
                seats['Party'][i] = 'NDA'
            elif any(x.casefold() in party_name for x in independent):
                seats['Party'][i] = 'Independent'
            elif any(x.casefold() in party_name for x in india):
                seats['Party'][i] = 'I.N.D.I.A'
            else:
                print(f"Other: {seats['Party'][i]}")
                seats['Party'][i] = 'Others'
        
        seats = seats.groupby('Party').sum()
        seats.sort_values(by='Leading', ascending=False, inplace=True)
        
        # Clear terminal
        clear_terminal()
        
        # Print ASCII table
        print(tabulate(seats, headers='keys', tablefmt='grid'))
        print("Total seats: ", seats['Total'].sum())
        
        # Wait for one minute before refreshing
        time.sleep(60)

except KeyboardInterrupt:
    # Gracefully close the WebDriver on interruption
    print("Script terminated by user.")
    driver.quit()
    # Exit the code
    exit()