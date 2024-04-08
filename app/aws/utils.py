import sys
sys.path.append(sys.path[0] + "/app/aws")
import random
import time
import random
import hashlib

def generate_random_data(year:int):
    # Generate energy_produced_data
    energy_produced_data = [random.randint(500, 1500) for _ in range(12)]
    
    # Generate carbon_generated_data
    carbon_generated_data = [random.randint(80, 300) for _ in range(12)]
    
    # Generate energy_consumed_data
    energy_consumed_data = [int(energy_produced * (0.8 + random.random() * 0.2)) for energy_produced in energy_produced_data]
    
    energy_produced_data = list(map(str, energy_produced_data))
    carbon_generated_data = list(map(str, carbon_generated_data))
    energy_consumed_data = list(map(str, energy_consumed_data))
    return { 'year':year, 'energy_produced': energy_produced_data, 'carbon_generated': carbon_generated_data, 'energy_consumed': energy_consumed_data}


def energy_consumption_data ():
    return[
    {
        "name": "Residential Sector",
        "y": str(round(random.uniform(10, 30), 2))  # realistic range for residential sector consumption
    },
    {
        "name": "Commercial Sector",
        "y": str(round(random.uniform(10, 25), 2))  # realistic range for commercial sector consumption
    },
    {
        "name": "Industrial Sector",
        "y": str(round(random.uniform(15, 35), 2))  # realistic range for industrial sector consumption
    },
    {
        "name": "Transportation Sector",
        "y": str(round(random.uniform(20, 40), 2))  # realistic range for transportation sector consumption
    },
    {
        "name": "Other (Agriculture, etc.)",
        "y": str(round(random.uniform(5, 20), 2))  # realistic range for other sectors consumption
    }
]

# Function to calculate total consumption and adjust values to ensure total is 100%
def adjust_values_to_sum_to_100(data):
    total = sum(float(item["y"]) for item in data)
    adjustment_factor = 100 / total if total != 0 else 0
    for item in data:
        item["y"] = str(round(float(item["y"]) * adjustment_factor, 2))  # Round to two decimal points and convert to string
    return data

# Call the function to adjust values
def adjusted_data(state,year):
    return {
        'id':generate_object_id(),
        'state':state,
        'year':year,
        'energy_consumption': adjust_values_to_sum_to_100(energy_consumption_data()),
        'energy_production': adjust_values_to_sum_to_100(energy_consumption_data()),
        'carbon_generation': adjust_values_to_sum_to_100(energy_consumption_data()),
    }
def generate_object_id():
    timestamp = int(time.time())  # Get current timestamp
    counter = random.randint(0, 16777215)  # Random 3-byte counter
    machine_id = random.randint(0, 4095)  # Random 2-byte machine identifier

    # Combine timestamp, counter, and machine id into bytes
    id_bytes = timestamp.to_bytes(4, byteorder='big') + \
            machine_id.to_bytes(2, byteorder='big') + \
            counter.to_bytes(3, byteorder='big')

    # Generate MD5 hash of the bytes
    hash_bytes = hashlib.md5(id_bytes).digest()

    # Return the hexadecimal representation of the hash
    return hash_bytes.hex()


# Output the adjusted data

