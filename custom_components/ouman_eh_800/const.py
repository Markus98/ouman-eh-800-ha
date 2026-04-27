"""Constants for the Ouman EH-800 integration."""

from collections.abc import Mapping

from homeassistant.const import EntityCategory
from ouman_eh_800_api import (
    L1BaseEndpoints,
    L1ConstantTempMode,
    L1FivePointCurve,
    L1NoRoomSensor,
    L1RoomSensor,
    L1ThreePointCurve,
    L2BaseEndpoints,
    L2FivePointCurve,
    L2NoRoomSensor,
    L2RoomSensor,
    L2ThreePointCurve,
    OumanEndpoint,
    SystemEndpoints,
)

DOMAIN = "ouman_eh_800"

CONF_SCAN_INTERVAL_SECONDS = "scan_interval_seconds"
DEFAULT_SCAN_INTERVAL = 60

ENDPOINT_CATEGORIES: Mapping[OumanEndpoint, EntityCategory] = {
    # L1
    L1BaseEndpoints.VALVE_POSITION_SETPOINT: EntityCategory.CONFIG,
    L1BaseEndpoints.WATER_OUT_MAX_TEMP: EntityCategory.CONFIG,
    L1BaseEndpoints.WATER_OUT_MIN_TEMP: EntityCategory.CONFIG,
    L1BaseEndpoints.CIRCUIT_NAME: EntityCategory.DIAGNOSTIC,
    L1BaseEndpoints.CURVE_SUPPLY_WATER_TEMPERATURE: EntityCategory.DIAGNOSTIC,
    L1BaseEndpoints.FINE_ADJUSTMENT_EFFECT: EntityCategory.DIAGNOSTIC,
    L1BaseEndpoints.ROOM_SENSOR_INSTALLED: EntityCategory.DIAGNOSTIC,
    L1BaseEndpoints.TEMPERATURE_LEVEL_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
    L1ThreePointCurve.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L1ThreePointCurve.CURVE_0_TEMP: EntityCategory.CONFIG,
    L1ThreePointCurve.CURVE_20_TEMP: EntityCategory.CONFIG,
    L1FivePointCurve.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L1FivePointCurve.CURVE_MINUS_10_TEMP: EntityCategory.CONFIG,
    L1FivePointCurve.CURVE_0_TEMP: EntityCategory.CONFIG,
    L1FivePointCurve.CURVE_10_TEMP: EntityCategory.CONFIG,
    L1FivePointCurve.CURVE_20_TEMP: EntityCategory.CONFIG,
    L1RoomSensor.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1RoomSensor.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1RoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L1RoomSensor.DELAYED_ROOM_TEMPERATURE: EntityCategory.DIAGNOSTIC,
    L1RoomSensor.ROOM_SENSOR_POTENTIOMETER: EntityCategory.DIAGNOSTIC,
    L1NoRoomSensor.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1NoRoomSensor.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L1NoRoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L1ConstantTempMode.CONSTANT_TEMP_SETPOINT: EntityCategory.CONFIG,
    # L2
    L2BaseEndpoints.VALVE_POSITION_SETPOINT: EntityCategory.CONFIG,
    L2BaseEndpoints.WATER_OUT_MAX_TEMP: EntityCategory.CONFIG,
    L2BaseEndpoints.WATER_OUT_MIN_TEMP: EntityCategory.CONFIG,
    L2BaseEndpoints.CIRCUIT_NAME: EntityCategory.DIAGNOSTIC,
    L2BaseEndpoints.CURVE_SUPPLY_WATER_TEMPERATURE: EntityCategory.DIAGNOSTIC,
    L2BaseEndpoints.DELAYED_OUTDOOR_TEMPERATURE_EFFECT: EntityCategory.DIAGNOSTIC,
    L2BaseEndpoints.ROOM_SENSOR_INSTALLED: EntityCategory.DIAGNOSTIC,
    L2BaseEndpoints.TEMPERATURE_LEVEL_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
    L2ThreePointCurve.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L2ThreePointCurve.CURVE_0_TEMP: EntityCategory.CONFIG,
    L2ThreePointCurve.CURVE_20_TEMP: EntityCategory.CONFIG,
    L2FivePointCurve.CURVE_MINUS_20_TEMP: EntityCategory.CONFIG,
    L2FivePointCurve.CURVE_MINUS_10_TEMP: EntityCategory.CONFIG,
    L2FivePointCurve.CURVE_0_TEMP: EntityCategory.CONFIG,
    L2FivePointCurve.CURVE_10_TEMP: EntityCategory.CONFIG,
    L2FivePointCurve.CURVE_20_TEMP: EntityCategory.CONFIG,
    L2RoomSensor.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2RoomSensor.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2RoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    L2RoomSensor.DELAYED_ROOM_TEMPERATURE: EntityCategory.DIAGNOSTIC,
    L2NoRoomSensor.TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2NoRoomSensor.BIG_TEMPERATURE_DROP: EntityCategory.CONFIG,
    L2NoRoomSensor.ROOM_TEMPERATURE_FINE_TUNING: EntityCategory.CONFIG,
    # System
    SystemEndpoints.TREND_SAMPLE_INTERVAL: EntityCategory.CONFIG,
    SystemEndpoints.L2_INSTALLED_STATUS: EntityCategory.DIAGNOSTIC,
    SystemEndpoints.RELAY_CONFIGURATION_TYPE: EntityCategory.DIAGNOSTIC,
    SystemEndpoints.RELAY_STATUS_TEXT: EntityCategory.DIAGNOSTIC,
}

ENDPOINTS_DISABLED_BY_DEFAULT: frozenset[OumanEndpoint] = frozenset(
    (
        # L1
        L1BaseEndpoints.CIRCUIT_NAME,
        L1BaseEndpoints.CURVE_SUPPLY_WATER_TEMPERATURE,
        L1BaseEndpoints.FINE_ADJUSTMENT_EFFECT,
        L1BaseEndpoints.ROOM_SENSOR_INSTALLED,
        L1BaseEndpoints.TEMPERATURE_LEVEL_STATUS_TEXT,
        L1RoomSensor.DELAYED_ROOM_TEMPERATURE,
        L1RoomSensor.ROOM_SENSOR_POTENTIOMETER,
        # L2
        L2BaseEndpoints.CIRCUIT_NAME,
        L2BaseEndpoints.CURVE_SUPPLY_WATER_TEMPERATURE,
        L2BaseEndpoints.DELAYED_OUTDOOR_TEMPERATURE_EFFECT,
        L2BaseEndpoints.ROOM_SENSOR_INSTALLED,
        L2BaseEndpoints.TEMPERATURE_LEVEL_STATUS_TEXT,
        L2RoomSensor.DELAYED_ROOM_TEMPERATURE,
        # System
        SystemEndpoints.RELAY_STATUS_TEXT,
        SystemEndpoints.L2_INSTALLED_STATUS,
        SystemEndpoints.RELAY_CONFIGURATION_TYPE,
        SystemEndpoints.TREND_SAMPLE_INTERVAL,
    )
)

TEMPERATURE_DELTA_ENDPOINTS: frozenset[OumanEndpoint] = frozenset(
    (
        L1RoomSensor.TEMPERATURE_DROP,
        L1RoomSensor.BIG_TEMPERATURE_DROP,
        L1RoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
        L1RoomSensor.ROOM_SENSOR_POTENTIOMETER,
        L2RoomSensor.TEMPERATURE_DROP,
        L2RoomSensor.BIG_TEMPERATURE_DROP,
        L2RoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
    )
)
