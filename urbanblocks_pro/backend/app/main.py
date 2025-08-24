from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from urbanblocks_pro.backend.app.api.routes import router as api_router
from urbanblocks_pro.backend.app.core.vit_engine import ZoningViT

app = FastAPI(title="UrbanBlocks Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.get("/")
def root():
    return {"message": "🚀 UrbanBlocks Backend Running!"}

@app.post("/api/predict-zoning-vit/")
def predict_zoning_vit(input_data: dict):
    model = ZoningViT()
    zoning_map = model.predict(input_data["grid"], input_data.get("constraints", {}))
    return {"zoning_map": zoning_map}
