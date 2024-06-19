# File Upload and Text Extraction App

This project is a web application that allows users to upload images and extract text from them using OCR. The application supports both drag-and-drop and manual file selection for uploading images.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Acknowledgements](#acknowledgements)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+
- Node.js 14+
- npm 6+ (comes with Node.js)
- A free OCR API key from [OCR.Space](https://ocr.space/ocrapi)

## Installation

### Backend

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository/backend
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the `backend` directory and add your OCR API key:

    ```env
    OCR_API_KEY=your_ocr_space_api_key
    ```

### Frontend

1. Navigate to the frontend directory:

    ```bash
    cd ../frontend
    ```

2. Install the required npm packages:

    ```bash
    npm install
    ```

## Running the Application

### Backend

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2. Start the Flask development server:

    ```bash
    flask run
    ```

   The backend server will start on `http://localhost:5000`.

### Frontend

1. Navigate to the `frontend` directory:

    ```bash
    cd ../frontend
    ```

2. Start the React development server:

    ```bash
    npm start
    ```

   The frontend server will start on `http://localhost:3000`.

## Usage

1. Open your web browser and navigate to `http://localhost:3000`.
2. Drag and drop an image file into the drop area or click to upload manually.
3. Click the "Upload" button to process the image.
4. The extracted text and bold words will be displayed on the page.

## API Endpoints

### Upload Image

- **URL**: `/upload`
- **Method**: `POST`
- **Form Data**:
  - `file`: The image file to be processed.
- **Response**: JSON object containing the extracted text and bold words.

Example:

```json
{
  "text": "Extracted text from image.",
  "bold_words": "Bold words from text.",
  "image": "base64_encoded_image"
}
