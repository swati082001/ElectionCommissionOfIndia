import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from HomePage import href_list,url,headers;


#print the get the data of the first href
firstPage = href_list[0]
firstPageReq = requests.get(firstPage,headers=headers)


if firstPageReq.status_code == 200:
    firstPagesoup = BeautifulSoup(firstPageReq.content, 'html.parser')

    scripts = firstPagesoup.find_all('script')
    print("\nNumber of <script> tags found:", len(scripts))
    if len(scripts) >= 7:
        script_7 = scripts[6].string
        # with open("scrappedData/scripts.html", "w") as filedata:
        #     filedata.write(f"Script 7:\n{script_7}\n")


        # Extract party names and number of seats
        start_xValues = script_7.find("var xValues = [") + len("var xValues = [")
        end_xValues = script_7.find("];", start_xValues)
        xValues_str = script_7[start_xValues:end_xValues]
        party_names = [x.strip().strip("'") for x in xValues_str.split(',')]

        start_yValues = script_7.find("var yValues = [") + len("var yValues = [")
        end_yValues = script_7.find("];", start_yValues)
        yValues_str = script_7[start_yValues:end_yValues]
        seats = [int(x.strip()) for x in yValues_str.split(',')]

        # Create a pandas DataFrame
        df = pd.DataFrame({
            'Party': party_names,
            'Seats': seats
        })

        print(df)
        df.to_csv('party_seats.csv', index=False)

    else:
        print("Less than 7 <script> tags found on the page.")





# Extract the data from for party names and vote shares using regex
if firstPageReq.status_code == 200:
    soup = BeautifulSoup(firstPageReq.content, 'html.parser')
    
    # Find all script tags
    script_tags = soup.find_all('script')
    
    # Initialize variables to store xValues
    xValues_2 = None

    # Search for the script tag containing xValues
    for script_tag in script_tags:
        if "var xValues = ['" in str(script_tag):
            script_content = str(script_tag.string)
            # Find positions of both sets of xValues
            start_pos_1 = script_content.find("var xValues = ['") + len("var xValues = ['")
            end_pos_1 = script_content.find("'];", start_pos_1)
            
            start_pos_2 = script_content.find("var xValues = ['", end_pos_1) + len("var xValues = ['")
            end_pos_2 = script_content.find("];\r\n", start_pos_2)
            
            # Extract the second set of xValues
            xValues_str_2 = script_content[start_pos_2:end_pos_2]
            xValues_2 = [x.strip().strip("'") for x in xValues_str_2.split(',')]
            
            print("Second set of xValues:")
            print(xValues_2)
            
            party_codes = [entry.split('{')[0] for entry in xValues_2 if entry.strip()]  # extract party code
            vote_shares = [entry.split('{')[1][:-1] for entry in xValues_2 if entry.strip()]  # extract vote share and remove the trailing '}'

            # Creating a DataFrame
            df = pd.DataFrame({
                'Party Code': party_codes,
                'Vote Share': vote_shares
            })

            print(df)
            df.to_csv('party_vote_share.csv', index=False)
        
    else:
        print("Script tag containing xValues not found.")
else:
    print(f"Failed to retrieve page: Status code {firstPageReq.status_code}")
    