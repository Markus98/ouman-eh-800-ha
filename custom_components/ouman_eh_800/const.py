"""Constants for the Ouman EH-800 integration."""

from typing import Mapping

from homeassistant.const import EntityCategory
from ouman_eh_800_api.endpoint import OumanEndpoint
from ouman_eh_800_api.registry import (
    L1Endpoints,
    L1EndpointsWithRoomSensor,
    L2Endpoints,
    L2EndpointsWithRoomSensor,
    SystemEndpoints,
)

DOMAIN = "ouman_eh_800"

CONF_SCAN_INTERVAL_SECONDS = "scan_interval_seconds"
DEFAULT_SCAN_INTERVAL = 30

ENDPOINT_CATEGORIES: Mapping[OumanEndpoint, EntityCategory] = {
    # L1
    L1Endpoints.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L1Endpoints.CURVE_0_TEMP: EntityCategory.CONFIG,
    L1Endpoints.CURVE_20_TEMP: EntityCategory.CONFIG,
    L1Endpoints.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1Endpoints.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1Endpoints.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L1EndpointsWithRoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L1Endpoints.WATER_OUT_MAX_TEMP: EntityCategory.CONFIG,
    L1Endpoints.WATER_OUT_MIN_TEMP: EntityCategory.CONFIG,
    L1Endpoints.CIRCUIT_NAME: EntityCategory.DIAGNOSTIC,
    L1Endpoints.HEATING_SHUTDOWN_STATUS: EntityCategory.DIAGNOSTIC,
    L1Endpoints.ROOM_SENSOR_INSTALLED: EntityCategory.DIAGNOSTIC,
    L1Endpoints.TEMPERATURE_LEVEL_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
    # L2
    L2Endpoints.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L2Endpoints.CURVE_0_TEMP: EntityCategory.CONFIG,
    L2Endpoints.CURVE_20_TEMP: EntityCategory.CONFIG,
    L2Endpoints.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2Endpoints.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2Endpoints.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L2EndpointsWithRoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L2Endpoints.WATER_OUT_MAX_TEMP: EntityCategory.CONFIG,
    L2Endpoints.WATER_OUT_MIN_TEMP: EntityCategory.CONFIG,
    L2Endpoints.CIRCUIT_NAME: EntityCategory.DIAGNOSTIC,
    L2Endpoints.ROOM_SENSOR_INSTALLED: EntityCategory.DIAGNOSTIC,
    L2Endpoints.TEMPERATURE_LEVEL_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
    # System
    SystemEndpoints.TREND_SAMPLE_INTERVAL: EntityCategory.CONFIG,
    SystemEndpoints.L2_INSTALLED_STATUS: EntityCategory.DIAGNOSTIC,
    SystemEndpoints.RELAY_CONFIGURATION_TYPE: EntityCategory.DIAGNOSTIC,
    SystemEndpoints.RELAY_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
}

ENDPOINTS_DISABLED_BY_DEFAULT: frozenset[OumanEndpoint] = frozenset(
    [
        # L1
        L1Endpoints.CIRCUIT_NAME,
        L1Endpoints.HEATING_SHUTDOWN_STATUS,
        L1Endpoints.ROOM_SENSOR_INSTALLED,
        L1Endpoints.TEMPERATURE_LEVEL_STATUS_TEXT,
        # L2
        L2Endpoints.CIRCUIT_NAME,
        L2Endpoints.ROOM_SENSOR_INSTALLED,
        L2Endpoints.TEMPERATURE_LEVEL_STATUS_TEXT,
        # System
        SystemEndpoints.RELAY_STATUS_TEXT,
        SystemEndpoints.L2_INSTALLED_STATUS,
        SystemEndpoints.RELAY_CONFIGURATION_TYPE,
    ]
)
