import requests
import csv
from bs4 import BeautifulSoup

# initialize a list to store all visited links
visited_links = []
spot_links = []
rows = []


def scrape(site):

    page_to_scrape = requests.get(site).text
    soup = BeautifulSoup(page_to_scrape, "lxml")
    links = soup.find_all('a')

# get all links
    for link in links:
        href = link.get('href')
        #TODO: ten bool niepotrzebny chyba
        if bool(href) and href.startswith("https://surfing-waves.com/atlas/europe/"):
        
            is_spot = href.find("/spot/")
            is_action = href.find("action")
            
            if is_spot > -1 and is_action == -1:
                if href not in spot_links:
                    spot_links.append(href)
            if href not in visited_links:
                visited_links.append(href)
                scrape(href)

def get_coordinates(link_list):
    link_set= set(link_list)
    
    
    for link in link_set:
        row= []
        page_content = requests.get(link).text

        # parse the html content

        page_soup = BeautifulSoup(page_content, "lxml")

        # find all meta tags with the given itemprop attributes
        latitude_tags = page_soup.find_all('meta', attrs={'itemprop': 'latitude'})
        longitude_tags = page_soup.find_all('meta', attrs={'itemprop': 'longitude'})

        # extract the latitude and longitude strings
        if bool(latitude_tags) and bool(longitude_tags):
            latitude = latitude_tags[0]['content']
            longitude = longitude_tags[0]['content']
            place_raw = link.split('/')

            # print the latitude and longitude strings
            country = place_raw[5].replace("_"," ").title()
            beach = place_raw[-1].replace(".html","")
            beach = beach.replace("_"," ").title()
            row.append(country)
            row.append(beach)
            row.append(latitude)
            row.append(longitude)
            rows.append(row)
   

            
if __name__ =="__main__":
    site = "https://surfing-waves.com/atlas/europe.html"
    scrape(site)
    get_coordinates(spot_links)
    with open('myfala.csv', 'w') as f:
        writer =csv.writer(f)
        writer.writerows(rows)