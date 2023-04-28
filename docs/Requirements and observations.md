# Conditions and exceptions:
## Heating is on
    - 0.5 = room_temperature += 0.5
    - 0.2 = room_temperature += 1
    - 0.2 = room_temperature = room_temperature
    - 0.1 = room_temperature -= 0.5
### Exceptions:
    - If temperature == 16:
        - 0.3 = room_temperature = room_temperature
        - 0.5 = room_temperature += 0.5
        - 0.2 = room_temperature += 1
    - If temperature == 25:
        - 0.1 = room_temperature -= 0.5
        - 0.9 = room_temperature = room_temperature
    - If temperature == 24.5:
        - 0.7 = room_temperature += 0.5
        - 0.2 = room_temperature = room_temperature
        - 0.1 = room_temperature -= 0.5

## Heating is off
    - 0.7 = room_temperature -= 0.5
    - 0.1 = room_temperature += 0.5
    - 0.2 = room_temperature = room_temperature

### Exceptions:
    - If temperature == 16:
        - 0.9 = room_temperature = room_temperature
        - 0.1 = room_temperature += 0.5
    - If temperature == 25:
        - 0.3 = room_temperature = room_temperature
        - 0.7 = room_temperature -= 0.5

Instead of activating the thermostat every time the temperature is off, we will have a margin of 1 degree, where the temperature is not activated.