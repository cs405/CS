import onnx
import torch
from onnx2pytorch import ConvertModel

# Load the ONNX model
onnx_model = onnx.load(r'E:\CF\model\CFHD.onnx')

# Convert the ONNX model to PyTorch model
pytorch_model = ConvertModel(onnx_model)

# Save the PyTorch model
torch.save(pytorch_model.state_dict(), 'model.pt')
