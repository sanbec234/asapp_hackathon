# PDFQuery

**PDFQuery** is a web-based application designed to answer questions from uploaded PDF files. It enables users to ask specific questions from PDF documents and to retrieve relevant information. The project is built with a Flask backend for handling PDF processing and a React frontend for user interaction, ensuring an intuitive user experience.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Project Structure](#project-structure)
8. [Future Improvements](#future-improvements)
9. [Contributors](#contributors)
10. [License](#license)

---

## Overview

**PDFQuery** provides users with the ability to interact with documents in a more dynamic way. Instead of reading through entire PDF files, users can upload their files and simply ask questions. The system will return relevant answers extracted from the content of the PDF.

---

## Features

- **Question & Answering**: Ask questions related to the content of the uploaded PDF, and receive relevant answers.
- **User-Friendly Interface**: A clean, modern UI with chat-like interactions between users and the system.
- **Fast Response**: Quick and efficient retrieval of answers from PDFs.
- **Multiple Document Support**: Handle multiple PDF documents with ease.

---

## Tech Stack

### Frontend:
- **React**: For building the user interface.
  
### Backend:
- **Flask**: Backend framework for processing the PDF and handling requests.
- **Python**: Core language for backend development.


### Other Tools:
- **Axios**: For handling API requests between the React frontend and Flask backend.
- **Git**: Version control for the project.

---

## Installation

### Prerequisites

Before you start, ensure you have the following tools installed on your machine:

- **Node.js** (v14 or later)
- **Python 3.11+**
- **Git**
- **Virtualenv** (optional, but recommended)

### Step 1: Clone the Repository
bash
git clone https://github.com/your-username/pdfquery.git
cd pdfquery


### Step 2: Backend Setup (Flask)
1. Navigate to the backend directory:
   bash
   cd backend
   

2. Create a virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   

3. Install backend dependencies:
   bash
   pip install -r requirements.txt
   

4. Start the Flask server:
   bash
   flask run
   

### Step 3: Frontend Setup (React)
1. Navigate to the frontend directory:
   bash
   cd frontend
   

2. Install frontend dependencies:
   bash
   npm install
   npm i
   

3. Start the React-Vite development server:
   bash
   npm run dev
   

4. Open the app at:
   
   http://localhost:5173
   

---

## Usage


1. **Ask Questions**: Type your questions related to the document in the provided input field.
2. **Get Answers**: The system will process the document and return the most relevant answer.

### Example Workflow:

1. **Upload a PDF**: Click on the "Upload PDF" button and select your document.
2. **Ask a Question**: Type a question such as "What is the conclusion of the paper?" in the input field.
3. **Receive Answer**: The system will display the answer in the chat window.

---

## API Endpoints

### 1. **POST /api/question**
- **Description**: Ask a question related to the uploaded PDF.
- **Request**: 
  json
  {
    "file_id": "unique_file_id",
    "question": "What is the summary of the document?"
  }
  
- **Response**:
  json
  {
    "answer": "This document provides an overview of..."
  }
  

---

## Project Structure


pdfquery/
│
├── backend/                  # Flask backend
│   ├── app.py                # Main application file
│   ├── requirements.txt      # Python dependencies
│   └── static/               # Static files (if needed)
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.jsx           # Main component
│   │   ├── index.js          # Entry point
│   │   └── App.css           # Global styles
│   ├── public/               # Public static files
│   └── package.json          # Frontend dependencies
│
├── README.md                 # Project documentation
└── .gitignore                # Ignored files



---

## Future Improvements

- **Advanced NLP Features**: Adding more sophisticated natural language processing to improve answer accuracy.
- **User Authentication**: Adding login and user sessions to allow users to save their uploaded files and query history.
- **Export Feature**: Enable users to download their questions and answers in a report format.

---

## Contributors

- **Navaneetha Krishnan K S, Snehan, Soorya, Sushant, VishnuDharshan** – Developer, Backend & Frontend
---
