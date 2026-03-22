# Rearc Data Quest

This project implements a simple AWS-based data pipeline.

## Overview

- Ingests BLS dataset and population API
- Stores data in S3
- Triggers analytics using SQS and Lambda
- Uses AWS CDK for infrastructure

## Design

Pipeline flow - 

Ingestion → S3 → SQS → Analytics

S3 acts as the storage layer.  
SQS decouples ingestion from analytics.  

## Run Locally

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py