#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from urlparse import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import kodilogging
from hitbox import Hitbox, HitboxException

PLUGINHANDLE = int(sys.argv[1])
ADDON = xbmcaddon.Addon()

PATH_GAMES = 'games/'
PATH_CHANNELS = 'channels/'
PATH_FOLLOWING = 'following/'


class HitboxController():

    def __init__(self, logger):
        self.logger = logger
        self.hitbox = Hitbox()

    def show_root(self):
        add_dir('Games', PATH_GAMES)
        add_dir('Channels', PATH_CHANNELS)
        add_dir('Following', PATH_FOLLOWING)
        xbmcplugin.endOfDirectory(handle=PLUGINHANDLE)

    def show_games(self):
        for game in self.hitbox.get_games():
            add_dir(game['category_name'], '?category=' + game['category_id'], self.hitbox.STATIC_URL + game['category_logo_large'])
        xbmcplugin.endOfDirectory(handle=PLUGINHANDLE)


def add_dir(title, plugin_path, icon='DefaultFolder.png'):
    plugin_url = sys.argv[0] + plugin_path
    item = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(handle=PLUGINHANDLE, url=plugin_url, listitem=item, isFolder=True)


if __name__ == '__main__':
    path = urlparse(sys.argv[0]).path
    kodilogging.debug(urlparse(path))
    hb = HitboxController(kodilogging)
    if path == '/':
        hb.show_root()
    elif path == '/games/':
        hb.show_games()

