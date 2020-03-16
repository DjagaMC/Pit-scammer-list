
import json
import logging
import os
import urllib.request
from datetime import datetime

import aiofiles

from mojang_api import Player



logger = logging.getLogger('utils.prices')


# Skyblock Price Table
# Features autocorrect, string eval, full sanitizer
# Three methods of loading files for prices.


def lJVL(fname, absolute=False):
    prefix = "" if absolute else os.getcwd() + "/"
    with open(prefix + fname, "r") as fileHandle:
        data = fileHandle.read()
    return json.loads(data)



class PricesTable:
    def __init__(self, *, JFSc: dict = lJVL('database/scammer.json')):
        
        self.scammer = JFSc
        
    

    async def addScammer(self, *, username, reason, responsible_staff):
        try:
            players = Player(username=username)
            uuid = players.uuid
            name = players.username
        except:
            return None
        content = self.scammer
        content[uuid] = {'uuid': uuid, 'reason': reason, 'operated_staff': responsible_staff}
        jsonwrite = json.dumps(content, indent=4, sort_keys=True)

        async with aiofiles.open(os.path.join('database', 'scammer.json'), 'w') as f:
            await f.write(jsonwrite)
            await f.close()
        self.scammer = content

    async def removeScammer(self, *, username):
        try:
            players = Player(username=username)
            uuid = players.uuid
            name = players.username
        except:
            return None
        content = self.scammer
        content.pop(uuid)
        jsonwrite = json.dumps(content, indent=4, sort_keys=True)

        async with aiofiles.open(os.path.join('database', 'scammer.json'), 'w') as f:
            await f.write(jsonwrite)
            await f.close()
        self.scammer = content
        return 'good'

    
    async def queryScammer(self, username):
        try:
            players = Player(username=username)
            uuid = players.uuid
            name = players.username
        except Exception:
            try:
                players = Player(uuid=username)
                uuid = username
                name = players.username
            except Exception:
                return 'INVPLY'
        async with aiofiles.open(os.path.join('database', 'scammer.json'), 'r') as f:
            content = json.loads(await f.read())
            if uuid not in content:
                return 'NOTSCM'
            scammerinfo = content[uuid]
            await f.close()
            return [scammerinfo['uuid'], scammerinfo['reason'], scammerinfo['operated_staff'], name]

    
        