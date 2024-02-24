import logging

from ucapi import (
    AbortDriverSetup,
    DriverSetupRequest,
    IntegrationSetupError,
    RequestUserInput,
    SetupAction,
    SetupComplete,
    SetupDriver,
    SetupError,
    UserDataResponse,
)

from discovery import discover_dm_players

_LOG = logging.getLogger(__name__)


async def setup_handler(msg: SetupDriver) -> SetupAction | SetupError:
    if isinstance(msg, DriverSetupRequest):
        return await handle_driver_setup(msg)
    if isinstance(msg, UserDataResponse):
        return await handle_selected_device(msg)
    if isinstance(msg, AbortDriverSetup):
        _LOG.info("Setup was aborted with code: %s", msg.error)
    return SetupError()


async def handle_driver_setup(_msg: DriverSetupRequest) -> RequestUserInput | SetupError:
    if not (devices := await discover_dm_players()):
        return SetupError(error_type=IntegrationSetupError.NOT_FOUND)
    dropdown_items = [{"id": host, "label": {"en": f"{label} ({host})"}} for (host, label) in devices]
    return RequestUserInput(
        {"en": "Please choose your device"},
        [
            {
                "field": {"dropdown": {"value": dropdown_items[0]["id"], "items": dropdown_items}},
                "id": "choice",
                "label": {
                    "en": "Choose your device",
                },
            }
        ],
    )


async def handle_selected_device(msg: UserDataResponse) -> SetupComplete | SetupError:
    return SetupComplete()
