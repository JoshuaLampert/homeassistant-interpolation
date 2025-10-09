"""Support for interpolation sensors."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from scipy.interpolate import CubicSpline

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

CONF_SOURCE_ENTITY = "source_entity"
CONF_X_VALUES = "x_values"
CONF_Y_VALUES = "y_values"
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"
CONF_BOUNDARY_CONDITION = "boundary_condition"

DEFAULT_NAME = "Interpolation"
DEFAULT_BOUNDARY_CONDITION = "not-a-knot"

# Valid boundary condition types for cubic spline
BOUNDARY_CONDITIONS = ["not-a-knot", "periodic", "clamped", "natural"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCE_ENTITY): cv.entity_id,
        vol.Required(CONF_X_VALUES): [vol.Coerce(float)],
        vol.Required(CONF_Y_VALUES): [vol.Coerce(float)],
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_BOUNDARY_CONDITION, default=DEFAULT_BOUNDARY_CONDITION): vol.In(BOUNDARY_CONDITIONS),
    }
)


def validate_data_points(x_values: list[float], y_values: list[float]) -> None:
    """Validate that x and y values are compatible for cubic spline interpolation."""
    if len(x_values) != len(y_values):
        raise vol.Invalid("x_values and y_values must have the same length")
    
    if len(x_values) < 2:
        raise vol.Invalid("At least 2 data points are required for interpolation")
    
    # Check that x values are strictly increasing
    if not all(x_values[i] < x_values[i + 1] for i in range(len(x_values) - 1)):
        raise vol.Invalid("x_values must be strictly increasing")


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Interpolation sensor."""
    name = config[CONF_NAME]
    source_entity = config[CONF_SOURCE_ENTITY]
    x_values = config[CONF_X_VALUES]
    y_values = config[CONF_Y_VALUES]
    unique_id = config.get(CONF_UNIQUE_ID)
    unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)
    boundary_condition = config[CONF_BOUNDARY_CONDITION]
    
    # Validate data points
    try:
        validate_data_points(x_values, y_values)
    except vol.Invalid as err:
        _LOGGER.error("Configuration error: %s", err)
        return
    
    async_add_entities(
        [InterpolationSensor(name, source_entity, x_values, y_values, unique_id, unit_of_measurement, boundary_condition)],
        True,
    )


class InterpolationSensor(SensorEntity):
    """Representation of an Interpolation sensor."""

    def __init__(
        self,
        name: str,
        source_entity: str,
        x_values: list[float],
        y_values: list[float],
        unique_id: str | None,
        unit_of_measurement: str | None,
        boundary_condition: str,
    ) -> None:
        """Initialize the Interpolation sensor."""
        self._attr_name = name
        self._source_entity = source_entity
        self._x_values = x_values
        self._y_values = y_values
        self._attr_unique_id = unique_id
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_native_value = None
        self._spline = None
        self._boundary_condition = boundary_condition
        
        # Create the cubic spline interpolation function
        try:
            self._spline = CubicSpline(x_values, y_values, bc_type=boundary_condition)
            _LOGGER.debug(
                "Created cubic spline interpolation for %s with %d data points and bc_type='%s'",
                name,
                len(x_values),
                boundary_condition,
            )
        except Exception as err:
            _LOGGER.error("Error creating cubic spline: %s", err)

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        
        @callback
        def sensor_state_listener(event):
            """Handle state changes of the source entity."""
            new_state = event.data.get("new_state")
            if new_state is None or new_state.state in ("unknown", "unavailable"):
                self._attr_native_value = None
            else:
                self._update_value(new_state.state)
            self.async_write_ha_state()
        
        # Track state changes of the source entity
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._source_entity], sensor_state_listener
            )
        )
        
        # Initialize with current state
        source_state = self.hass.states.get(self._source_entity)
        if source_state and source_state.state not in ("unknown", "unavailable"):
            self._update_value(source_state.state)

    def _update_value(self, source_value: str) -> None:
        """Update the sensor value based on the source entity state."""
        if self._spline is None:
            _LOGGER.error("Cubic spline not initialized")
            self._attr_native_value = None
            return
        
        try:
            x = float(source_value)
            y = float(self._spline(x))
            self._attr_native_value = y
            _LOGGER.debug(
                "Interpolated value for %s: x=%s, y=%s",
                self._attr_name,
                x,
                y,
            )
        except (ValueError, TypeError) as err:
            _LOGGER.error(
                "Error interpolating value from %s: %s",
                self._source_entity,
                err,
            )
            self._attr_native_value = None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        source_state = self.hass.states.get(self._source_entity)
        return (
            source_state is not None
            and source_state.state not in ("unknown", "unavailable")
            and self._spline is not None
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "source_entity": self._source_entity,
            "x_values": self._x_values,
            "y_values": self._y_values,
            "interpolation_method": "cubic_spline",
            "boundary_condition": self._boundary_condition,
        }
