import requests
from bs4 import BeautifulSoup
import pandas as pd
from HomePage import href_list,url,headers;


#print the get the data of the first href
AssemblyElectionsPage = href_list[1]
AssemblyElectionsPageReq = requests.get(AssemblyElectionsPage,headers=headers)


if AssemblyElectionsPageReq.status_code == 200:
    AssemblyElectionsPagesoup = BeautifulSoup(AssemblyElectionsPageReq.content, 'html.parser')
    main_tag = AssemblyElectionsPagesoup.find('main')

    # Find all a tags within the main tag
    href_list = []
    if main_tag:
        links = main_tag.find_all('a')
        hrefs = [link.get('href') for link in links]

        # Print all hrefs
        for href in hrefs:
            if href and href not in href_list: 
                href_list.append(href)
                # print(href)
    else:
        print("Main tag not found")
    


# Loop in through the href list and gather the information
for i in href_list:
    assemblyStateURL = f"https://results.eci.gov.in/AcResultGenJune2024/{i}"
    assemblyStateReq = requests.get(assemblyStateURL,headers=headers)
    
    if assemblyStateReq.status_code == 200:
        assemblyStateSoup = BeautifulSoup(assemblyStateReq.content,"html.parser")
        state_tag = assemblyStateSoup.find('div', class_='page-title').find('strong')
        state_name = state_tag.text.strip() if state_tag else "N/A"
        party_boxes = assemblyStateSoup.find_all('div', class_='grid-box')

        party_data = []
        for box in party_boxes:
            party_name = box.find('h4').text.strip()
            vote_count = box.find('h2').text.strip()
            party_data.append({'Party': party_name, 'Votes': vote_count})

        # Create a Pandas DataFrame
        df = pd.DataFrame(party_data)
        csvName = f"{state_name}Assembly Election.csv"
        df.to_csv(csvName, index=False)

        


    
