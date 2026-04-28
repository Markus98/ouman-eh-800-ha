import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ouman_eh_800_api import (
    ControllableEndpoint,
    EnumControlOumanEndpoint,
    FloatControlOumanEndpoint,
    IntControlOumanEndpoint,
    OumanClientCommunicationError,
    OumanEh800Client,
    OumanEndpoint,
    OumanRegistrySet,
    OumanUnit,
    OumanValues,
)

_LOGGER = logging.getLogger(__name__)


class OumanEh800Coordinator(DataUpdateCoordinator[dict[OumanEndpoint, OumanValues]]):
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

        self.sensor_endpoints: list[OumanEndpoint] = []
        self.number_endpoints: list[
            IntControlOumanEndpoint | FloatControlOumanEndpoint
        ] = []
        self.select_endpoints: list[EnumControlOumanEndpoint] = []
        self.valve_endpoints: list[IntControlOumanEndpoint] = []

    async def _async_setup(self) -> None:
        # Even though not required to fetch values, perform login once
        # at the start to verify that the credentials are valid.
        await self.client.login()

        self._registry_set = await self.client.get_active_registries()

        # Categorize the endpoints for platforms
        for endpoint in self._registry_set.endpoints:
            if not isinstance(endpoint, ControllableEndpoint):
                self.sensor_endpoints.append(endpoint)
            elif isinstance(endpoint, EnumControlOumanEndpoint):
                self.select_endpoints.append(endpoint)
            elif isinstance(
                endpoint, IntControlOumanEndpoint | FloatControlOumanEndpoint
            ):
                if endpoint.unit == OumanUnit.PERCENT and isinstance(
                    endpoint, IntControlOumanEndpoint
                ):
                    self.valve_endpoints.append(endpoint)
                else:
                    self.number_endpoints.append(endpoint)

    async def _async_update_data(self) -> dict[OumanEndpoint, OumanValues]:
        """Fetch registry values from the device."""
        try:
            return await self.client.get_values(self._registry_set)
        except OumanClientCommunicationError as err:
            raise UpdateFailed("Error communicating with API") from err
