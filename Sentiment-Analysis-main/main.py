import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set the prediction endpoint
prediction_endpoint = "http://127.0.0.1:5000/predict"

st.title("Text Sentiment Predictor")

# File uploader for bulk prediction
uploaded_file = st.file_uploader(
    "Choose a CSV file for bulk prediction - Upload the file and click on Predict",
    type="csv",
)

# Text input for single sentiment prediction
user_input = st.text_input("Enter text and click on Predict", "")

# Prediction button for single sentence
if st.button("Predict"):
    if uploaded_file is not None:
        # Handle bulk prediction
        response = requests.post(prediction_endpoint, files={"file": uploaded_file})
        if response.status_code == 200:
            response_bytes = BytesIO(response.content)
            response_df = pd.read_csv(response_bytes)

            st.download_button(
                label="Download Predictions",
                data=response_bytes,
                file_name="Predictions.csv",
                key="result_download_button",
            )

            # Check for graph data in headers
            if response.headers.get("X-Graph-Exists") == "true":
                graph_data = base64.b64decode(response.headers["X-Graph-Data"])
                st.image(graph_data, caption="Sentiment Distribution")

        else:
            st.error("Failed to get response from API for file upload.")
    else:
        # Handle single text prediction
        response = requests.post(prediction_endpoint, json={"text": user_input})
        if response.status_code == 200:
            result = response.json()
            if 'prediction' in result:
                st.write(f"Predicted sentiment: {result['prediction']}")
            else:
                st.error("Prediction key not found in response.")
        else:
            st.error("Failed to get response from API for text input.")
