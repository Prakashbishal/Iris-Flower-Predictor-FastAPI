
# 🌸 Iris Flower Prediction API (FastAPI)

A **production-ready, modular FastAPI application** that predicts the species of an Iris flower based on physical measurements and enriches the response with a representative flower image fetched from Wikipedia.

This project demonstrates **clean backend architecture for ML inference**, following industry-standard separation of concerns and validation practices.

---

## ✨ Key Features

* 🧠 Machine Learning inference using a **scikit-learn pipeline**
* 📏 Accepts **real-world measurements (cm)** with strict validation
* 🖼️ Automatically fetches a representative flower image from **Wikipedia**
* 📊 Optional class probabilities
* 🧱 Clean modular architecture (routes, schemas, services, config)
* 🧪 Response validation using **Pydantic response models**
* 🐳 Designed for Docker & cloud deployment
* ❤️ Health check endpoint for monitoring

---

## 🧠 Machine Learning Model

* **Dataset**: Iris dataset (scikit-learn)
* **Features**:

  * Sepal length (cm)
  * Sepal width (cm)
  * Petal length (cm)
  * Petal width (cm)
* **Pipeline**:

  * `StandardScaler`
  * `LogisticRegression`
* **Classes**:

  | ID | Class      |
  | -- | ---------- |
  | 0  | setosa     |
  | 1  | versicolor |
  | 2  | virginica  |

The model is trained on raw centimeter values and saved as a **single pipeline**, ensuring consistent preprocessing during inference.

---

## 📁 Project Structure

```
Iris_Flower_Prediction/
│
├── app/
│   ├── main.py              # App factory & router wiring
│   ├── config.py            # Environment-based configuration
│   ├── schemas.py           # Pydantic request & response models
│   ├── model_loader.py      # ML model loading logic
│   │
│   ├── routers/
│   │   ├── predict.py       # /predict endpoint
│   │   └── health.py        # /health endpoint
│   │
│   ├── services/
│   │   ├── predict.py       # ML prediction logic
│   │   └── wiki.py          # Wikipedia image fetching
│   │
│   └── __init__.py
│
├── model/
│   └── saved_model_iris.pkl # Trained ML pipeline
│
├── requirements.txt
└── README.md
```

---

## 🔗 API Endpoints

### 🔮 `POST /predict`

Predict the Iris flower species.

#### Request Body

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

#### Input Validation (cm)

| Feature      | Min | Max |
| ------------ | --- | --- |
| Sepal length | 4.3 | 7.9 |
| Sepal width  | 2.0 | 4.4 |
| Petal length | 1.0 | 6.9 |
| Petal width  | 0.1 | 2.5 |

Invalid inputs automatically return **422 Unprocessable Entity** with detailed error messages.

---

#### Response

```json
{
  "predicted_category_id": 0,
  "predicted_category_name": "setosa",
  "image_url": "https://upload.wikimedia.org/...",
  "probabilities": {
    "setosa": 0.98,
    "versicolor": 0.01,
    "virginica": 0.01
  }
}
```

---

### ❤️ `GET /health`

Health check endpoint for Docker/Kubernetes.

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## 🧾 Response Validation

The API uses **Pydantic response models** to validate output structure.

* Ensures correct types & keys
* Automatically documented in `/docs`
* Prevents accidental malformed responses

Validation is applied via:

```python
@router.post("/predict", response_model=PredictResponse)
```

---

## ⚙️ Configuration (Environment Variables)

| Variable           | Description                     | Default                        |
| ------------------ | ------------------------------- | ------------------------------ |
| `MODEL_PATH`       | Path to ML model                | `./model/saved_model_iris.pkl` |
| `ENABLE_WIKI`      | Enable Wikipedia image fetching | `true`                         |
| `WIKI_TIMEOUT_SEC` | Wikipedia API timeout (sec)     | `6`                            |
| `WIKI_USER_AGENT`  | HTTP user agent                 | `iris-fastapi/1.0`             |
| `LOG_LEVEL`        | Logging level                   | `INFO`                         |

---

## ▶️ Running Locally

### 1️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API

```bash
uvicorn app.main:app --reload
```

### 4️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker Ready

The app is designed for containerization:

* Model loaded at startup
* Stateless requests
* Configurable via environment variables
* Health endpoint for orchestration

*(Dockerfile can be added later without refactoring code)*

---

## 🛡️ Production Considerations

* Model loaded once at startup (fast inference)
* External API calls use retries & caching
* Input validation at API boundary
* Response validation enforced
* Graceful degradation if Wikipedia fails

---

## 🔮 Possible Enhancements

* Dockerfile & CI pipeline
* Rate limiting & auth
* Structured logging & metrics
* Model versioning
* Multiple ML models
* Image source fallback

---

## 👤 Author

**Bishal Pandey**
<br>
MSc Artificial Intelligence
University of Southampton

---
