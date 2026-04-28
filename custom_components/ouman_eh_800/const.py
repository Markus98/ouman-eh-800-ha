"""Constants for the Ouman EH-800 integration."""

from ouman_eh_800_api import (
    L1BaseEndpoints,
    L1ConstantTempMode,
    L1NoRoomSensor,
    L1RoomSensor,
    L2BaseEndpoints,
    L2NoRoomSensor,
    L2RoomSensor,
    OumanEndpoint,
    SystemEndpoints,
)

DOMAIN = "ouman_eh_800"

CONF_SCAN_INTERVAL_SECONDS = "scan_interval_seconds"
DEFAULT_SCAN_INTERVAL = 60

# Sensor endpoints that should NOT be marked as DIAGNOSTIC.
# Sensors default to DIAGNOSTIC; these are the primary readings users care about.
PRIMARY_SENSOR_ENDPOINTS: frozenset[OumanEndpoint] = frozenset(
    (
        SystemEndpoints.OUTSIDE_TEMPERATURE,
        L1BaseEndpoints.SUPPLY_WATER_TEMPERATURE,
        L1BaseEndpoints.VALVE_POSITION,
        L1RoomSensor.ROOM_TEMPERATURE,
        L1RoomSensor.ROOM_TEMPERATURE_SETPOINT,
        L2BaseEndpoints.SUPPLY_WATER_TEMPERATURE,
        L2BaseEndpoints.VALVE_POSITION,
        L2RoomSensor.ROOM_TEMPERATURE,
        L2RoomSensor.ROOM_TEMPERATURE_SETPOINT,
    )
)

# Number endpoints that should NOT be marked as CONFIG.
# Numbers default to CONFIG; these are primary user-facing setpoints.
PRIMARY_NUMBER_ENDPOINTS: frozenset[OumanEndpoint] = frozenset(
    (
        L1RoomSensor.ROOM_TEMPERATURE_SETPOINT_USER,
        L2RoomSensor.ROOM_TEMPERATURE_SETPOINT_USER,
        L1ConstantTempMode.CONSTANT_TEMP_SETPOINT,
    )
)

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
        L1NoRoomSensor.TEMPERATURE_DROP,
        L1NoRoomSensor.BIG_TEMPERATURE_DROP,
        L1NoRoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
        L2RoomSensor.TEMPERATURE_DROP,
        L2RoomSensor.BIG_TEMPERATURE_DROP,
        L2RoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
        L2NoRoomSensor.TEMPERATURE_DROP,
        L2NoRoomSensor.BIG_TEMPERATURE_DROP,
        L2NoRoomSensor.ROOM_TEMPERATURE_FINE_TUNING,
    )
)
