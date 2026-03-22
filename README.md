# Rearc Data Quest

## Overview

This project implements a simple end-to-end data pipeline on AWS.
The goal was to ingest publicly available datasets, store them in S3, and run basic analytics in an automated manner.

The pipeline pulls:

* BLS productivity dataset
* US population data via API

Both datasets are processed and stored in S3, and then used for downstream analytics.

---

## Architecture

High-level flow:

EventBridge -> Ingest Lambda -> S3 -> SQS -> Analytics Lambda

* **EventBridge** is used to schedule ingestion
* **Ingest Lambda** fetches data and uploads to S3
* **S3** acts as the storage layer
* **SQS** decouples ingestion from analytics
* **Analytics Lambda** reads from S3 and computes metrics

This keeps the pipeline loosely coupled and easy to extend.

---

## Key Decisions

* Kept ingestion and analytics separate using SQS to avoid tight coupling
* Used Lambda for simplicity and serverless execution
* Used environment variables instead of hardcoding configuration
* Used Pandas for analytics (handled via Lambda layer due to dependency constraints)
* Focused on keeping the solution simple, readable, and production-friendly

---

## Running Locally

Rearc team can run the pipeline locally (without AWS) for quick validation:

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

This will:

* Fetch data
* Store locally
* Run analytics

---

## Deployment

Infrastructure is defined using AWS CDK.

```bash
cd infrastructure
cdk bootstrap
cdk deploy
```

After deployment:

* Ingestion runs via EventBridge schedule
* Analytics is triggered via SQS

---

## Output Validation

* Data is stored in S3 under `bls/` and `population/`
* Analytics results can be verified in CloudWatch logs
* The pipeline can be re-run safely without duplication issues

---

## Challenges Faced

* Handling BLS data access restrictions (403/406 issues)
* Packaging Pandas/Numpy for Lambda (resolved using Lambda layers)
* Managing IAM permissions between services
* Ensuring compatibility between local and Lambda environments

---

## Acknowledgement

While building this project, I referred to official documentation and used AI-assisted tools (such as ChatGPT) for troubleshooting specific issues (e.g., pandas dependency packaging and AWS CDK configuration).
All design decisions, implementation, and debugging were carried out by me.

---

## Notes

The focus of this project was to keep things simple and production-oriented, rather than adding unnecessary complexity. The same structure can be extended for larger datasets or additional transformations.
