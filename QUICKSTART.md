# Quick Start Guide

## Installation

1. Copy the `custom_components/interpolation` directory to your Home Assistant's `custom_components` directory:

   ```
   /config/custom_components/interpolation/
   ```

2. Restart Home Assistant

3. Add configuration to `configuration.yaml`

4. Restart Home Assistant again or reload YAML configuration via Developer Tools → YAML → Reload "Manually configured YAML entities"

## Basic Configuration

```yaml
sensor:
  - platform: interpolation
    name: "Interpolated Sensor"
    source_entity: sensor.source
    x_values: [0, 10, 20, 30, 40]
    y_values: [0, 25, 40, 45, 50]
```

## Step-by-Step Example

### Scenario: Temperature Calibration

You have a temperature sensor (`sensor.raw_temperature`) that reads inaccurately.
You've measured the actual temperature at several points:

| Raw Reading | Actual Temperature|
|-------------|-------------------|
| 0°C         | 0.5°C             |
| 10°C        | 10.2°C            |
| 20°C        | 20.1°C            |
| 30°C        | 30.3°C            |
| 40°C        | 40.5°C            |

### Configuration

```yaml
sensor:
  - platform: interpolation
    name: "Corrected Temperature"
    source_entity: sensor.raw_temperature
    x_values: [0, 10, 20, 30, 40]
    y_values: [0.5, 10.2, 20.1, 30.3, 40.5]
    unit_of_measurement: "°C"
    unique_id: "corrected_temperature_01"
```

### Result

- When `sensor.raw_temperature` shows 15°C
- `sensor.corrected_temperature` will automatically update to ~15.1°C
- The interpolation creates a smooth curve through your calibration points

## Common Use Cases

### 1. Battery Voltage to Percentage

```yaml
sensor:
  - platform: interpolation
    name: "Battery Percentage"
    source_entity: sensor.battery_voltage
    x_values: [3.0, 3.3, 3.6, 3.9, 4.2]
    y_values: [0, 25, 50, 75, 100]
    unit_of_measurement: "%"
```

### 2. Non-Linear Fan Control

```yaml
sensor:
  - platform: interpolation
    name: "Fan Speed"
    source_entity: input_number.fan_slider
    x_values: [0, 25, 50, 75, 100]
    y_values: [0, 10, 30, 70, 100]
    unit_of_measurement: "%"
```

### 3. Light Brightness Curve

```yaml
sensor:
  - platform: interpolation
    name: "Light Brightness"
    source_entity: input_number.brightness
    x_values: [0, 20, 40, 60, 80, 100]
    y_values: [0, 5, 15, 35, 65, 100]
    unit_of_measurement: "%"
```

## Using the Sensor

Once configured, you can:

### In Automations

```yaml
automation:
  - alias: "Adjust based on corrected temperature"
    trigger:
      - platform: numeric_state
        entity_id: sensor.corrected_temperature
        above: 25
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.ac
        data:
          temperature: 20
```

### In Lovelace Cards

```yaml
type: entities
entities:
  - entity: sensor.raw_temperature
    name: "Raw Temperature"
  - entity: sensor.corrected_temperature
    name: "Corrected Temperature"
```

### In Templates

```yaml
sensor:
  - platform: template
    sensors:
      temperature_status:
        value_template: >
          {% if states('sensor.corrected_temperature') | float > 25 %}
            Hot
          {% else %}
            Cool
          {% endif %}
```

## Troubleshooting

### Sensor shows "unavailable"

- Check that source entity exists and has a numeric value
- Verify x_values are strictly increasing
- Ensure x_values and y_values have the same length

### Unexpected output values

- Check your x_values and y_values are correct
- Remember: cubic spline can extrapolate beyond your data range
- Verify the source entity value is within or near your x_values range

### Integration not loading

- Check Home Assistant logs for errors
- Ensure the directory structure is correct

## Configuration Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `source_entity` | Yes | string | Entity ID to monitor |
| `x_values` | Yes | list of floats | X coordinates (strictly increasing) |
| `y_values` | Yes | list of floats | Y coordinates (same length as x_values) |
| `name` | No | string | Sensor name (default: "Interpolation") |
| `unique_id` | No | string | Unique identifier for the sensor |
| `unit_of_measurement` | No | string | Unit for the output value |
| `boundary_condition` | No | string | Boundary condition type: `not-a-knot` (default), `natural`, `clamped`, or `periodic` |

## Tips

1. **More points = smoother curve**: Add more calibration points for better accuracy
2. **Minimum 2 points**: You need at least 2 data points to create an interpolation
3. **Strictly increasing**: X values must be in ascending order with no duplicates
4. **Extrapolation**: The sensor works outside your data range, but accuracy decreases
5. **Unique IDs**: Use unique_id for entity customization in the UI
6. **Boundary conditions**: Use `natural` for linear extrapolation, `clamped` for flat endpoints, or `periodic` for repeating patterns

## Next Steps

- See [README.md](README.md) for detailed information
- Check [TECHNICAL.md](TECHNICAL.md) for implementation details
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Examine [example_configuration.yaml](example_configuration.yaml) for more examples
