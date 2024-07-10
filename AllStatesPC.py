import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from tabulate import tabulate

# Add the directory containing HomePage.py to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the necessary data or functions from HomePage
from HomePage import url, headers, href_list

# Print to get the data of the first href
firstPage = href_list[0]
firstPageReq = requests.get(firstPage, headers=headers)

# The main data frame
main_dataFrame = []

# Check if the request was successful
if firstPageReq.status_code == 200:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(firstPageReq.content, 'html.parser')
    # Find the dropdown element for selecting the state
    dropdown = soup.find('select', {'id': 'ctl00_ContentPlaceHolder1_Result1_ddlState'})
    state_options = dropdown.find_all('option')
    
    # Loop through each state option
    for state_option in state_options:
        if state_option['value']:  # Skip the default "Select State" option
            state_value = state_option['value']
            state_name = state_option.text.strip()
            # Construct the URL for fetching results for the current state
            state_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm"
            # Send another GET request to the state-specific URL
            state_response = requests.get(state_url)
            if state_response.status_code == 200:
                # Parse the state-specific page
                state_soup = BeautifulSoup(state_response.content, 'html.parser')
                constituency_dropdown = state_soup.find('select', {'id': 'ctl00_ContentPlaceHolder1_Result1_ddlState'})
                constituency_options = constituency_dropdown.find_all('option')
                for option in constituency_options:
                    if option['value']:  # Skip the default "Select Constituency" option
                        constituency_value = option['value']     # S312
                        constituency_name = option.text.strip()
                        constituencyWise_url = f"https://results.eci.gov.in/PcResultGenJune2024/Constituencywise{constituency_value}.htm"
                        constituency_response = requests.get(constituencyWise_url)
                        if constituency_response.status_code == 200:
                            constituency_soup = BeautifulSoup(constituency_response.content, 'html.parser')
                            title = constituency_soup.find('div', {"class": "page-title"}).find("h2")
                            constituency_info = title.text.strip()
                            constituency_name = constituency_info.split(' - ')[-1].split('(')[0].strip()
                            table = constituency_soup.find('table', {'class': 'table table-striped table-bordered'})
                            if table:
                                headers = [header.text.strip() for header in table.find('thead').find_all('th')]
                                data = []
                                for row in table.find('tbody').find_all('tr'):
                                    row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
                                    data.append(row_data)
                                df = pd.DataFrame(data, columns=headers)
                                df['Constituency Name'] = constituency_name
                                df['State'] = state_name
                                main_dataFrame.append(df)
                            else:
                                print(f"Table Not Found for constituency {constituency_name}")
                        else:
                            print(f"Constituency response failure for {constituency_name}")
            else:
                print(f"State response failure for {state_name}")
else:
    print("First Page request failed. Check HREF List")

# Merge all data frames                                
merged_df = pd.concat(main_dataFrame, ignore_index=True)
merged_df['Serial No.'] = merged_df.reset_index().index + 1


merged_df.to_csv('CSV Files/All_States_PC_electionresults.csv', index=False)

# Display the merged DataFrame
print(tabulate(merged_df, headers='keys', tablefmt='fancy_grid'))
