import mysql.connector
import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from decimal import Decimal

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Gemini API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Custom JSON encoder to handle Decimal objects
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

app.json_encoder = CustomJsonEncoder

@app.route('/')
def index():
    return "Backend server is running!"

@app.route('/api/query', methods=['POST'])
def process_query():
    # 1. Ensure API key is set
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY environment variable not set."}), 500

    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    # 2. Get database schema dynamically
    schema_info = get_database_schema()

    # 3. Generate SQL using the LLM
    generated_sql = generate_sql_with_gemini(user_query, schema_info)
    
    if not generated_sql:
        return jsonify({"error": "Failed to generate SQL query from LLM"}), 500

    # 4. Execute the generated SQL
    try:
        data = execute_sql(generated_sql)
        
        # 5. Summarize the results for human readability
        human_readable_summary = summarize_results_with_gemini(user_query, data)
        
        return jsonify({
            "sql_query": generated_sql,
            "data": data,
            "summary": human_readable_summary
        })
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def get_database_schema():
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        schema = {}
        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in cursor.fetchall()]
            schema[table] = columns
        
        return schema
    except mysql.connector.Error as err:
        print(f"Error getting schema: {err}")
        return {}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def generate_sql_with_gemini(query, schema_info):
    prompt_text = f"""
        You are a SQL expert. Your task is to write a MySQL query based on a user's natural language question.
        
        Database Schema:
        {schema_info}
        
        Analyze the user's question and determine the relevant tables and columns.
        
        User's question: {query}
        
        Provide only the SQL query as your response. Do not include any other text, explanations, or backticks.
        """
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [
            {
                'parts': [{'text': prompt_text}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_json = response.json()
        
        generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
        cleaned_sql = generated_text.replace('```sql', '').replace('```', '').strip()
        
        return cleaned_sql
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Failed to parse API response: {e}")
        print(f"API response: {response.text}")
        return None

def summarize_results_with_gemini(query, data):
    data_json_str = json.dumps(data, cls=CustomJsonEncoder)
    
    prompt_text = f"""
        You are a financial analyst. Your task is to provide a concise, single-paragraph summary of the key findings from a data query.
        
        Original User Question: "{query}"
        
        Query Results:
        {data_json_str}
        
        Analyze the data provided and write a short, professional summary.
        Do not include the raw data or column names in your final response.
        Focus on interpreting the numbers and providing actionable insights.
        """
        
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'contents': [
            {
                'parts': [{'text': prompt_text}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Failed to generate a human-readable summary."
    except (KeyError, IndexError) as e:
        print(f"Failed to parse API response: {e}")
        print(f"API response: {response.text}")
        return "Failed to generate a human-readable summary."
        
def execute_sql(sql_query):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print(f"Error executing SQL: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
