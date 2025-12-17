from pathlib import Path
import pickle

def load_model(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at: {model_path.resolve()}")
    with open(model_path, "rb") as f:
        return pickle.load(f)
