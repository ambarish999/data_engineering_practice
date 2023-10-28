import boto3
import os
import pandas as pd
import json


def main():
    for root, dirs, files in os.walk('data'):
        json_files = list(filter(lambda file: file.endswith('.json'), files))
        print(json_files)
        for json_file in json_files:
            print(f"{root}\{json_file}")
            with open(f"{root}\{json_file}") as file:
                data = json.load(file)
                # normalize doesn't seem to be working for the example `{"type":"Point","coordinates":[-99.9,16.88333]}` value
                # beyond the first level i.e., geolocation.type: "Point" geolocation.coordinates: [lat, long]
                json_file_normal = pd.json_normalize(data, max_level=3)
                json_file_normal.to_csv(f"{root}\{json_file.replace('.json', '.csv')}", index=False)


if __name__ == "__main__":
    main()
