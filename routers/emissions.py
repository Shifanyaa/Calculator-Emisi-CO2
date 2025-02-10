from fastapi import FastAPI, HTTPException, Request
from models.emission_request import EmissionRequest, MachineEmissionRequest
from services.emission_calculator import get_emission_calculator

app = FastAPI()

@app.post("/calculate-emissions")
async def calculate_emissions(request: Request):
    try:
        data = await request.json()
        if data["sourceType"] == "vehicle":
            emission_request = EmissionRequest(**data)
        elif data["sourceType"] == "machine":
            emission_request = MachineEmissionRequest(**data)
        else:
            raise HTTPException(status_code=400, detail="Unsupported source type")

        calculator = get_emission_calculator(emission_request)
        total_emissions = calculator.calculate_emissions()
        return {"total_emissions": total_emissions}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))