import logging
from datetime import timedelta
from typing import Sequence

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ouman_eh_800_api import OumanEh800Client
from ouman_eh_800_api.endpoint import OumanEndpoint, OumanValues
from ouman_eh_800_api.exceptions import OumanClientCommunicationError
from ouman_eh_800_api.registry import OumanRegistrySet

_LOGGER = logging.getLogger(__name__)


class OumanEh800Coordinator(DataUpdateCoordinator):
    """Ouman EH-800 data update coordinator."""

    _registry_set: OumanRegistrySet

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: OumanEh800Client,
        update_interval: int,
    ):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Ouman EH-800",
            config_entry=config_entry,
            update_interval=timedelta(seconds=update_interval),
            always_update=False,
        )
        self.client: OumanEh800Client = client

    async def _async_setup(self) -> None:
        """Fetch available registries from the device."""
        # Even though not required to fetch values, perform login once
        # at the start to verify that the credentials are valid.
        await self.client.login()

        self._registry_set = await self.client.get_active_registries()

    @property
    def endpoints(self) -> Sequence[OumanEndpoint]:
        return self._registry_set.endpoints

    async def _async_update_data(self) -> dict[OumanEndpoint, OumanValues]:
        """Fetch registry values from the device."""
        try:
            return await self.client.get_values(self._registry_set)
        except OumanClientCommunicationError as err:
            raise UpdateFailed("Error communicating with API") from err
