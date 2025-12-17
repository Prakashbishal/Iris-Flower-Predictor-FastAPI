from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):
    sepal_length: float = Field(..., ge=4.3, le=7.9, description="Sepal length in cm (4.3–7.9)")
    sepal_width:  float = Field(..., ge=2.0, le=4.4, description="Sepal width in cm (2.0–4.4)")
    petal_length: float = Field(..., ge=1.0, le=6.9, description="Petal length in cm (1.0–6.9)")
    petal_width:  float = Field(..., ge=0.1, le=2.5, description="Petal width in cm (0.1–2.5)")

class PredictResponse(BaseModel):
    predicted_category_id: int
    predicted_category_name: str
    image_url: Optional[str] = None
    probabilities: Optional[dict[str, float]] = None
