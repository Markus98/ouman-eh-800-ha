import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ouman_eh_800_api import OumanEh800Client
from ouman_eh_800_api.registry import OumanRegistry
from ouman_eh_800_api.exceptions import OumanClientCommunicationError

_LOGGER = logging.getLogger(__name__)


class OumanEh800Coordinator(DataUpdateCoordinator):
    """Ouman EH-800 data update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: OumanEh800Client,
    ):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Ouman EH-800",
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            always_update=False,
        )
        self.client: OumanEh800Client = client

    async def _async_setup(self):
        """Fetch available registries from the device."""
        self._registries: list[
            type[OumanRegistry]
        ] = await self.client.get_active_registries()

    @property
    def registries(self):
        return self._registries

    @property
    def endpoints(self):
        return (
            endpoint for registry in self.registries for endpoint in registry.iterate_endpoints()
        )

    async def _async_update_data(self):
        """Fetch registry values from the device."""
        try:
            return await self.client.get_registry_values(self.registries)
        except OumanClientCommunicationError as err:
            raise UpdateFailed("Error communicating with API") from err
