import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import timm
import numpy as np
import os

X = np.random.rand(100, 3, 224, 224).astype(np.float32)  # Dummy RGB images
y = np.random.randint(0, 3, (100, 224, 224)).astype(np.int64)  # Dummy masks

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
        x = x.transpose(1, 2).reshape(B, C, 14, 14)
        x = nn.functional.interpolate(x, size=(224, 224), mode='bilinear', align_corners=False)
        x = self.decoder(x)
        return x

model = SimpleViTSeg(num_classes=3)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

dataset = TensorDataset(torch.tensor(X), torch.tensor(y))
loader = DataLoader(dataset, batch_size=8, shuffle=True)

for epoch in range(2):  # Demo: 2 epochs
    for xb, yb in loader:
        optimizer.zero_grad()
        out = model(xb)
        loss = criterion(out, yb)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), "models/zoning_vit.pt")
print("ViT model saved as models/zoning_vit.pt")