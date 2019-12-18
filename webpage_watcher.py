import requests
import hashlib
import time
import io
import os.path
import boto3
from os.path import expanduser
WEB_ADDRESS = "https://support.apple.com/en-us/HT201222"
LOCAL_PATH = expanduser("~") + "/local_copy.html"
TEMP_PATH = expanduser("~") +  "/temp_copy.html"
BUCKET = "zimperium-interview-bucket"
RECENT_KEY = "LATEST_FILE"
ACCESS_KEY = "AKIAUFARHWWAV6XYUXK6"
SECRET_KEY = "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"


def download_file(file_name, file_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3.download_file(BUCKET, file_name, file_path)


def upload_file(file_key, file_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    data = open(file_path, "rb")
    s3.upload_fileobj(data, BUCKET, file_key)
    data.close()


def auth_local_copy():
    file_exists = os.path.isfile(LOCAL_PATH)
    if file_exists:
            os.remove(LOCAL_PATH)
    download_file(RECENT_KEY, LOCAL_PATH)


def running_loop():
    while True:
        # TODO:Try
        new_page = requests.get(WEB_ADDRESS)
        new_page_content = new_page.text

        local_file = io.open(LOCAL_PATH, mode='r', encoding="utf-8")
        local_contents = local_file.read()
        local_file.close()

        if local_contents == new_page_content:
            time.sleep(60)
        else:
            current_time = time.strftime("%Y_%m_%d_%H_%M_%S_", time.gmtime())
            md5_hash_func = hashlib.md5()
            md5_hash_func.update(new_page_content.encode("UTF-8"))
            hashed_string = md5_hash_func.hexdigest()
            key_string = current_time + hashed_string
            os.remove(LOCAL_PATH)
            new_local_file = io.open(LOCAL_PATH, mode="w", encoding="utf-8")
            new_local_file.write(new_page_content)
            new_local_file.close()

            upload_file(key_string, LOCAL_PATH)
            upload_file(RECENT_KEY, LOCAL_PATH)



def main():
    auth_local_copy()
    running_loop()


main()



