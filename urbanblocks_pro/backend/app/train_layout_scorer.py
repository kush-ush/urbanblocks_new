import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
import os

# Dummy data: Replace with your real features and scores if available
X = np.random.rand(100, 10)  # 100 samples, 10 features
y = np.random.rand(100)      # 100 scores

model = RandomForestRegressor()
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/layout_scorer.pkl")
print("ML model saved as models/layout_scorer.pkl")