import os
import json
import asyncio
import subprocess
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import bigquery
from mcp_client import query_pulsa_providers, query_pulsa_products

# Load environment variables
load_dotenv()

# Configure Google AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize BigQuery client
# For now, disable BigQuery and use mock data
bigquery_enabled = False
bq_client = None

# Mock data storage
mock_database = {
    "customers": [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "total_orders": 15},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "total_orders": 23},
        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "total_orders": 8},
        {"id": 4, "name": "Alice Williams", "email": "alice@example.com", "total_orders": 31},
        {"id": 5, "name": "Charlie Brown", "email": "charlie@example.com", "total_orders": 12}
    ],
    "products": [
        {"id": 1, "name": "Laptop", "price": 15000000, "stock": 25},
        {"id": 2, "name": "Mouse", "price": 250000, "stock": 150},
        {"id": 3, "name": "Keyboard", "price": 750000, "stock": 80},
        {"id": 4, "name": "Monitor", "price": 3500000, "stock": 40},
        {"id": 5, "name": "Headset", "price": 850000, "stock": 60}
    ],
    "sales": [
        {"order_id": 1, "customer_id": 1, "product_id": 1, "quantity": 2, "total": 30000000, "date": "2025-11-20"},
        {"order_id": 2, "customer_id": 2, "product_id": 2, "quantity": 5, "total": 1250000, "date": "2025-11-21"},
        {"order_id": 3, "customer_id": 3, "product_id": 3, "quantity": 3, "total": 2250000, "date": "2025-11-21"},
        {"order_id": 4, "customer_id": 4, "product_id": 4, "quantity": 1, "total": 3500000, "date": "2025-11-22"},
        {"order_id": 5, "customer_id": 1, "product_id": 5, "quantity": 2, "total": 1700000, "date": "2025-11-22"}
    ]  
}

# Initialize Flask app
app = Flask(__name__)

# Define function declarations for Gemini
query_database_tool = genai.protos.FunctionDeclaration(
    name="query_database",
    description="Query database tables: 'customers', 'products', 'sales', or 'pulsa'. Use this when user asks about data, statistics, or database queries. For pulsa queries, use 'pulsa' table.",
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            "table_name": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                description="Name of table to query: customers, products, sales, or pulsa",
                enum=["customers", "products", "sales", "pulsa"]
            ),
            "action": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                description="Action to perform: list_all, count, search, or filter_by_provider (for pulsa only)",
                enum=["list_all", "count", "search", "filter_by_provider"]
            ),
            "filter_value": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                description="Filter value for filter_by_provider action (e.g., Telkomsel, Indosat, XL, Axis, Tri)"
            )
        },
        required=["table_name", "action"]
    )
)

# Initialize Gemini model with tools
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    tools=[query_database_tool]
)

chat = model.start_chat(history=[])

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

def query_database(table_name, action, filter_value=None):
    """Query mock database or MCP server"""
    try:
        # If asking for pulsa data, use MCP server
        if table_name == "pulsa":
            if action == "list_all":
                return query_pulsa_products()
            elif action == "filter_by_provider" and filter_value:
                return query_pulsa_products(provider=filter_value)
            elif action == "count":
                products = query_pulsa_products()
                return {
                    "success": True,
                    "table": "pulsa",
                    "count": products.get("total", 0)
                }
            return query_pulsa_products()
        
        # For other tables, use mock database
        if table_name not in mock_database:
            return {"error": f"Table '{table_name}' not found"}
        
        data = mock_database[table_name]
        
        if action == "list_all":
            return {
                "success": True,
                "table": table_name,
                "rows": data,
                "total_rows": len(data)
            }
        elif action == "count":
            return {
                "success": True,
                "table": table_name,
                "count": len(data)
            }
        elif action == "search":
            return {
                "success": True,
                "table": table_name,
                "rows": data[:5],
                "total_rows": len(data)
            }
        else:
            return {"error": "Invalid action"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Send message to Gemini
        response = chat.send_message(user_message)
        
        # Handle function calls if Gemini requests them
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            
            # Execute database query function
            if function_call.name == "query_database":
                table_name = function_call.args["table_name"]
                action = function_call.args.get("action", "list_all")
                filter_value = function_call.args.get("filter_value")
                result = query_database(table_name, action, filter_value)
                
                # Send function response back to Gemini
                function_response = genai.protos.FunctionResponse(
                    name="query_database",
                    response={"result": result}
                )
                
                response = chat.send_message(
                    genai.protos.Part(function_response=function_response)
                )
        
        return jsonify({
            'response': response.text,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Reset the chat history"""
    global chat
    chat = model.start_chat(history=[])
    return jsonify({
        'status': 'success',
        'message': 'Chat history reset'
    })

@app.route('/api/data/<table_name>', methods=['GET', 'POST'])
def manage_data(table_name):
    """Get or add data to tables"""
    if table_name not in mock_database:
        return jsonify({'error': f"Table '{table_name}' not found"}), 404
    
    if request.method == 'GET':
        # Return all data from table
        return jsonify({
            'table': table_name,
            'data': mock_database[table_name],
            'count': len(mock_database[table_name])
        })
    
    elif request.method == 'POST':
        # Add new data to table
        data = request.get_json()
        mock_database[table_name].append(data)
        return jsonify({
            'status': 'success',
            'message': f'Data added to {table_name}',
            'data': data
        })

@app.route('/api/tables', methods=['GET'])
def list_tables():
    """List all available tables"""
    return jsonify({
        'tables': list(mock_database.keys()),
        'counts': {table: len(data) for table, data in mock_database.items()}
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
