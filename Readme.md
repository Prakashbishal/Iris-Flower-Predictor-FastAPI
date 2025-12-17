
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

| ID | Class |
|----|------|
| 0  | setosa |
| 1  | versicolor |
| 2  | virginica |

The model is trained on raw centimeter values and saved as a **single pipeline**, ensuring consistent preprocessing during inference.

---

## 📁 Project Structure
```

Iris_Flower_Prediction/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── model_loader.py
│   │
│   ├── routers/
│   │   ├── predict.py
│   │   └── health.py
│   │
│   ├── services/
│   │   ├── predict.py
│   │   └── wiki.py
│   │
│   └── **init**.py
│
├── model/
│   └── saved_model_iris.pkl
│
├── requirements.txt
└── README.md

````

---

## 🔗 API Endpoints

### 🔮 `POST /predict`

#### Request Body
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
````

#### Input Validation (cm)

| Feature      | Min | Max |
| ------------ | --- | --- |
| Sepal length | 4.3 | 7.9 |
| Sepal width  | 2.0 | 4.4 |
| Petal length | 1.0 | 6.9 |
| Petal width  | 0.1 | 2.5 |

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

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

## 🧾 Response Validation

The API uses **Pydantic response models** to validate output structure.

```python
@router.post("/predict", response_model=PredictResponse)
```

---

## ⚙️ Configuration (Environment Variables)

| Variable         | Description                     | Default                        |
| ---------------- | ------------------------------- | ------------------------------ |
| MODEL_PATH       | Path to ML model                | `./model/saved_model_iris.pkl` |
| ENABLE_WIKI      | Enable Wikipedia image fetching | `true`                         |
| WIKI_TIMEOUT_SEC | Wikipedia API timeout           | `6`                            |
| WIKI_USER_AGENT  | HTTP user agent                 | `iris-fastapi/1.0`             |
| LOG_LEVEL        | Logging level                   | `INFO`                         |

---

## ▶️ Running Locally

```bash
uvicorn app.main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker

```bash
docker build -t iris-api .
docker run -p 8000:8000 iris-api
```

---

## ☁️ AWS EC2 Deployment (Docker)

After deploying the container on an EC2 instance, the API is accessible via the **EC2 Public IPv4 address**:

```
http://<EC2_PUBLIC_IP>:8000/docs
```

> The public IP can be found in:
> AWS Console → EC2 → Instances → Public IPv4 address

⚠️ Do **not** hard-code the public IP in source code or configuration files.

---

## 🎨 Streamlit Frontend (Local / Network Access)

During local development, the Streamlit frontend exposes:

```
Local URL:    http://localhost:8501
Network URL:  http://10.130.49.2:8501
```

### Notes

* `localhost` → accessible only on the same machine
* `Network URL` → accessible **within the same local network**
* These URLs are **not public** and **should not be used for cloud deployment**
* For production, the frontend should call the **EC2 public API URL**

---

## 🛡️ Production Considerations

* Model loaded once at startup
* Stateless API
* Input & output validation enforced
* External API calls fail gracefully
* Docker & cloud ready

---

## 👤 Author

**Bishal Pandey**
<br>
MSc Artificial Intelligence @
University of Southampton

