from fastapi import APIRouter, HTTPException, Depends
from models.request import VehicleEmissionRequest, MachineEmissionRequest
from services.factory import EmissionCalculatorFactory
from typing import Union

router = APIRouter()

@router.post("/calculate-emissions")
async def calculate_emissions(emission_request: Union[VehicleEmissionRequest, MachineEmissionRequest]):
    if not isinstance(emission_request, (VehicleEmissionRequest, MachineEmissionRequest)):
        raise HTTPException(status_code=400, detail="Invalid emission request type")

    calculator = EmissionCalculatorFactory.get_emission_calculator(emission_request)
    total_emissions = calculator.calculate_emissions()
    return {"total_emissions": total_emissions}
