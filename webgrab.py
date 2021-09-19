import requests
from bs4 import BeautifulSoup

URL = "https://aqicn.org/city/usa/kansas/peck/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("div", class_="aqivalue")
results = str(results)
aqi_start=results.find(">")+1
aqi_end=len(results)-6
print(results[aqi_start:aqi_end])

