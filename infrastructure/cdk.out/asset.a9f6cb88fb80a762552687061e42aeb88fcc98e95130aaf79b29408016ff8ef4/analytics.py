import json
import boto3
import pandas as pd
from io import BytesIO

from config import BUCKET_NAME

s3 = boto3.client("s3")


def load_population():
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key="population/population.json"
    )

    data = json.loads(obj["Body"].read())
    return pd.DataFrame(data["data"])


def load_bls():
    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key="bls/pr.data.0.Current"
    )

    df = pd.read_csv(BytesIO(obj["Body"].read()), sep="\t")

    df.columns = df.columns.str.strip()

    df["series_id"] = df["series_id"].str.strip()
    df["period"] = df["period"].str.strip()

    return df


def population_stats(pop):
    df = pop[(pop["Year"] >= 2013) & (pop["Year"] <= 2018)]

    print("mean:", df["Population"].mean())
    print("std:", df["Population"].std())


def best_year(bls):
    print(bls)
    df = (
        bls.groupby(["series_id", "year"])["value"]
        .sum()
        .reset_index()
    )

    best = (
        df.sort_values(["series_id", "value"], ascending=[True, False])
        .groupby("series_id")
        .head(1)
    )
    print(best["series_id"].count())
    print(best.head())


def join_data(bls, pop):
    df = bls[
        (bls["series_id"] == "PRS30006032") &
        (bls["period"] == "Q01")
    ]

    joined = df.merge(pop, left_on="year", right_on="Year", how="inner")
    print(bls["year"].dtype)
    print(pop["Year"].dtype)
    print(joined)


def run():
    pop = load_population()
    print("bls started")
    bls = load_bls()

    population_stats(pop)
    best_year(bls)
    join_data(bls, pop)


def handler(event, context):
    run()