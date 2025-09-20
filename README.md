## Data Sphere: An LLM-Powered Data Assistant

## Project Overview
Data Sphere is a full-stack application that demonstrates how to use a Large Language Model (LLM) to make data accessible to non-technical users, like business leaders. It allows a user to ask a question in natural language, which is then translated into an executable SQL query. The system runs the query on a real database and provides a concise, human-readable summary of the results.

This project showcases skills in building an end-to-end GenAI application, from front-end design to secure backend development and database interaction.

## Features
Natural Language to SQL: Uses the Gemini API to translate plain English queries into executable SQL, abstracting the need for technical knowledge.

Dynamic Schema Introspection: The backend automatically explores the database to identify tables and columns, making the application adaptable to changes in the database without manual code updates.

Human-Readable Summaries: The LLM is used to generate a concise, professional summary of the query results, providing immediate insights.

Validation Fallback: A "Send for Validation" button pre-populates an email with the query and generated SQL, providing a clear path for human review.

## Technical Stack
Frontend: HTML, CSS (Tailwind CSS), and JavaScript

Backend: Python with the Flask framework

LLM: Google Gemini API

Database: MySQL

## Getting Started
Follow these steps to set up and run the project locally.

1. Database Setup
Open MySQL Workbench and create a new schema (database) named leadership_app.

Run the database/database_setup.sql script inside your new schema to create the necessary tables and populate them with sample data.

2. Backend Setup
Navigate to the backend folder in your terminal.

Create a Python virtual environment and activate it.

python -m venv venv

source venv/bin/activate (macOS/Linux) or venv\Scripts\activate (Windows)

Install the required libraries using the requirements.txt file:

pip install -r requirements.txt

Configure Environment Variables:

Create a file named .env in the backend folder. Do not add this file to Git.

Add your credentials, replacing the placeholders below:

DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=leadership_app
GEMINI_API_KEY=your_gemini_api_key


Run the Flask server:

python app.py

3. Running the Application
Open the frontend/index.html file in your web browser.

The application will automatically connect to your running backend server.

Enter a natural language query in the text box (e.g., "What is the total revenue from all orders?") and click "Get Data".
