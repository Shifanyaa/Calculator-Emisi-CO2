from fastapi import FastAPI
from routers.emissions import router 

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Carbon Measurement Service is running!"}



