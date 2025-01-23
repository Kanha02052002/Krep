# Krep
## Overview
This project is designed to transform a PDF syllabus into an interactive and visually engaging flow network graph. The tool provides an efficient way for students and educators to explore and track their syllabus. Additionally, it links topics to curated resources like YouTube videos, books, and summaries, enabling a centralized learning experience.

---

## Features
### Current Features:
- **PDF Upload:** Upload course syllabi in PDF format for processing.
- **Text Extraction:** Extracts syllabus content using `PyMuPDF`.
- **JSON Conversion:** Converts the extracted text into a structured JSON format.
- **Interactive Graph:** Visualizes the syllabus using flow network graphs, showing:
  - Course name at the center.
  - Modules branching out from the course name.
  - Topics connected under each module.
- **Checklist Integration:** Track topic completion status interactively.
- **Resource Linking:** Add hyperlinks to:
  - YouTube videos
  - Recommended books
  - Summaries of each topic
- **File Management:** Organizes uploaded PDFs, generated JSON files, and graphs in designated folders.

---

## Tech Stack
- **Framework:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Backend Libraries:**
  - `PyMuPDF` (fitz) for PDF text extraction
  - `Matplotlib` or `NetworkX` for generating flow network graphs
  - `Faker` for generating mock data
- **File Handling:** Securely handles file uploads and storage with organized directories

---

## How It Works
1. **Upload a Syllabus:** Upload a course syllabus in PDF format via the web interface.
2. **Text Extraction:** The system extracts text from the PDF and processes it into a JSON format.
3. **JSON Processing:** Converts the syllabus into modules and topics with a "completed" status for tracking.
4. **Graph Visualization:** Generates a flow network graph and saves it.
5. **Interactive Checklist:** Users can mark topics as completed, and the status is dynamically updated in the JSON file.
6. **Resource Links:** Adds hyperlinks to external learning resources for each topic.

---

## Upcoming Features
### Planned Enhancements:
1. **Downloadable Summaries:** Provide downloadable PDF guides for each topic.
2. **Dynamic Graph Updates:** Allow users to modify or update the graph nodes directly from the interface.
3. **Custom Visual Themes:** Add options for customizable graph styles and themes.
4. **Database Integration:** Store and retrieve syllabus data and resources from a database.
5. **Enhanced Resource Suggestions:** Automatically recommend resources for each topic using machine learning.
6. **Search Functionality:** Add a search bar to quickly locate specific modules or topics.
7. **User Authentication:** Introduce login functionality for personalized dashboards and progress tracking.
8. **Collaboration:** Enable shared access for teams to track and update syllabus progress collaboratively.

---

## Installation and Setup
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd <project-directory>
   ```
3. **Install Dependencies:**
   Ensure Python and pip are installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   Start the Flask development server:
   ```bash
   python app.py
   ```
5. **Access the Application:**
   Open your browser and go to `http://127.0.0.1:5000`.

---

## Folder Structure
```
project-directory/
|-- app.py                 # Flask application
|-- data_preprocess.py     # Text-to-JSON conversion logic
|-- graph_gen_test.py      # Graph generation logic
|-- templates/             # HTML templates
|   |-- index.html
|   |-- course_structure.html
|-- static/                # CSS, JS, and image files
|-- uploads/               # Directory for uploaded PDFs
|-- json_format/           # Directory for JSON files
|-- graph_format/          # Directory for generated graphs
|-- requirements.txt       # List of dependencies
```

---

## Contributing
Feel free to fork the repository, create a new branch, and submit a pull request for any improvements or feature suggestions. Contributions are welcome!

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact
For questions, suggestions, or collaborations, feel free to reach out! 😊
