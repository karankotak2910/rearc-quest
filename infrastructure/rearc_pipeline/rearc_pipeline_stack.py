from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_s3_notifications as s3n,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda_event_sources as event_sources,
)

from constructs import Construct

class RearcPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pandas_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "PandasLayer",
            "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p314-pandas:14"
        )

        bucket = s3.Bucket(self, "DataBucket")

        queue = sqs.Queue(
            self,
            "Queue",
            visibility_timeout=Duration.seconds(300)
        )

        ingest = _lambda.Function(
            self,
            "Ingest",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="ingest.handler",
            code=_lambda.Code.from_asset("../src"),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            },
            timeout=Duration.seconds(300),
        )
        bucket.grant_read_write(ingest)

        analytics = _lambda.Function(
            self,
            "Analytics",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="analytics.handler",
            code=_lambda.Code.from_asset("../src"),
            layers=[pandas_layer],
            environment={
                "BUCKET_NAME": bucket.bucket_name
            },
            timeout=Duration.seconds(300),
        )
        bucket.grant_read_write(analytics)

        bucket.grant_read_write(ingest)
        bucket.grant_read(analytics)

        queue.grant_consume_messages(analytics)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SqsDestination(queue),
        )

        analytics.add_event_source(
            event_sources.SqsEventSource(queue)
        )

        rule = events.Rule(
            self,
            "Daily",
            schedule=events.Schedule.rate(Duration.days(1)),
        )

        rule.add_target(targets.LambdaFunction(ingest))