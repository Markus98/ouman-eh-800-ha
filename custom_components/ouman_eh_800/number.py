from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ouman_eh_800_api import (
    FloatControlOumanEndpoint,
    IntControlOumanEndpoint,
    OumanUnit,
)

from . import OumanEh800ConfigEntry
from .const import TEMPERATURE_DELTA_ENDPOINTS
from .coordinator import OumanEh800Coordinator
from .entity import OumanEh800Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OumanEh800ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ouman EH-800 number entities based on a config entry."""
    coordinator = entry.runtime_data

    entities = (
        OumanEh800NumberEntity(coordinator, endpoint)
        for endpoint in coordinator.number_endpoints
    )

    async_add_entities(entities)


class OumanEh800NumberEntity(OumanEh800Entity, NumberEntity):
    """Ouman EH-800 number entity."""

    def __init__(
        self,
        coordinator: OumanEh800Coordinator,
        endpoint: IntControlOumanEndpoint | FloatControlOumanEndpoint,
    ):
        """Initialize the number entity."""
        super().__init__(coordinator, endpoint)
        self._endpoint: IntControlOumanEndpoint | FloatControlOumanEndpoint = endpoint

        self._attr_mode = NumberMode.BOX
        if endpoint.unit == OumanUnit.CELSIUS:
            self._attr_device_class = (
                NumberDeviceClass.TEMPERATURE_DELTA
                if endpoint in TEMPERATURE_DELTA_ENDPOINTS
                else NumberDeviceClass.TEMPERATURE
            )

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
    def native_value(self) -> float:
        """Return the current number value."""
        value = self.coordinator.data[self._endpoint]
        assert isinstance(value, float)
        return value
