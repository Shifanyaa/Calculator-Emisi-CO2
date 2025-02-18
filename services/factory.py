from typing import Union
from fastapi import HTTPException
from models.request import VehicleEmissionRequest, MachineEmissionRequest
from services.emission_calculator import EmissionCalculator, VehicleEmissionCalculator, MachineEmissionCalculator

class EmissionCalculatorFactory:
    @staticmethod
    def get_emission_calculator(emission_request):
        if isinstance(emission_request, VehicleEmissionRequest) and emission_request.sourceType == "vehicle":
            return VehicleEmissionCalculator(emission_request)
        elif isinstance(emission_request, MachineEmissionRequest) and emission_request.sourceType == "machine":
            return MachineEmissionCalculator(emission_request)
        else:
            raise HTTPException(status_code=400, detail="Invalid emission request")

