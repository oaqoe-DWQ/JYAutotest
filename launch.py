# -*- coding: utf-8 -*-
__author__ = "zhangxiaoguo"

from airtest.core.api import *
from airtest.cli.parser import cli_setup


def launch():
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=["iOS:///http://127.0.0.1:8100"])
