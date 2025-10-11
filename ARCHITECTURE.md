# Integration Flow Diagram

## Data Flow

```
┌────────────────────────────────────────────────────────────────┐
│                     Home Assistant Core                        │
│                                                                │
│  ┌──────────────────┐                                          │
│  │  Source Entity   │ (e.g., sensor.raw_temperature)           │
│  │  State: 15.5°C   │                                          │
│  └────────┬─────────┘                                          │
│           │ State Change Event                                 │
│           │                                                    │
│           ▼                                                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Interpolation Sensor                           │    │
│  │                                                        │    │
│  │  ┌─────────────────────────────────────────────────┐   │    │
│  │  │  Configuration                                  │   │    │
│  │  │  x_values: [0, 10, 20, 30, 40]                  │   │    │
│  │  │  y_values: [0.5, 10.2, 20.1, 30.3, 40.5]        │   │    │
│  │  └─────────────────────────────────────────────────┘   │    │
│  │                      ▼                                 │    │
│  │  ┌─────────────────────────────────────────────────┐   │    │
│  │  │  Cubic Spline Function                          │   │    │
│  │  │  Input:  x = 15.5                               │   │    │
│  │  │  Process: Evaluate spline at x=15.5             │   │    │
│  │  │  Output: y = 15.11                              │   │    │
│  │  └─────────────────────────────────────────────────┘   │    │
│  │                      ▼                                 │    │
│  │  ┌─────────────────────────────────────────────────┐   │    │
│  │  │  Sensor State Update                            │   │    │
│  │  │  State: 15.11°C                                 │   │    │
│  │  └─────────────────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Cubic Spline Visualization

```
Y
│
50│                                          * (40, 50)
  │                                      ╱
45│                              * (30, 45)
  │                          ╱╱╱
40│                  * (20, 40)
  │              ╱╱╱
35│          ╱╱╱
  │      ╱╱╱
30│  ╱╱╱
  │╱╱
25│* (10, 25)
  │
20│
  │
15│
  │
10│
  │
 5│
  │
 0│* (0, 0)
  └───────────────────────────────────────────────── X
  0   10   20   30   40

* = Data points
╱ = Cubic spline curve

The cubic spline creates a smooth curve through all data points,
ensuring continuous first and second derivatives.
```

## Component Interaction

```
┌────────────────────┐
│  configuration.yaml│
│                    │
│  sensor:           │
│    - platform:     │
│      interpolation │
│      ...           │
└─────────┬──────────┘
          │ Loaded at startup
          ▼
┌─────────────────────────────────────┐
│  __init__.py                        │
│  - async_setup()                    │
│  - Registers sensor platform        │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  sensor.py                          │
│  - async_setup_platform()           │
│  - Validates configuration          │
│  - Creates InterpolationSensor      │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  InterpolationSensor                │
│                                     │
│  1. __init__():                     │
│     - Create CubicSpline            │
│     - Store configuration           │
│                                     │
│  2. async_added_to_hass():          │
│     - Register event listener       │
│     - Initialize state              │
│                                     │
│  3. sensor_state_listener():        │
│     - Receive state updates         │
│     - Call _update_value()          │
│                                     │
│  4. _update_value():                │
│     - Convert state to float        │
│     - Evaluate spline               │
│     - Update sensor state           │
└─────────────────────────────────────┘
```

## Lifecycle

```
┌─────────────────────┐
│  Integration Setup  │
│  (Home Assistant    │
│   starts)           │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│  Load Configuration  │
│  - Parse YAML        │
│  - Validate schema   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Create Sensor       │
│  - Build CubicSpline │
│  - Register entity   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Add to HA           │
│  - Register listener │
│  - Init state        │
└──────────┬───────────┘
           │
           ▼
      ┌────────────┐
      │  Running   │◄───────┐
      │  - Monitor │        │
      │  - Update  │        │
      └────────────┘        │
           │                │
           │ State change   │
           └────────────────┘
           │
           ▼
┌──────────────────────┐
│  Shutdown            │
│  - Clean up listener │
└──────────────────────┘
```

## State Update Sequence

```
1. Source entity changes
   sensor.raw_temperature: 15.0 → 15.5

2. Event fired
   event_type: state_changed
   entity_id: sensor.raw_temperature
   new_state: 15.5

3. Listener callback
   sensor_state_listener(event)

4. Value extraction
   new_state.state = "15.5"

5. Type conversion
   x = float("15.5") = 15.5

6. Interpolation
   y = spline(15.5) = 15.11

7. State update
   self._attr_native_value = 15.11

8. Notify Home Assistant
   self.async_write_ha_state()

9. New state available
   sensor.corrected_temperature: 15.11
```
