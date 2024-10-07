import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from fastapi.responses import HTMLResponse


app = FastAPI()

# Load your pre-trained model
model = load_model('model.keras')

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image file
    image = Image.open(file.file)
    # Preprocess the image to fit the model input requirements (28x28)
    image = image.resize((28, 28)).convert("L") # Example resize, adjust as needed
    # Convert the image to grayscale
    
    image = np.array(image).reshape(1,-1) / 255.0  # Normalize the image    
    # Make prediction   
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction, axis=1)

    return {"predicted_class": int(predicted_class[0])}


@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <title>Image Classification</title>
            <script>
                async function uploadImage(event) {
                    const formData = new FormData();
                    formData.append("file", event.target.files[0]);

                    const response = await fetch("/predict/", {
                        method: "POST",
                        body: formData
                    });

                    const result = await response.json();
                    document.getElementById("result").innerText = "Predicted Class: " + result.predicted_class;
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        document.getElementById("uploadedImage").src = e.target.result;
                    }
                    reader.readAsDataURL(event.target.files[0]);
                }
            </script>
        </head>
        <body>
            <h1>Upload an image to classify</h1>
            <input id="file" name="file" type="file" onchange="uploadImage(event)">
            <img id="uploadedImage" src="" alt="Uploaded Image" style="display: block; margin-top: 20px; max-width: 100%; width: 100px; height: 100px;">
            <p id="result"></p>
        </body>
    </html>
    """
    return content
