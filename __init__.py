# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Stanisław Borodziuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
# Requires spotpy package: https://pypi.org/project/spotipy/
#
# Changelog:
# [2023-06-17] Initial version


PLUGIN_NAME = "Streaming Metadata"
PLUGIN_AUTHOR = "Stanislaw Borodziuk"
PLUGIN_DESCRIPTION = "Get metadata from streaming services"
PLUGIN_VERSION = "0.1.0"
PLUGIN_API_VERSIONS = ["2.0", "2.1", "2.2"]
PLUGIN_LICENSE = "GPL-3.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.html"

import picard
from picard import config
from picard.config import (
    TextOption,
    get_config,
)
from picard.ui.options import (
    OptionsPage,
    register_options_page,
)
from .ui_options_streaming_metadata import Ui_StreamingMetadataOptionsPage


class StreamingOptionsPage(OptionsPage):

    NAME = "streaming_metadata"
    TITLE = "Streaming Metadata"
    PARENT = "metadata"
    ACTIVE = True

    options = [
        TextOption("setting", "spotify_id", ""),
        TextOption("setting", "spotify_secret", ""),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_StreamingMetadataOptionsPage()
        self.ui.setupUi(self)

    def load(self):
        config = get_config()
        self.ui.spotify_id.setText(config.setting["spotify_id"])
        self.ui.spotify_secret.setText(config.setting["spotify_secret"])

    def save(self):
        config = get_config()
        config.setting["spotify_id"] = self.ui.spotify_id.text()
        config.setting["spotify_secret"] = self.ui.spotify_secret.text()


register_options_page(StreamingOptionsPage)