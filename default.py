# -*- coding: utf-8 -*-

#################################################################################################

import logging
import os
import sys
import urlparse

import xbmc
import xbmcaddon

#################################################################################################

_addon = xbmcaddon.Addon(id='plugin.video.emby')
_addon_path = _addon.getAddonInfo('path').decode('utf-8')
_base_resource = xbmc.translatePath(os.path.join(_addon_path, 'resources', 'lib')).decode('utf-8')
sys.path.append(_base_resource)

#################################################################################################

import entrypoint

#################################################################################################

import loghandler

import utils
import time
def waitEmbyLoaded():
    userId = utils.window('emby_currUser')
    server = utils.window('emby_server%s' % userId)
    token = utils.window('emby_accessToken%s' % userId)
    while not userId or not server or not token:
        time.sleep(0.2)
        userId = utils.window('emby_currUser')
        server = utils.window('emby_server%s' % userId)
        token = utils.window('emby_accessToken%s' % userId)
        xbmc.log("Emby plugin.video.emby : Wait for emby loaded %s, %s, %s"%(userId, server, token))

loghandler.config()
log = logging.getLogger("EMBY.default_movies")

#################################################################################################

# Parse parameters
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = urlparse.parse_qs(sys.argv[2][1:])
log.warn("Parameter string: %s" % sys.argv[2])

try:
    mode = params['mode'][0]
    itemid = params['id'][0]
    dbid = params['dbid'][0]

except (KeyError, IndexError):
    pass

else:
    if "play" in mode:
        waitEmbyLoaded()
        # plugin.video.emby entrypoint
        entrypoint.doPlayback(itemid, dbid)
