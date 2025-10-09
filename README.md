# homeassistant-interpolation
Home Assistant integration performing interpolation

## Overview

This custom integration provides a sensor that performs cubic spline interpolation between a set of data points. It takes a numeric entity as input (x value) and outputs the interpolated value (y value) based on a discrete set of (x, y) pairs.

## Features

- Uses scipy's CubicSpline for smooth interpolation
- Supports arbitrary number of data points (minimum 2)
- Automatically updates when the source entity changes
- Validates input data (x values must be strictly increasing)
- Provides detailed state attributes

## Installation

1. Copy the `custom_components/interpolation` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the configuration to your `configuration.yaml`

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: interpolation
    name: "My Interpolation Sensor"
    source_entity: sensor.input_value
    x_values: [0, 10, 20, 30, 40]
    y_values: [0, 25, 40, 45, 50]
    unit_of_measurement: "°C"
```

### Configuration Variables

- **source_entity** (required): The entity ID of the numeric sensor to use as the x value
- **x_values** (required): List of x values for interpolation (must be strictly increasing)
- **y_values** (required): List of y values corresponding to x values (must have same length as x_values)
- **name** (optional): Name of the sensor (default: "Interpolation")
- **unique_id** (optional): A unique ID for the sensor
- **unit_of_measurement** (optional): Unit of measurement for the output value

## Example Use Cases

### Temperature Correction
Correct temperature readings from a sensor based on calibration points:

```yaml
sensor:
  - platform: interpolation
    name: "Corrected Temperature"
    source_entity: sensor.raw_temperature
    x_values: [0, 10, 20, 30, 40]
    y_values: [0.5, 10.2, 20.1, 30.3, 40.5]
    unit_of_measurement: "°C"
```

### Fan Speed Control
Map a linear input to a non-linear fan speed curve:

```yaml
sensor:
  - platform: interpolation
    name: "Fan Speed Curve"
    source_entity: input_number.fan_control
    x_values: [0, 25, 50, 75, 100]
    y_values: [0, 10, 30, 70, 100]
    unit_of_measurement: "%"
```

### Battery Voltage to Percentage
Convert battery voltage to percentage:

```yaml
sensor:
  - platform: interpolation
    name: "Battery Percentage"
    source_entity: sensor.battery_voltage
    x_values: [3.0, 3.3, 3.6, 3.9, 4.2]
    y_values: [0, 25, 50, 75, 100]
    unit_of_measurement: "%"
```

## How It Works

The integration uses scipy's CubicSpline interpolation, which creates a smooth curve through the provided data points. For any input value (x), the sensor calculates the corresponding output value (y) along this curve.

- If the input is within the range of x_values, the value is interpolated
- If the input is outside the range, the value is extrapolated using the cubic spline

## State Attributes

The sensor provides the following attributes:

- **source_entity**: The entity ID being monitored
- **x_values**: The x values used for interpolation
- **y_values**: The y values used for interpolation
- **interpolation_method**: Always "cubic_spline"

## Requirements

- Home Assistant 2021.12 or later
- scipy >= 1.7.0 (automatically installed)
