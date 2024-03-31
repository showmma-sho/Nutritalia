from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyDjTqzuNHvlXAjnhLfXc69QM4f0qkefRKQ")

def get_gemini_response(input_prompt, image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify(error='No file part in the request'), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join('/tmp', filename)
    file.save(filepath)

    image_data = input_image_setup(file)
    input_prompt="""
    You are an expert in nutritionist where you need to see the food items from the image
                   and calculate the total calories, also provide the details of every food items with calories intake
                   is below format

                   1. Item 1 - no of calories
                   2. Item 2 - no of calories
                   ----
                   ----
    Finally you can also mention whether the food is healthy, balanced or not healthy and what all additional food items can be added in the diet which are healthy.
    """
    response = get_gemini_response(input_prompt, image_data)

    return jsonify(response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
