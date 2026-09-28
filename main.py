from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# This allows your DigitalOcean Next.js storefront to talk to this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Nexus Backend Engine Online", "rooms_active": "Dynamic"}

@app.get("/api/matrix")
def get_matrix_catalog():
    # This dynamically reads the JSON file, whether it has 22 or 25 rooms
    try:
        if os.path.exists("matrix_catalog.json"):
            with open("matrix_catalog.json", "r") as file:
                catalog = json.load(file)
            return catalog
        else:
            return {"error": "Matrix catalog not found. Awaiting JSON deployment."}
    except Exception as e:
        return {"error": f"Engine fault: {str(e)}"}
