# Copyright (c) <2018>, Ethan <ipvedaily@gmail.com>
# Copyright (c) <2018>, Eef Top <eeftop1994@gmail.com>
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import json


class Settings:

    def __init__(self, settings_file='settings.json'):
        with open(settings_file) as f:
            settings = json.load(f)
        self.channels = settings['channels']
        self.servers = settings['servers']
        self.ranks = settings['ranks']
        self.bot_only_channel = settings['bot-only-channel']
        self.bot_channel = settings['bot-channel']
