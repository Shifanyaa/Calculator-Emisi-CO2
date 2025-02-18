# Calculation-Service
## Installation and Setup
Follow these steps to install and run the project:

### 1. Clone the Repository
```
git clone https://github.com/alamsyah10/carbon-measurement.git
cd .\carbon-measurement\calculation_service\
```
### 2. Create a Virtual Environment
#### On Windows
```
python -m venv venv
venv\Scripts\activate
```
#### On macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Run the FastAPI Server
```
uvicorn main:app --reload
```
### 5. Access the API
Once the server is running, you can access the API at:
```
- Docs UI: http://127.0.0.1:8000/docs
- Redoc UI: http://127.0.0.1:8000/redoc
```