import numpy as np
import tensorflow as tf
import os

class ZoningUNet:
    def __init__(self, model_path="models/zoning_unet.h5"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"DL model not found at {model_path}")
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, grid, constraints=None):
        grid_arr = np.array(grid)
        # Resize to (32, 32) if needed
        if grid_arr.shape != (32, 32):
            from skimage.transform import resize
            grid_arr = resize(grid_arr, (32, 32), order=0, preserve_range=True, anti_aliasing=False).astype(int)
        grid_arr = grid_arr.reshape(1, 32, 32, 1)
        pred = self.model.predict(grid_arr)
        zoning_map = np.argmax(pred, axis=-1)[0].tolist()
        return zoning_map