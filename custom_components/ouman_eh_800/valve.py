"""Valve platform for the Ouman EH-800 integration."""

from typing import override

from homeassistant.components.valve import ValveEntity, ValveEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ouman_eh_800_api import IntControlOumanEndpoint

from .coordinator import OumanEh800ConfigEntry, OumanEh800Coordinator
from .entity import OumanEh800Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OumanEh800ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ouman EH-800 valve entities based on a config entry."""
    coordinator = entry.runtime_data

    entities = (
        OumanEh800ValveEntity(coordinator, endpoint)
        for endpoint in coordinator.valve_endpoints
    )
    async_add_entities(entities)


class OumanEh800ValveEntity(OumanEh800Entity, ValveEntity):
    """Ouman EH-800 valve entity."""

    _attr_reports_position = True
    _attr_supported_features = (
        ValveEntityFeature.OPEN
        | ValveEntityFeature.CLOSE
        | ValveEntityFeature.SET_POSITION
    )

    def __init__(
        self, coordinator: OumanEh800Coordinator, endpoint: IntControlOumanEndpoint
    ):
        """Initialize the valve entity."""
        super().__init__(coordinator, endpoint)
        self._endpoint: IntControlOumanEndpoint = endpoint

    @property
    @override
    def current_valve_position(self) -> int:
        """Return current valve position 0-100."""
        value = self.coordinator.data[self._endpoint]
        assert isinstance(value, float)
        return int(value)

    @override
    async def async_set_valve_position(self, position: int) -> None:
        """Move valve to the given position."""
        await self.coordinator.async_set_endpoint_value(self._endpoint, position)

    @override
    async def async_open_valve(self) -> None:
        """Fully open the valve."""
        await self.async_set_valve_position(100)

    @override
    async def async_close_valve(self) -> None:
        """Fully close the valve."""
        await self.async_set_valve_position(0)
