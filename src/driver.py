#!/usr/bin/env python3

import asyncio
import logging
import sys
from typing import Any

import ucapi

from setup import setup_handler

loop = asyncio.get_event_loop()
api = ucapi.IntegrationAPI(loop)


async def cmd_handler(entity: ucapi.Button, cmd_id: str, _params: dict[str, Any] | None) -> ucapi.StatusCodes:
    print(f"Got {entity.id} command request: {cmd_id}")

    return ucapi.StatusCodes.OK


@api.listens_to(ucapi.Events.CONNECT)
async def on_connect() -> None:
    await api.set_device_state(ucapi.DeviceStates.CONNECTED)


if __name__ == "__main__":
    logging.basicConfig()

    button = ucapi.Button(
        "button1",
        "Push the button",
        cmd_handler=cmd_handler,
    )
    api.available_entities.add(button)

    loop.run_until_complete(api.init(sys.argv[1], setup_handler))
    loop.run_forever()
