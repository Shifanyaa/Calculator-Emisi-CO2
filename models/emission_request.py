from pydantic import BaseModel
from typing import List, Optional

class TripData(BaseModel):
    distance: float
    loadWeight: float

class MachineTrip(BaseModel):
    duration: float  # Duration of usage in minutes
    load: float  # Load of the machine in weight

class EmissionRequest(BaseModel):
    sourceType: str
    fuelType: str
    tripData: List[TripData]
    unit: Optional[str] = None  # Make the unit field optional

class MachineEmissionRequest(BaseModel):
    sourceType: str
    fuelType: str
    tripData: List[MachineTrip]
    unit: Optional[str] = None  # Make the unit field optional