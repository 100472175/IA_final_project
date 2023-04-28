
DESIRED_TEMP = 22
POSSIBLE_TEMPERATURES = range(16, 25)
TEMPERATURE_STEP = 0.5
TEMPERATURE_STEP_TIME = 0.5


"""
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
"""

prompt = "Enter the desired temperature(Default temperature is %i): " % DESIRED_TEMP
user_temperature = input(prompt)
if user_temperature == "":
    user_temperature = DESIRED_TEMP

# Instead of waiting for half-hour intervals, we will do 5 second intervals
# to speed up the process

# We will use a while loop to simulate the passing of time
for i in range(10):
    print(random())