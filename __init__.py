# -*- coding: utf-8 -*-
# MetaStreaming plugin for Picard
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
# Changelog:
# [2023-06-17] Initial version


PLUGIN_NAME = "Streaming Metadata"
PLUGIN_AUTHOR = "Stanisław Borodziuk"
PLUGIN_DESCRIPTION = "Get metadata from streaming services"
PLUGIN_VERSION = "0.1.0"
PLUGIN_API_VERSIONS = ["2.0", "2.1", "2.2"]
PLUGIN_LICENSE = "GPL-3.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.html"

from PyQt5 import QtCore
from PyQt5.QtNetwork import (
    QNetworkReply,
    QNetworkRequest,
)
from picard import log, config
from picard.config import Option, get_config
from picard.album import Album
from picard.ui.options import OptionsPage, register_options_page
from picard.ui.itemviews import BaseAction, register_cluster_action
from picard.ui.searchdialog import Retry, SearchDialog
from picard.plugins.metastreaming.ui_options_streaming_metadata import (
    Ui_StreamingMetadataOptionsPage,
)
import re

DEEZER_API_URL = "api.deezer.com"
DEEZER_API_PORT = 443

class GetMetaStreaming(BaseAction):
    NAME = "Get metadata from streamings"

    def callback(self, objs):
        log.debug("MetaStreaming BaseAction executed")
        obj = objs[0]
        # Working
        # for file in obj.files:
        #     log.debug(file.metadata["title"])

        dialog = MetaStreamingSearchDialog(obj)
        dialog.exec_()


class MetaStreamingSearchDialog(SearchDialog):

    dialog_header_state = "metastreamingsearchdialog_header_state"

    options = [Option("persist", dialog_header_state, QtCore.QByteArray())]

    def __init__(self, cluster, parent=None):
        super().__init__(
            parent,
            accept_button_title=_("Select for metadata source"),
            force_advanced_search=True,
        )
        self.cluster = cluster
        self.setWindowTitle(_("MetaStreaming Search Results"))
        self.columns = [
            ("name", _("Name")),
            ("artist", _("Artist")),
            ("tracks", _("Tracks")),
            ("cover", _("Cover")),
        ]
        self.cover_cells = []
        self.fetching = False
        self.scrolled.connect(self.fetch_coverarts)
        self.metadata = []

    def search(self, text):
        log.debug(text)
        self.metadata = self.parse_deezer_url(text)
        if self.metadata is None:
            return

        self.cluster.tagger.webservice.get_url(
            url=DEEZER_API_URL + self._deezer_album_url(),
            handler=self._caa_json_downloaded,
            priority=True,
            important=False,
            cacheloadcontrol=QNetworkRequest.CacheLoadControl.PreferNetwork,
        )


        # self.cluster.tagger.webservice.get_url(
        #     url=CAA_URL + self._caa_path,
        #     handler=self._caa_json_downloaded,
        #     priority=True,
        #     important=False,
        #     cacheloadcontrol=QNetworkRequest.CacheLoadControl.PreferNetwork,
        # )

    def fetch_coverarts(self):
        log.debug("fetch_coverarts placeholder function")

    def fetch_coverart(self, cell):
        log.debug("fetch_coverart placeholder function")

    def accept_event(self, rows):
        log.debug("accept_event placeholder function")

    def parse_deezer_url(self, url):
        """Extract language, resource type and id from a deezer url.
        It returns a dict with resource and id keys on success, None else
        """
        r = re.compile(r'^https?://(?:www.)?deezer.com(?:/(?P<language>.+))?/(?P<service>[A-Za-z]+)/(?P<id>[A-Za-z0-9]+)')
        match = r.match(url)
        if match is not None:
            return match.groupdict()
        return None

    def _deezer_album_url(self):
        # https://api.deezer.com/version/service/id/method/?parameters
        return "/{}/{}".format(self.metadata["service"], self.metadata["id"])


class MetaStreamingOptionsPage(OptionsPage):
    NAME = "streaming_metadata"
    TITLE = "Streaming Metadata"
    PARENT = "plugins"

    options = [
        config.TextOption("setting", "metastreaming_spotify_id", ""),
        config.TextOption("setting", "metastreaming_spotify_secret", ""),
        config.BoolOption("setting", "metastreaming_spotify_enabled", False),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_StreamingMetadataOptionsPage()
        self.ui.setupUi(self)

    def load(self):
        config = get_config()
        self.ui.spotify_id.setText(config.setting["metastreaming_spotify_id"])
        self.ui.spotify_secret.setText(config.setting["metastreaming_spotify_secret"])
        self.ui.enable_spotify.setChecked(
            config.setting["metastreaming_spotify_enabled"]
        )
        log.debug("MetaStreaming settings loaded from config")

    def save(self):
        config = get_config()
        config.setting["metastreaming_spotify_id"] = self.ui.spotify_id.text()
        config.setting["metastreaming_spotify_secret"] = self.ui.spotify_secret.text()
        config.setting["metastreaming_spotify_enabled"] = (
            self.ui.enable_spotify.isChecked()
        )
        log.debug("MetaStreaming settings saved to config")


# plugin = MetaStreamingPlugin()
register_cluster_action(GetMetaStreaming())
register_options_page(MetaStreamingOptionsPage)
