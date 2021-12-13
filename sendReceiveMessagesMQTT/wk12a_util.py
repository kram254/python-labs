import random



start_id= 420
def create_data():
    global start_id
    power = ["250.1 KW @ 5300-6400 RPM", "340 HP @ 5300-6400 RPM", "335 BHP @ 5300-6400 RPM"]
    start_id += 1
    payload = {"id": start_id,"brandName": "VW TUAREG","cylinders": "V6",  "turboCharged": random.choice(["YES", "NO"]), 
    "myResult": {"acceleration": random.randint(0,6.2), "allWheelDrive": random.choice(["YES", "NO"]),
 "power": random.choice(power), "min": random.randint(5300,5500), "max": random.randint(6400,6700)}}
    return payload


def print_data(payload):
    print("Message ID: {}\n"\
    "Brand name: {}\n"\
    "Cylinders: {}\n"\
    "Turbo Charged: {}\n"\
    "Acceleration Time: {}\n"\
    "All Wheel Drive: {}\n"\
    "Power: {}\n"\
    "Minimum RPM: {}\n"\
    "Maximum RPM: {}\n"\
    .format(payload.get("id"),
    payload.get("brandName"),
    payload.get("cylinders"),
    payload.get("turboCharged"),
    payload["myResult"].get("acceleration"),
    payload["myResult"].get("allWheelDrive"),
    payload["myResult"].get("power"),
    payload["myResult"].get("min"),
    payload["myResult"].get("max")))