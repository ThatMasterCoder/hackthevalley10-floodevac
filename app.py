from flask import Flask, jsonify, request, render_template
import time, requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Get the prompt from the request
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Add context for flood evacuation with more specific role definition
        flood_context = """You are FloodEvac Assistant, an AI specialist in flood evacuation and emergency preparedness.
        Your role is to:
        1. Provide clear, actionable advice for flood emergencies
        2. Help with evacuation planning and safety measures
        3. Respond in a calm, informative manner
        4. Always prioritize human safety first
        
        Format your responses in a clear, easy-to-read manner.
        If you need to list steps, number them clearly.
        If you provide emergency advice, highlight critical information."""
        
        full_prompt = f"{flood_context}\n\nUser message: {prompt}\n\nProvide a helpful, clear response:"
        
        # Generate response using Gemini with safety configurations
        try:
            response = model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                }
            )
            
            # Validate the response
            if not response:
                raise ValueError("Empty response from Gemini API")
            
            # Extract and validate the text
            response_text = getattr(response, 'text', None)
            if not response_text or not isinstance(response_text, str):
                raise ValueError("Invalid or missing response text")
            
            return jsonify({
                'response': response_text,
                'status': 'success'
            })
            
        except Exception as api_error:
            return jsonify({
                'error': f'AI Generation Error: {str(api_error)}',
                'status': 'error'
            }), 500
    
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Server Error: ' + str(e),
            'status': 'error',
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)