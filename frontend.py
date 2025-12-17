import streamlit as st
import requests

API_URL="http://localhost:8000/predict"

st.title("Iris Flower Predictor")
st.markdown("Enter the flower measurements (in cm) and click **Predict**.")

#Input Fields
sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, value=5.1, step=0.1, format="%.1f")
sepal_width  = st.number_input("Sepal Width (cm)",  min_value=0.0, value=3.5, step=0.1, format="%.1f")
petal_length = st.number_input("Petal Length (cm)", min_value=0.0, value=1.4, step=0.1, format="%.1f")
petal_width  = st.number_input("Petal Width (cm)",  min_value=0.0, value=0.2, step=0.1, format="%.1f")


if st.button("Predict"):
    input_data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }

    try:
        response = requests.post(API_URL, json=input_data, timeout=10)

        # If FastAPI returns non-JSON error (500 text), this prevents crash
        try:
            result = response.json()
        except Exception:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
            st.stop()
        if response.status_code == 422:
            error = response.json()
            st.error("Invalid input value")

            for e in error["detail"]:
                field = e["loc"][-1]
                message = e["msg"]
                st.warning(f"❌ {field}: {message}")
            st.stop()

        if response.status_code == 200:
            st.success(f"Predicted Flower: **{result['predicted_category_name']}**")
            st.write("Class ID:", result["predicted_category_id"])
            img = result.get("image_url")
            if img:
                st.image(img, caption=f"Iris {result['predicted_category_name']}")
            else:
                st.info("No image found from Wikipedia for this class.")

            # If you later add probabilities in FastAPI, this will display them
            if "probabilities" in result and result["probabilities"] is not None:
                st.subheader("Probabilities")
                st.json(result["probabilities"])
        else:
            st.error(f"API Error: {response.status_code}")
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI. Make sure Uvicorn is running on port 8000.")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Try again.")
