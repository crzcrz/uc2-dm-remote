import asyncio
import upnpy

DM_DEVICE = "urn:schemas-denon-com:device:AiosDevice"


async def discover_dm_players():
    upnp = upnpy.UPnP()
    devices = await asyncio.to_thread(upnp.discover)
    players = [(d.host, d.friendly_name) for d in devices if d.type_.startswith(DM_DEVICE)]
    return players
