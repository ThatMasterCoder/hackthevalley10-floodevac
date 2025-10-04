from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv
from methods import get_elevation, convert_markdown_to_html

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@app.route('/flood-height-calculator')
def flood_height_calculator():
    return render_template('flood-calculator.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/elevation', methods=['GET'])
def elevation():
    return get_elevation()

@app.route('/location-disasters', methods=['POST'])
def location_disasters():
    try:
        # Get location data from the request
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        region = data.get('region', 'this location')
        
        if lat is None or lng is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        # Create a prompt for natural disaster information
        disaster_prompt = f"""You are a natural disaster expert. For the location at coordinates {lat}, {lng} (region: {region}), 
        provide a brief, informative summary (3-4 sentences) about the most common natural disasters that could occur in this area.
        
        Consider: floods, hurricanes, earthquakes, wildfires, tornadoes, tsunamis, etc.
        Be specific to the geographic region and climate. Focus on the top 2-3 most likely disasters.
        Keep it concise and actionable."""
        
        # Generate response using Gemini
        response = model.generate_content(disaster_prompt)
        
        # Check if response has text
        if hasattr(response, 'text') and response.text:
            # Convert markdown formatting to HTML
            formatted_response = convert_markdown_to_html(response.text)
            
            return jsonify({
                'response': formatted_response,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'No response generated from AI',
                'status': 'error'
            }), 500
    
    except Exception as e:
        import traceback
        print(f"Error in location_disasters: {str(e)}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Get the prompt from the request
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Add context for flood evacuation
        flood_context = """You are a helpful AI assistant specializing in flood evacuation and emergency preparedness. 
        Provide clear, actionable advice for flood emergencies. Always prioritize safety first."""
        
        full_prompt = f"{flood_context}\n\nUser question: {prompt}"
        
        # Generate response using Gemini
        response = model.generate_content(full_prompt)
        
        # Check if response has text
        if hasattr(response, 'text') and response.text:
            # Convert markdown formatting to HTML
            formatted_response = convert_markdown_to_html(response.text)
            
            return jsonify({
                'response': formatted_response,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'No response generated from AI',
                'status': 'error',
                'debug_info': str(response)
            }), 500
    
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(f"API Key present: {'GEMINI_API_KEY' in os.environ}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'status': 'error',
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)