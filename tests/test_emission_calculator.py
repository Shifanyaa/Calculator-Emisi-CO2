import pytest
from services.emission_calculator import VehicleEmissionCalculator
from models.request import VehicleEmissionRequest, VehicleTrip


# test basic calculation
def test_basic_calculation():
    request = VehicleEmissionRequest(sourceType="vehicle", fuelType="bensin", tripData=[
        VehicleTrip(vehicleType="Truk Sedang", fuelConsumed=3, distance=100, loadWeight=500)
    ])
    calculator = VehicleEmissionCalculator(request)
    assert calculator.calculate_emissions() == pytest.approx(861.735)

# test if trip data is empty
def test_empty_trip_data():
    request = VehicleEmissionRequest(sourceType="vehicle", fuelType="bensin", tripData=[])
    calculator = VehicleEmissionCalculator(request)
    assert calculator.calculate_emissions() == 0

# test if just weight load without distance
def test_zero_distance():
    request = VehicleEmissionRequest(sourceType="vehicle", fuelType="bensin", tripData=[
        VehicleTrip(vehicleType="Truk Sedang", fuelConsumed=2, distance=0, loadWeight=500)
    ])
    calculator = VehicleEmissionCalculator(request)
    assert calculator.calculate_emissions() == 0

# test if just distance without weight load
def test_zero_load_weight():
    request = VehicleEmissionRequest(sourceType="vehicle", fuelType="bensin", tripData=[
        VehicleTrip(vehicleType="Truk Sedang", fuelConsumed=0.1, distance=100, loadWeight=0)
    ])
    calculator = VehicleEmissionCalculator(request)
    assert calculator.calculate_emissions() > 0