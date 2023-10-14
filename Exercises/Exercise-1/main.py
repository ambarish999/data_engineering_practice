import requests
import os
# not needed when running in Docker.
from install import install
import io
import zipfile
from urllib.parse import urlparse, unquote
# not needed when running in Docker. import directly.
try:
    import validators
except ImportError as e:
    install("validators")

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]




def main():
    # create directory `downloads` if it doesn't exist
    try:
        os.mkdir('/downloads')
    except FileExistsError:
        print("Directory already exists!")

    
    for uri in download_uris:
        if validators.url(uri):
            try:
                # the first `.split()` gets the filename alongwith the .zip extension
                # the second `.split()` gets the filename without the extension which is
                # the name the saved file will have.
                filename = unquote(urlparse(uri).path.split('/')[-1].split('.')[0])
                r = requests.get(uri)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(f'/downloads/{filename}')
            except Exception as e:
                print("Some error occurred as follows-")
                print("Error: ", e)
        else:
            print(f"This URL {uri} is not valid!")


if __name__ == "__main__":
    main()
