"""Base entity for Ouman EH-800."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ouman_eh_800_api.endpoint import OumanEndpoint

from .const import DOMAIN
from .coordinator import OumanEh800Coordinator


class OumanEh800Entity(CoordinatorEntity[OumanEh800Coordinator]):
    """Base entity for Ouman EH-800."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: OumanEh800Coordinator, endpoint: OumanEndpoint) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._endpoint = endpoint

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Ouman EH-800",
            manufacturer="Ouman",
            model="EH-800",
            # sw_version=coordinator.device_version,  # TODO: if available from API
        )
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{endpoint.name}"
        self._attr_name = endpoint.name
