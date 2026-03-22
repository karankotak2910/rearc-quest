import json
import re
import requests
import boto3
import re

from config import BLS_URL, POPULATION_API, HEADERS, BUCKET_NAME

s3 = boto3.client("s3")

import re

def list_files():

    res = requests.get(BLS_URL, headers=HEADERS)
    print("Status:", res.status_code)
    res.raise_for_status()
    matches = re.findall(r'href="([^"]+)"', res.text, re.IGNORECASE)
    files = []
    for m in matches:
        # get filename from full path
        name = m.split("/")[-1]
        if name.startswith("pr."):
            files.append(name)

    files = list(set(files))
    print(f"Found {len(files)} files:", files)

    return files

# def list_files():
#     return ["pr.data.0.Current"]

def delete_removed_files(source_files):

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="bls/"
    )

    existing = [
        obj["Key"].split("/")[-1]
        for obj in response.get("Contents", [])
    ]

    to_delete = set(existing) - set(source_files)

    for f in to_delete:
        key = f"bls/{f}"
        print(f"Deleting: {key}")
        s3.delete_object(Bucket=BUCKET_NAME, Key=key)

def upload_file(file):

    key = f"bls/{file}"
    url = BLS_URL + file

    print(f"Uploading (overwrite): {file}")

    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=res.content
    )


def sync_bls():

    files = list_files()

    for f in files:
        upload_file(f)

    delete_removed_files(files)


def ingest_population():
    res = requests.get(POPULATION_API)
    res.raise_for_status()

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="population/population.json",
        Body=json.dumps(res.json())
    )


def run():
    print("ingestion started")
    sync_bls()
    ingest_population()
    print("ingestion done")


def handler(event, context):
    run()