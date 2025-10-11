# homeassistant-interpolation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/JoshuaLampert/homeassistant-interpolation.svg)](https://github.com/JoshuaLampert/homeassistant-interpolation/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Home Assistant integration performing cubic spline interpolation.

## Overview

This custom integration provides a sensor that performs cubic spline interpolation between a set of data points. It takes a numeric entity as input (x value) and outputs the interpolated value (y value) based on a discrete set of (x, y) pairs.

## Features

- Uses [scipy's `CubicSpline`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html) for smooth interpolation
- Supports arbitrary number of data points (minimum 2)
- Automatically updates when the source entity changes
- Validates input data (x values must be strictly increasing)

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/JoshuaLampert/homeassistant-interpolation` as an integration
5. Click "Install" on the Interpolation integration
6. Restart Home Assistant
7. Add the configuration to your `configuration.yaml`

### Manual Installation

1. Copy the `custom_components/interpolation` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the configuration to your `configuration.yaml`

## Configuration

The following provides an example configuration:

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
- **boundary_condition** (optional): Boundary condition type for the cubic spline (default: "not-a-knot")
  - `not-a-knot`: Default option, good when there is no information on boundary conditions
  - `natural`: Second derivative at curve ends are zero
  - `clamped`: First derivative at curve ends are zero
  - `periodic`: Assumes the function is periodic (first and last y values must be identical)

## Example Use Cases

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

## How It Works

The integration uses [scipy's `CubicSpline`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html) interpolation, which creates a smooth curve through the provided data points. For any input value (x), the sensor calculates the corresponding output value (y) along this curve.

- If the input is within the range of x_values, the value is interpolated
- If the input is outside the range, the value is extrapolated using the cubic spline

### Boundary Conditions

The `boundary_condition` parameter controls how the cubic spline behaves at the endpoints of your data. This is important because it affects the shape of the curve, especially for extrapolation beyond your data range.

Available boundary conditions:

- **not-a-knot** (default): The first and second segments at each end are the same polynomial. This is a good default when you don't have specific requirements for the endpoints. It produces natural-looking curves.

- **natural**: The second derivative at both endpoints is zero. This creates a curve that "straightens out" at the ends, which is useful when you expect the function to become linear beyond your data range.

- **clamped**: The first derivative at both endpoints is zero. This means the curve has zero slope at the ends, creating a "flat" approach to the endpoints. Useful when you know the rate of change should be zero at the boundaries.

- **periodic**: Assumes the function is periodic with period `x[-1] - x[0]`. The first and last y values must be identical. This ensures smooth transitions when the data represents a repeating pattern (e.g., seasonal data).

Example with natural boundary condition:
```yaml
sensor:
  - platform: interpolation
    name: "Temperature with Natural BC"
    source_entity: sensor.raw_temperature
    x_values: [0, 10, 20, 30, 40]
    y_values: [0.5, 10.2, 20.1, 30.3, 40.5]
    boundary_condition: natural
    unit_of_measurement: "°C"
```

## Comparison with Compensation Integration

Home Assistant includes a built-in [Compensation integration](https://www.home-assistant.io/integrations/compensation/) that also transforms sensor values based on calibration data. Here's how they differ:

**Similarities:**
- Both correct/transform sensor values using data points
- Both monitor a source entity and update automatically
- Both support configurable units of measurement

**Differences:**
- **Interpolation Method**: Compensation uses polynomial fitting, while this integration uses cubic spline interpolation. This also means Compensation is not guaranteed to exactly match the input data, while this integration is.
- **Smoothness**: Cubic splines guarantee smooth first and second derivatives at data points, while high-degree polynomials can create unwanted oscillations between data points (Runge's phenomenon)
- **Accuracy**: Polynomial fitting in the Compensation integration can have huge errors for certain functions, especially when using many calibration points, whereas cubic splines remain stable and accurate
- **Data Point Requirements**: Compensation requires specific polynomial degrees, while this integration works with any number of points (≥2)
- **Extrapolation**: Cubic splines generally extrapolate more predictably than high-degree polynomials

**When to use this integration:**
- You want guaranteed smoothness between data points
- You have many calibration points and need to avoid polynomial oscillation and large interpolation errors
- You want to exactly match the input data
- Your use case is sensitive to accuracy and stability

**When to use Compensation:**
- You prefer a built-in Home Assistant integration
- Polynomial fitting is sufficient for your use case
- You want simpler configuration with degree specification

## State Attributes

The sensor provides the following attributes:

- **source_entity**: The entity ID being monitored
- **x_values**: The x values used for interpolation
- **y_values**: The y values used for interpolation
- **interpolation_method**: Always "cubic_spline"
- **boundary_condition**: The boundary condition type used ("not-a-knot", "natural", "clamped", or "periodic")

## Disclaimer

Please note that large parts of this integration are written by GitHub Copilot, see [this PR](https://github.com/JoshuaLampert/homeassistant-interpolation/pull/1).
I have checked the implementation and tested the integration though. However, I do not extend any warranty. Use at your own risk!

## License and contributing

This project is under the MIT License (see [License](https://github.com/JoshuaLampert/homeassistant-interpolation/blob/main/LICENSE)).
I am pleased to accept contributions from everyone, preferably in the form of a PR.

## Support

For issues, questions, or contributions, please [open an issue](https://github.com/JoshuaLampert/homeassistant-interpolation/issues)
or [create a pull request](https://github.com/JoshuaLampert/homeassistant-interpolation/pulls).
