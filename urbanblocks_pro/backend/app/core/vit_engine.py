import torch
import torch.nn as nn
import timm
import numpy as np
import os

class SimpleViTSeg(nn.Module):
    def __init__(self, num_classes=3):
        super().__init__()
        self.encoder = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=0)
        self.decoder = nn.Conv2d(768, num_classes, kernel_size=1)

    def forward(self, x):
        x = self.encoder.patch_embed(x)
        x = self.encoder.pos_drop(x)
        x = self.encoder.blocks(x)
        x = self.encoder.norm(x)
        B, N, C = x.shape
        x = x.transpose(1, 2).reshape(B, C, 14, 14)  # 224/16 = 14
        x = nn.functional.interpolate(x, size=(224, 224), mode='bilinear', align_corners=False)
        x = self.decoder(x)
        return x

class ZoningViT:
    def __init__(self, model_path="models/zoning_vit.pt"):
        self.model = SimpleViTSeg(num_classes=3)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()

    def predict(self, grid, constraints=None):
        grid_arr = np.array(grid)
        if grid_arr.shape != (224, 224, 3):
            from skimage.transform import resize
            grid_arr = resize(grid_arr, (224, 224, 3), order=1, preserve_range=True, anti_aliasing=True).astype(np.float32)
        grid_arr = np.transpose(grid_arr, (2, 0, 1))  # HWC to CHW
        grid_arr = torch.tensor(grid_arr).unsqueeze(0).float()
        with torch.no_grad():
            out = self.model(grid_arr)
            zoning_map = torch.argmax(out, dim=1)[0].numpy().tolist()
        return zoning_map