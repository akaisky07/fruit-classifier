import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/hgarg/fruits"
API_KEY = "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"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            # Save the uploaded image temporarily
            img_path = "temp_image.png"
            uploaded_file.save(img_path)

            # Send the image to the Hugging Face model for prediction
            with open(img_path, "rb") as f:
                data = f.read()
            headers = {"Authorization": f"Bearer {API_KEY}"}
            response = requests.post(API_URL, headers=headers, data=data)
            predictions = response.json()

            # Get the label from the predictions
            if predictions:
                label = predictions[0]["label"]
            else:
                label = "No prediction available"

            # Remove the temporary image file
            os.remove(img_path)

            return render_template("index.html", label=label)

    return render_template("index.html", label=None)

if __name__ == "__main__":
    app.run(debug=True)

