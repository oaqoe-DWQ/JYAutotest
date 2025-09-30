#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime

class TimeManager:
    _instance = None
    _timestamp = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeManager, cls).__new__(cls)
            # 初始化时间戳，格式：2025-01-02-16_50_02
            cls._timestamp = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        return cls._instance

    @classmethod
    def get_timestamp(cls):
        if cls._timestamp is None:
            cls._instance = cls()
        return cls._timestamp