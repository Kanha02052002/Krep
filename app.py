import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import fitz
from data_preprocess import process_syllabus_to_json  # Import the function from data_process.py
from graph_gen_test import save_visualization  # Import the save_visualization function from graph_gen_test.py

# Initialize Flask app
app = Flask(__name__)

UPLOAD_DIR = "uploads"
JSON_DIR = 'json_format'
GRAPH_DIR = 'graph_format'  # This should match the GRAPH_DIR in graph_gen_test.py

# Directory for storing uploaded files
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(JSON_DIR):
    os.makedirs(JSON_DIR)

if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'pdf'}

# Clear all folders on reset
def reset_func(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print('Folder reset')

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_pdf_content(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error while processing PDF: {e}")
    return text

# Route for file upload page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            file.save(file_path)

            # Extract PDF content and process the text to convert it into JSON
            extracted_text = extract_pdf_content(file_path)
            # Process the extracted text and convert it to JSON format
            syllabus_json = process_syllabus_to_json(extracted_text)

            # Save JSON to a file in the JSON_DIR
            json_file_path = os.path.join(JSON_DIR, 'syllabus.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(syllabus_json, json_file, indent=4)

            # After processing JSON, generate the graph visualization and save it
            save_visualization(json_file_path)  # This will save the visualization in the GRAPH_DIR

            # Redirect to the page displaying the extracted JSON content
            return redirect(url_for('extract_text', filename='syllabus.json'))

    return render_template('index.html')

# Route for displaying extracted text (JSON content)
@app.route('/extract_text/<filename>')
def extract_text(filename):
    json_file_path = os.path.join(JSON_DIR, 'syllabus.json')

    try:
        with open(json_file_path, 'r') as json_file:
            extracted_json = json.load(json_file)
    except Exception as e:
        return f"Error loading JSON file: {e}"

    # Render the extracted JSON as text on the page
    return render_template('extract_text.html', extracted_json=extracted_json)

if __name__ == "__main__":
    app.run(debug=True)
