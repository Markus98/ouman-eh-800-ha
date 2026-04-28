from typing import override

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ouman_eh_800_api import ControlEnum, EnumControlOumanEndpoint

from . import OumanEh800ConfigEntry
from .coordinator import OumanEh800Coordinator
from .entity import OumanEh800Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: OumanEh800ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ouman EH-800 select entities based on a config entry."""
    coordinator = entry.runtime_data

    entities = (
        OumanEh800SelectEntity(coordinator, endpoint)
        for endpoint in coordinator.select_endpoints
    )

    async_add_entities(entities)


class OumanEh800SelectEntity(OumanEh800Entity, SelectEntity):
    """Ouman EH-800 select entity."""

    def __init__(
        self, coordinator: OumanEh800Coordinator, endpoint: EnumControlOumanEndpoint
    ):
        """Initialize the select entity."""
        super().__init__(coordinator, endpoint)
        self._endpoint: EnumControlOumanEndpoint = endpoint

        self._attr_options: list[str] = [member.name for member in endpoint.enum_type]

    @override
    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        result = await self.coordinator.client.set_endpoint_value(
            self._endpoint, self._endpoint.enum_type[option]
        )
        self.coordinator.data[self._endpoint] = result
        self.async_write_ha_state()

        await self.coordinator.async_request_refresh()

    @property
    @override
    def current_option(self) -> str | None:
        """Return the current selected option."""
        value = self.coordinator.data[self._endpoint]
        assert isinstance(value, ControlEnum)
        return value.name
