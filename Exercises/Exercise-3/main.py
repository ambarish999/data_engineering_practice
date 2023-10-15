import boto3
import gzip
import shutil
import io
from pathlib import Path
from urllib.parse import urlparse, unquote


bucket_name = 'commoncrawl'
key_name = 'crawl-data/CC-MAIN-2022-05/wet.paths.gz'
another_key_name = None


def main():
    # your code here
    s3 = boto3.client('s3')
    first_gz_file = Path('wet.paths.gz')
    second_gz_file = Path('file.txt')

    if not first_gz_file.is_file():

        s3.download_file(Filename='wet.paths.gz', Bucket=bucket_name, Key=key_name)
    else:
        if not second_gz_file.is_file():
            with gzip.open('wet.paths.gz', 'rb') as f_in:
                with open('file.txt', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
    
            with open('file.txt', 'r') as file:
                another_key_name = file.readline()
                filename = unquote(urlparse(another_key_name).path.split('/')[-1])
                print(filename)
                if not Path(filename).is_file():
                    s3.download_file(Filename=filename, Bucket=bucket_name, Key=another_key_name)
                else:
                    if not Path('another_file.txt').is_file():
                        with gzip.open(filename, 'rb') as f_in:
                            with open('another_file.txt', 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    else:
                        with open('another_file.txt', 'r') as file:
                            for line in file.readlines():
                                print(line)
print("")

if __name__ == "__main__":
    main()
