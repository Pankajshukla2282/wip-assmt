#!/usr/bin/env python3

from aws_cdk import core

from announce.announce_stack import AnnounceStack


app = core.App()
AnnounceStack(app, "announce")

app.synth()
