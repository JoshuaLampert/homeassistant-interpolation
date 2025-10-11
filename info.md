# Interpolation

This integration provides cubic spline interpolation for Home Assistant sensors.

## Features

✅ **Smooth Interpolation** - Uses scipy's CubicSpline for mathematically accurate interpolation  
✅ **Flexible Configuration** - Supports any number of data points (minimum 2)  
✅ **Multiple Boundary Conditions** - Choose from not-a-knot, natural, clamped, or periodic  
✅ **Automatic Updates** - Sensor updates automatically when source entity changes  
✅ **Data Validation** - Ensures x values are strictly increasing  

## Use Cases

- **Temperature Calibration** - Correct sensor readings based on known calibration points
- **Battery Voltage Conversion** - Convert voltage to percentage using discharge curves
- **Non-linear Mapping** - Map fan speeds, light brightness, or other controls
- **Sensor Correction** - Fix any sensor with known error patterns

## Configuration

```yaml
sensor:
  - platform: interpolation
    name: "My Interpolation Sensor"
    source_entity: sensor.input_value
    x_values: [0, 10, 20, 30, 40]
    y_values: [0, 25, 40, 45, 50]
    boundary_condition: not-a-knot  # optional
    unit_of_measurement: "°C"  # optional
```

## Advantages over Compensation Integration

Unlike the built-in Compensation integration which uses polynomial fitting:
- ✅ Guaranteed to pass through all data points exactly
- ✅ No oscillations between data points (avoids Runge's phenomenon)
- ✅ More stable and accurate with many calibration points
- ✅ Smooth first and second derivatives

## Documentation

For detailed documentation, examples, and troubleshooting, see the [GitHub repository](https://github.com/JoshuaLampert/homeassistant-interpolation).
