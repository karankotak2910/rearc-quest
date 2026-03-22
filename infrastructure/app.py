#!/usr/bin/env python3

import aws_cdk as cdk
from rearc_pipeline.rearc_pipeline_stack import RearcPipelineStack

app = cdk.App()
RearcPipelineStack(app, "RearcPipelineStack")

app.synth()