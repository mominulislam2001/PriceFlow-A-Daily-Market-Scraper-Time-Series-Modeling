import datetime
import time
import os
import glob
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def scrape_market_data(url, start_date, end_date):
    # Set up Chrome web driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open the URL in the browser
        driver.get(url)
        
        try:
            # Handle language selection if needed
            lang_btn = driver.find_element(By.XPATH, "//button[@class='btn btn_lang']")
            lang_btn.click()
            print("Language button clicked successfully.")
        except Exception as lang_err:
            print(f"Language button not found or error: {lang_err}")

        try:
            # Wait for the elements to be clickable
            division_btns = driver.find_elements(By.XPATH, '//button[@class="btn-select w-100 d-block text-left"]')
            helper_btns = driver.find_elements(By.XPATH, '//button[@class="helperButton"]')  
            for i in range(min(5, len(division_btns))):
                division_btns[i].click() 
                helper_btns[i].click()    
            print("Division buttons clicked successfully!")
        except Exception as click_err:
            print(f"Error clicking division buttons: {click_err}")
        
        try:
            # Locate the date input field
            date_elem = driver.find_element(By.XPATH, '//input[@id="__BVID__51"]')
            driver.execute_script("arguments[0].removeAttribute('readonly');", date_elem)
        except Exception as date_err:
            print(f"Date input element not found or error: {date_err}")
            driver.quit()
            return
        
        # Loop through each date from start_date to end_date
        current_date = start_date
        delta = datetime.timedelta(days=1)

        while current_date <= end_date:
            # Clear any existing date
            date_elem.clear()

            # Format the date string
            date_str = current_date.strftime("%Y-%m-%d")

            # Enter the date into the input field
            date_elem.send_keys(date_str)
            
            try:
                # Locate and click the search button
                search_btn = driver.find_element(By.XPATH, "//button[@class='btn mr-2 btn-primary']")
                search_btn.click()
                print(f"Search button clicked for date: {date_str}")

                # Wait for the download button and click it
                time.sleep(10)
                try:
                    download_file_btn = driver.find_element(By.XPATH, "//div[@class='btn btn_add_new']")
                    download_file_btn.click()
                    print(f"Download button clicked for date: {date_str}")
                    
                    
                    
                    
                    
                except Exception as download_err:
                    print(f"Error clicking download button for date {date_str}: {download_err}")

            except Exception as search_err:
                print(f"Search button not found or error: {search_err}")
            
            # Move to the next day
            current_date += delta
        
    except Exception as main_err:
        print(f"Error in main scraping function: {main_err}")

    finally:
        # Close the browser session
        driver.quit()


def rename_xls_to_html(directory):
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Check if the file has a .xls extension
        if filename.endswith(".xls"):
            # Create the new filename with .html extension
            new_filename = filename.replace(".xls", ".html")
            # Construct the full file paths
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

    print("Renaming completed.")


def parse_html_and_convert_to_csv(html_file_path, output_directory):
    # Read HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <th> tags with colspan='7'
    th_tags = soup.find_all('th', colspan='7')
    if len(th_tags) >= 2:
        date_text = th_tags[8].get_text(strip=True).replace('Price Date: ', '')  # Extract the second one
    else:
        date_text = 'Unknown Date'

    # Find the tbody tag
    tbody = soup.find('tbody')

    # Extracting rows and cells
    rows = tbody.find_all('tr')
    table_data = []
    for row in rows:
        row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        row_data.append(date_text)  # Append the date to each row
        table_data.append(row_data)

    # Write data to CSV
    base_filename = os.path.basename(html_file_path)
    csv_filename = base_filename.replace('.html', '.csv')
    csv_file_path = os.path.join(output_directory, csv_filename)
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Serial Number", "Product Group", "Product Name and Description", "Unit Retail", 
            "Retail Price (Tk) Lowest Price - Highest Price", "Unit Wholesale", 
            "Wholesale Price (Tk) Lowest Price - Highest Price", "Price Date"
        ])  # English column names
        writer.writerows(table_data)

    return csv_file_path


def process_all_html_files(input_directory, output_directory):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.html'):
            html_file_path = os.path.join(input_directory, filename)
            csv_file_path = parse_html_and_convert_to_csv(html_file_path, output_directory)
            print(f"CSV file saved at: {csv_file_path}")


def merge_csv_files(input_directory, output_file_path):
    # Initialize an empty list to hold DataFrames
    df_list = []
    
    # Iterate over all files in the input directory
    for file in os.listdir(input_directory):
        if file.endswith('.csv'):
            csv_file = os.path.join(input_directory, file)
            # Read the CSV file and append the DataFrame to the list
            df = pd.read_csv(csv_file)
            df_list.append(df)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    merged_df = pd.concat(df_list, axis=0)
    
    # Save the merged DataFrame to the specified output file path
    merged_df.to_csv(output_file_path, index=False)
    
    print(f"All CSV files merged into: {output_file_path}")


if __name__ == "__main__":
   
    url = "http://service.moa.gov.bd/market-directory/market-daily-price-report"
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    scrape_market_data(url, start_date, end_date)

    directory = "./scrapped_data"
    rename_xls_to_html(directory)

    input_directory = './scrapped_data'
    output_directory = './csv_data_all'
    process_all_html_files(input_directory, output_directory)

    input_directory = './csv_data_all'
    output_file_path = './merged_data/merged_data.csv'
    merge_csv_files(input_directory, output_file_path)