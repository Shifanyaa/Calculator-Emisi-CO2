from fastapi import HTTPException
from models.emission_request import EmissionRequest, MachineEmissionRequest
import json
import os

# ambil data faktor emisi json
json_file_path = "D:/Project Intern/emission_data.json"

# periksa json
with open(json_file_path, "r") as f:
    content = f.read()
    if content.strip():  
        emissionData = json.loads(content)
    else:
        raise ValueError("The JSON file is empty")

# Error handling untuk source type
def validate_source_type(source_type: str):
    allowed_types = ["vehicle", "machine"]
    if source_type not in allowed_types:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "Unsupported emission source type",
            "details": {
                "sourceType": source_type,
                "allowedTypes": allowed_types
            }
        })

# Error handling untuk fuel type
def validate_fuel_type(fuel_type: str):
    if fuel_type not in emissionData:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Unsupported fuel type",
            "details": {
                "fuelType": fuel_type,
                "allowedTypes": list(emissionData.keys())
            }
        })

# Class untuk menghitung emisi
class EmissionCalculator:
    def __init__(self, data: EmissionRequest):
        self.data = data

    def calculate_emissions(self) -> float:
        raise NotImplementedError("Subclasses should implement this method")

# Class untuk menghitung emisi kendaraan
class VehicleEmissionCalculator(EmissionCalculator):
    def calculate_emissions(self) -> float:
        total_emissions = 0
        for trip in self.data.tripData:
            distance, load_weight = trip.distance, trip.loadWeight
            weight_factor = 1 + (load_weight / 100) * 0.005
            fuel_consumption = (distance / 100) * weight_factor
            emissions = fuel_consumption * emissionData[self.data.fuelType]
            total_emissions += emissions
        return total_emissions

# Class untuk menghitung emisi mesin
class MachineEmissionCalculator(EmissionCalculator):
    def __init__(self, data: MachineEmissionRequest):
        self.data = data

    def calculate_emissions(self) -> float:
        total_emissions = 0
        for trip in self.data.tripData:
            duration_hours = trip.duration / 60  # Convert duration from minutes to hours
            load = trip.load
            load_factor = 1 + (load / 100) * 0.01  # Different factor for machines
            fuel_consumption = duration_hours * load_factor  # Use duration in hours and load factor
            emissions = fuel_consumption * emissionData[self.data.fuelType]
            total_emissions += emissions
        return total_emissions

# Fungsi untuk mendapatkan kalkulator emisi
def get_emission_calculator(data: EmissionRequest) -> EmissionCalculator:
    if data.sourceType == "vehicle":
        return VehicleEmissionCalculator(data)
    elif data.sourceType == "machine":
        machine_data = MachineEmissionRequest(**data.dict())
        return MachineEmissionCalculator(machine_data)
    else:
        raise HTTPException(status_code=400, detail="Unsupported source type")