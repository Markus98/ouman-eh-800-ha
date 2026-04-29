"""Data update coordinator for the Ouman EH-800 integration."""

import logging
from datetime import timedelta
from typing import override

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    ConfigEntryNotReady,
    HomeAssistantError,
    ServiceValidationError,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ouman_eh_800_api import (
    ControllableEndpoint,
    EnumControlOumanEndpoint,
    FloatControlOumanEndpoint,
    IntControlOumanEndpoint,
    OumanClientAuthenticationError,
    OumanClientCommunicationError,
    OumanEh800Client,
    OumanEndpoint,
    OumanRegistrySet,
    OumanUnit,
    OumanValues,
)

_LOGGER = logging.getLogger(__name__)

type OumanEh800ConfigEntry = ConfigEntry[OumanEh800Coordinator]


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

    @override
    async def _async_setup(self) -> None:
        try:
            # Even though not required to fetch values, perform login once
            # at the start to verify that the credentials are valid.
            await self.client.login()
            self._registry_set = await self.client.get_active_registries()
        except OumanClientAuthenticationError as err:
            raise ConfigEntryAuthFailed("Invalid credentials") from err
        except OumanClientCommunicationError as err:
            raise ConfigEntryNotReady("Error communicating with API") from err

        # Categorize the endpoints for platforms
        for endpoint in self._registry_set.endpoints:
            if not isinstance(endpoint, ControllableEndpoint):
                self.sensor_endpoints.append(endpoint)
            elif isinstance(endpoint, EnumControlOumanEndpoint):
                self.select_endpoints.append(endpoint)
            elif isinstance(
                endpoint, IntControlOumanEndpoint | FloatControlOumanEndpoint
            ):
                if (
                    isinstance(endpoint, IntControlOumanEndpoint)
                    and endpoint.unit == OumanUnit.PERCENT
                ):
                    self.valve_endpoints.append(endpoint)
                else:
                    self.number_endpoints.append(endpoint)

    @override
    async def _async_update_data(self) -> dict[OumanEndpoint, OumanValues]:
        """Fetch registry values from the device."""
        try:
            return await self.client.get_values(self._registry_set)
        except OumanClientCommunicationError as err:
            raise UpdateFailed("Error communicating with API") from err

    async def async_set_endpoint_value(
        self, endpoint: ControllableEndpoint, value: OumanValues | int
    ) -> None:
        """Set a value on the device and refresh."""
        try:
            result = await self.client.set_endpoint_value(endpoint, value)
        except OumanClientAuthenticationError as err:
            raise HomeAssistantError("Authentication failed") from err
        except OumanClientCommunicationError as err:
            raise HomeAssistantError("Error communicating with API") from err
        except ValueError as err:
            raise ServiceValidationError(str(err)) from err

        new_data = {**self.data, endpoint: result}
        self.async_set_updated_data(new_data)

        # Separate refresh on all endpoints to catch cascading changes
        await self.async_request_refresh()
