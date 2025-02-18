import os
import json
from fastapi import HTTPException

current_dir = os.path.dirname(__file__)

def load_json(filename):
    path = os.path.abspath(os.path.join(current_dir, filename))
    if not os.path.exists(path):
        raise FileNotFoundError(f"The JSON file {filename} was not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError(f"The JSON file {filename} is empty")
        return json.loads(content)

try:
    emission_factors = load_json("../emissionFactor.json")
    load_factors = load_json("../loadFactor.json")
    print("Emission factors and load factors loaded successfully")
except (FileNotFoundError, ValueError) as e:
    raise HTTPException(status_code=500, detail={
        "status": "error",
        "message": str(e)
    })

# Validasi sourceType
def validate_source_type(source_type: str):
    allowed_types = ["vehicle", "machine"]
    if source_type not in allowed_types:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Unsupported emission source type",
            "details": {
                "sourceType": source_type,
                "allowedTypes": allowed_types
            }
        })

# Validasi fuelType
def validate_fuel_type(fuel_type: str):
    if fuel_type not in emission_factors:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Unsupported fuel type",
            "details": {
                "fuelType": fuel_type,
                "allowedTypes": list(emission_factors.keys())
            }
        })

# Validasi vehicleType
def validate_vehicle_type(vehicle_type: str):
    if vehicle_type not in load_factors:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Unsupported vehicle type for load factor",
            "details": {
                "vehicleType": vehicle_type,
                "allowedTypes": list(load_factors.keys())
            }
        })
