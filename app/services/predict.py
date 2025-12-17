from __future__ import annotations

import pandas as pd
from fastapi import HTTPException

CLASS_NAMES = ["setosa", "versicolor", "virginica"]

FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]

def make_input_df(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> pd.DataFrame:
    return pd.DataFrame([{
        "sepal length (cm)": sepal_length,
        "sepal width (cm)": sepal_width,
        "petal length (cm)": petal_length,
        "petal width (cm)": petal_width,
    }], columns=FEATURE_COLUMNS)

def predict(model, input_df: pd.DataFrame) -> tuple[int, str]:
    try:
        pred_id = int(model.predict(input_df)[0])
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")

    if pred_id < 0 or pred_id >= len(CLASS_NAMES):
        raise HTTPException(status_code=500, detail="Invalid model output")

    return pred_id, CLASS_NAMES[pred_id]

def predict_proba(model, input_df: pd.DataFrame) -> dict[str, float] | None:
    if not hasattr(model, "predict_proba"):
        return None
    try:
        probs = model.predict_proba(input_df)[0]
        return {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))}
    except Exception:
        return None
