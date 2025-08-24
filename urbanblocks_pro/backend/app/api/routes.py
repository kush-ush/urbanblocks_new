from fastapi import APIRouter, Body
from urbanblocks_pro.backend.app.api import upload
from urbanblocks_pro.backend.app.core.ml_engine import LayoutScorer
from urbanblocks_pro.backend.app.core.dl_engine import ZoningUNet
from urbanblocks_pro.backend.app.core.vit_engine import ZoningViT
from urbanblocks_pro.backend.app.core.optimization import genetic_algorithm, simulated_annealing, reinforcement_learning
from urbanblocks_pro.backend.app.crud.zone import create_zone, get_zones
import numpy as np

router = APIRouter()
router.include_router(upload.router, prefix="/api")

@router.post("/api/score-layout/")
def score_layout(features: list = Body(...)):
    scorer = LayoutScorer()
    score, shap_values = scorer.predict(np.array(features))
    return {"score": score, "shap": shap_values}

@router.post("/api/predict-zoning/")
def predict_zoning(input_data: dict = Body(...)):
    # input_data: { "grid": ..., "constraints": ... }
    model = ZoningUNet()
    zoning_map = model.predict(input_data["grid"], input_data.get("constraints", {}))
    return {"zoning_map": zoning_map}

@router.post("/predict-zoning-vit/")
def predict_zoning_vit(input_data: dict):
    model = ZoningViT()
    zoning_map = model.predict(input_data["grid"], input_data.get("constraints", {}))
    return {"zoning_map": zoning_map}

@router.post("/api/optimize-layout/")
def optimize_layout(data: dict = Body(...)):
    layout = data.get("layout")
    constraints = data.get("constraints", {})
    method = data.get("method", "ga")
    if method == "ga":
        optimized = genetic_algorithm(layout, constraints)
    elif method == "sa":
        optimized = simulated_annealing(layout, constraints)
    elif method == "rl":
        optimized = reinforcement_learning(layout, constraints)
    else:
        return {"error": "Unknown optimization method"}
    return {"optimized_layout": optimized}

@router.post("/zones/")
def add_zone(name: str, geom_wkt: str):
    return create_zone(name, geom_wkt)

@router.get("/zones/")
def list_zones():
    return get_zones()
