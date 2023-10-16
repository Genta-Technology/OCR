"""
Download the model from the hub, only run once
"""

from huggingface_hub import snapshot_download

snapshot_download(repo_id="genta-tech/nougat-small-onnx-quantized", local_dir="./model")