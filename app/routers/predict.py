from fastapi import APIRouter, Request
from app.schemas import UserInput, PredictResponse
from app.services.predict import make_input_df, predict, predict_proba

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictResponse)
def predict_route(payload: UserInput, request: Request) -> PredictResponse:
    model = request.app.state.model
    wiki = request.app.state.wiki

    df = make_input_df(
        sepal_length=payload.sepal_length,
        sepal_width=payload.sepal_width,
        petal_length=payload.petal_length,
        petal_width=payload.petal_width,
    )

    pred_id, pred_name = predict(model, df)
    probs = predict_proba(model, df)
    image_url = wiki.get_thumbnail(pred_name) if wiki else None

    return PredictResponse(
        predicted_category_id=pred_id,
        predicted_category_name=pred_name,
        image_url=image_url,
        probabilities=probs,
    )
