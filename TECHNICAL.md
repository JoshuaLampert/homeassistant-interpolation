# Technical Documentation

## Implementation Details

### Overview
This Home Assistant integration implements cubic spline interpolation using scipy's `CubicSpline` class. The integration creates a sensor that monitors a source entity and applies interpolation based on provided data points.

### Architecture

#### Components

1. **`__init__.py`** - Integration setup and entry point
   - Registers the sensor platform
   - Handles async setup
   - Manages domain data

2. **`sensor.py`** - Core interpolation sensor implementation
   - Defines configuration schema
   - Validates input data
   - Creates and manages interpolation sensor entities
   - Handles state updates from source entity

3. **`manifest.json`** - Integration metadata
   - Declares scipy dependency
   - Specifies IoT class as "calculated"
   - Provides integration information

4. **`strings.json`** - Localization strings
   - UI text for configuration

### Cubic Spline Interpolation

The integration uses scipy's `CubicSpline` which:
- Creates a piecewise cubic polynomial between data points
- Ensures continuity up to the second derivative
- Provides smooth interpolation and extrapolation
- Supports both interpolation (within range) and extrapolation (outside range)

### Configuration

The sensor is configured via YAML in `configuration.yaml`:

```yaml
sensor:
  - platform: interpolation
    name: "Sensor Name"
    source_entity: sensor.source
    x_values: [x1, x2, x3, ...]
    y_values: [y1, y2, y3, ...]
    unit_of_measurement: "unit"  # optional
    unique_id: "unique_id"       # optional
```

#### Configuration Validation

The integration validates:
1. **Length matching**: x_values and y_values must have equal length
2. **Minimum points**: At least 2 data points required
3. **Monotonicity**: x_values must be strictly increasing
4. **Entity ID**: source_entity must be a valid entity ID

### Sensor Behavior

#### State Updates
- The sensor listens to state changes of the source entity
- When the source entity updates, the sensor:
  1. Reads the new state value
  2. Converts it to a float (x value)
  3. Evaluates the cubic spline at that x value
  4. Updates its own state with the result (y value)

#### Error Handling
- If source entity is unavailable or unknown, sensor becomes unavailable
- If source value cannot be converted to float, sensor becomes unavailable
- Validation errors during setup prevent sensor creation with error logging

#### State Attributes

The sensor provides these attributes:
- `source_entity`: The entity being monitored
- `x_values`: The x values used for interpolation
- `y_values`: The y values used for interpolation
- `interpolation_method`: Always "cubic_spline"

### Performance Considerations

1. **Initialization**: Cubic spline is created once during sensor initialization
2. **Updates**: Each state change requires only one function evaluation O(1)
3. **Memory**: Stores coefficients for piecewise polynomials
4. **Scipy Dependency**: Uses optimized C/Fortran libraries for performance

### Use Cases

The integration is designed for scenarios where:
- Sensor readings need calibration/correction
- Non-linear mappings are required
- Smooth transitions between discrete points are desired

Examples:
- Temperature sensor calibration
- Battery voltage to percentage conversion
- Fan speed curves
- Light brightness mapping
- Pressure sensor linearization

### Integration with Home Assistant

#### Platform Type
- Implements as a sensor platform (read-only)
- No config flow (YAML configuration only)
- No persistent storage required

#### Dependencies
- scipy >= 1.7.0 (for CubicSpline)
- Standard Home Assistant core components
- voluptuous for configuration validation

#### Event Handling
- Uses `async_track_state_change_event` for efficient state monitoring
- Properly cleans up event listeners on removal
- Follows Home Assistant async patterns

### Testing

The implementation has been tested for:
- Validation logic (length, minimum points, monotonicity)
- Linear interpolation accuracy
- Non-linear interpolation behavior
- Boundary conditions (at data points)
- Extrapolation (beyond data range)
- Real-world use cases (battery, fan, temperature)

### Future Enhancements

Possible improvements:
- Config flow UI for easier setup
- Additional interpolation methods (linear, quadratic)
- Boundary condition options (natural, clamped, periodic)
- Smoothing parameter for noisy data
- Derivative sensors (rate of change)
- Multi-dimensional interpolation

### Limitations

Current limitations:
- Only 1D interpolation (x -> y)
- YAML configuration only (no UI)
- No input validation for numeric source entity
- Extrapolation may produce unexpected results far from data range

### References

- scipy CubicSpline: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html
- Home Assistant Sensor Platform: https://developers.home-assistant.io/docs/core/entity/sensor
- Home Assistant Integration Development: https://developers.home-assistant.io/docs/creating_component_index
