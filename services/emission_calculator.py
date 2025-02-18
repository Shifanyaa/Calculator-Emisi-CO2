import os
import json
from models.request import VehicleEmissionRequest, MachineEmissionRequest
from fastapi import HTTPException
from utils.validation import validate_source_type, validate_fuel_type, validate_vehicle_type, load_factors, emission_factors

class EmissionCalculator:
    def __init__(self, data):
        self.data = data

    def calculate_emissions(self) -> float:
        raise NotImplementedError("Subclasses should implement this method")

class VehicleEmissionCalculator(EmissionCalculator):
    def calculate_emissions(self) -> float:
        total_emissions = 0
        validate_fuel_type(self.data.fuelType)

        for trip in self.data.tripData:
            validate_vehicle_type(trip.vehicleType)
            if trip.vehicleType not in load_factors:
                raise HTTPException(status_code=400, detail="Invalid vehicle type")
            if self.data.fuelType not in emission_factors:
                raise HTTPException(status_code=400, detail="Invalid fuel type")

            load_factor = load_factors[trip.vehicleType]
            adjusted_fuel_consumed = trip.fuelConsumed * (1 + load_factor * (trip.loadWeight / 1000))
            activity_data = adjusted_fuel_consumed * trip.distance
            emission_factor = emission_factors[self.data.fuelType]
            emissions = activity_data * emission_factor

            total_emissions += emissions

        return total_emissions

class MachineEmissionCalculator(EmissionCalculator):
    def calculate_emissions(self) -> float:
        total_emissions = 0
        validate_fuel_type(self.data.fuelType)

        for trip in self.data.tripData:
            if trip.fuelConsumed <= 0 or trip.productionCapacityLoad <= 0:
                raise HTTPException(status_code=400, detail="Fuel consumed and production capacity must be positive")
            if self.data.fuelType not in emission_factors:
                raise HTTPException(status_code=400, detail="Invalid fuel type")

            activity_data = trip.fuelConsumed * (trip.machineEficiency / 100) * trip.productionCapacityLoad
            emission_factor = emission_factors[self.data.fuelType]
            emissions = activity_data * emission_factor

            total_emissions += emissions

        return total_emissions