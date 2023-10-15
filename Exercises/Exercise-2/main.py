import requests
import pandas as pd
from helpers.install import install
import validators
from urllib.parse import urljoin
import io

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("bs4")

url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
timestamp = '2022-02-07 14:03'
column_name = 'Last Modified'
column_index = 1 # 0-based indexing

pandas_column = 'HourlyDryBulbTemperature'


def main():
    # your code here
    if validators.url(url):
        page = requests.get(url)
        target_url = None

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")

            table = soup.find("table")

            if table:
                rows = table.find_all('tr')
                table_data = []

                for row in rows:
                    # headers = row.find_all('th')
                    values = row.find_all('td')
                    row_data = []

                    for value in values:
                        if value.find('a'):
                            a_tag = value.find('a')
                            row_data.append(a_tag.get('href'))
                        else:
                            row_data.append(value)
                    table_data.append(row_data)


                target_data = filter(lambda cell_data: cell_data[column_index] == timestamp, table)
                target_url = urljoin(url, target_data[0])
            else:
                print("Nothing in the table!")
        else:
            print("Request did not return anything!")
        
        if validators.url(target_url):
            csv = requests.get(target_url)

            if csv.status_code == 200:
                df = pd.read_csv(io.StringIO(csv.text))

                max_hr_dry_bulb_temp = df[df[pandas_column] == df[pandas_column].max()]

                print(max_hr_dry_bulb_temp.head())
            else:
                print("Download URL request didn't return anything!")
        else:
            print("Not a valid URL for download!")
    else:
        print("Requested URL is not valid!")

print("")

if __name__ == "__main__":
    main()
