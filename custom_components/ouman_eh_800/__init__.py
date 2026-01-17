"""The Ouman EH-800 integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from ouman_eh_800_api import OumanEh800Client

from .const import CONF_SCAN_INTERVAL_SECONDS, DEFAULT_SCAN_INTERVAL
from .coordinator import OumanEh800Coordinator

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type OumanEh800ConfigEntry = ConfigEntry[OumanEh800Coordinator]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: OumanEh800ConfigEntry) -> bool:
    """Set up Ouman EH-800 from a config entry."""
    client = OumanEh800Client(
        session=async_get_clientsession(hass),
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        address=entry.data[CONF_HOST],
    )

    # TODO: verify that login works

    scan_interval = entry.options.get(CONF_SCAN_INTERVAL_SECONDS, DEFAULT_SCAN_INTERVAL)
    coordinator = OumanEh800Coordinator(hass, entry, client, scan_interval)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: OumanEh800ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
