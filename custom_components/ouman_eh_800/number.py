from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ouman_eh_800_api import (
    FloatControlOumanEndpoint,
    IntControlOumanEndpoint,
    L1Endpoints,
    L1EndpointsWithRoomSensor,
    L2Endpoints,
    L2EndpointsWithRoomSensor,
    OumanUnit,
)

from . import OumanEh800ConfigEntry
from .coordinator import OumanEh800Coordinator
from .entity import OumanEh800Entity

NumberControlOumanEndpoint = IntControlOumanEndpoint | FloatControlOumanEndpoint


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OumanEh800ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ouman EH-800 number entities based on a config entry."""
    coordinator = entry.runtime_data

    endpoints = (
        endpoint
        for endpoint in coordinator.endpoints
        if isinstance(endpoint, NumberControlOumanEndpoint)
    )
    entities = (OumanEh800NumberEntity(coordinator, endpoint) for endpoint in endpoints)

    async_add_entities(entities)


class OumanEh800NumberEntity(OumanEh800Entity, NumberEntity):
    """Ouman EH-800 number entity."""

    def __init__(
        self, coordinator: OumanEh800Coordinator, endpoint: NumberControlOumanEndpoint
    ):
        """Initialize the number entity."""
        super().__init__(coordinator, endpoint)
        self._endpoint: NumberControlOumanEndpoint = endpoint

        self._attr_mode = NumberMode.BOX
        if endpoint.unit == OumanUnit.CELSIUS:
            self._attr_device_class = NumberDeviceClass.TEMPERATURE
            if endpoint in (
                L1Endpoints.ROOM_TEMPERATURE_FINE_TUNING,
                L1EndpointsWithRoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
                L2Endpoints.ROOM_TEMPERATURE_FINE_TUNING,
                L2EndpointsWithRoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
            ):
                self._attr_device_class = NumberDeviceClass.TEMPERATURE_DELTA

        self._attr_native_unit_of_measurement = endpoint.unit
        self._attr_native_max_value = float(endpoint.max_val)
        self._attr_native_min_value = float(endpoint.min_val)
        self._attr_native_step = (
            1 if isinstance(endpoint, IntControlOumanEndpoint) else 0.1
        )

    async def async_set_native_value(self, value: float) -> None:
        """Change the number value."""
        final_value: float | int = value
        if isinstance(self._endpoint, IntControlOumanEndpoint):
            final_value = int(value)
        result = await self.coordinator.client.set_endpoint_value(
            self._endpoint, final_value
        )
        self.coordinator.data[self._endpoint] = result
        self.async_write_ha_state()

        await self.coordinator.async_request_refresh()

    @property
    def native_value(self):
        """Return the current number value."""
        return self.coordinator.data[self._endpoint]
