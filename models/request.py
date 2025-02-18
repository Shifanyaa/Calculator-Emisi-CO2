from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from fastapi import HTTPException

class EmissionRequest(BaseModel):
    sourceType: str = Field(..., pattern="^(vehicle|machine)$", description="Must be either 'vehicle' or 'machine'")
    fuelType: str
    unit: Optional[str] = None

    # @classmethod
    # def from_union(cls, data):
    #     # Implement the logic to create an instance from the provided data
    #     return cls(**data)

    model_config = ConfigDict(extra="forbid") 

class VehicleTrip(BaseModel):
    vehicleType: str
    fuelConsumed: float = Field(..., gt=0, description="Fuel consumed must be positive")
    distance: float = Field(..., ge=0, description="Distance must be positive")
    loadWeight: float = Field(..., ge=0, description="Load weight must be non-negative")

class MachineTrip(BaseModel):
    fuelConsumed: float = Field(..., gt=0) 
    machineEficiency: float = Field(..., ge=0, le=100)
    productionCapacityLoad: float = Field(..., gt=0)

class VehicleEmissionRequest(EmissionRequest):
    tripData: List[VehicleTrip]

class MachineEmissionRequest(EmissionRequest):
    tripData: List[MachineTrip]