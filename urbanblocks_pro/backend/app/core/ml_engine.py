import numpy as np
import joblib
import shap
import os

class LayoutScorer:
    def __init__(self, model_path="models/layout_scorer.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ML model not found at {model_path}")
        self.model = joblib.load(model_path)
        self.explainer = shap.Explainer(self.model)

    def predict(self, features: np.ndarray):
        score = self.model.predict([features])[0]
        shap_values = self.explainer(features.reshape(1, -1))
        return score, shap_values.values[0].tolist()