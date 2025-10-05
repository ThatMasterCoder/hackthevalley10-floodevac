# FloodEvac

A comprehensive web application for flood risk assessment, evacuation route planning, and real-time flood monitoring. Built for Hack the Valley 10.

## Features

### Interactive Flood Risk Map
- View global flood risk zones on an interactive map powered by OpenTopoMap
- Search for any location worldwide using intelligent city search
- Real-time elevation data retrieval for any coordinate
- Visual disaster risk indicators for selected locations
- Click-to-place markers and explore flood-prone areas

### Flood Height Calculator
- Calculate potential flood water height based on elevation and flood severity
- Input custom location coordinates or use suggested questions
- Get detailed safety recommendations and evacuation guidance
- AI-powered chat assistant for flood-related queries
- Personalized risk assessment with actionable next steps

### Recent Floods Dashboard
- Live feed of global flood events from the last 90 days
- Data sourced from GDACS (Global Disaster Alert and Coordination System)
- Severity indicators (Red, Orange, Green alerts)
- Affected population statistics
- Direct links to view flood locations on the map

### FloodEvac AI Assistant
- Powered by Google Gemini AI
- Context-aware responses about flood safety
- Pre-populated suggestion buttons for common questions
- Natural language interface for evacuation planning

## Technology Stack

**Backend:**
- Flask (Python web framework)
- Google Generative AI (Gemini API)
- Open-Elevation API
- GDACS API for disaster data

**Frontend:**
- HTML5, CSS3, JavaScript
- Leaflet.js for interactive maps
- Bootstrap 5 for responsive design
- Custom CSS with modern animations

**APIs Used:**
- OpenTopoMap tiles
- Nominatim (OpenStreetMap) for geocoding
- Open-Elevation for elevation data
- GDACS for real-time flood alerts
- Google Gemini for AI chat functionality

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Gemini API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ThatMasterCoder/hackthevalley10-floodevac.git
cd hackthevalley10-floodevac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
hackthevalley10-floodevac/
├── app.py                  # Main Flask application
├── methods.py              # Helper functions and API integrations
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── templates/
│   ├── home.html          # Landing page
│   ├── map.html           # Interactive map interface
│   ├── flood-calculator.html  # Flood height calculator
│   ├── recent-floods.html # Global flood events dashboard
│   └── ai-chat.html       # AI assistant interface
└── static/
    └── css/
        ├── modern.css     # Chat interface styling
        └── suggestions.css # Suggestion button styling
```

## Usage

### Finding Flood Risk for a Location
1. Navigate to the Interactive Map
2. Search for a city or click anywhere on the map
3. View elevation data and disaster risk information
4. Check the risk level indicator (Low, Moderate, High, Very High)

### Calculating Flood Heights
1. Go to the Flood Calculator page
2. Enter latitude, longitude, and flood severity (1-10)
3. Receive estimated flood water height and safety recommendations
4. Use the AI chat for specific questions about your situation

### Monitoring Recent Floods
1. Access the Recent Floods page
2. Browse the table of current flood events
3. Filter by location, date, or severity
4. Click "View on Map" to see the exact location

### Using the AI Assistant
1. Type your question in the chat box
2. Or click a suggested question button
3. Receive personalized flood safety guidance
4. Ask follow-up questions for more details

## API Endpoints

- `GET /` - Home page
- `GET /map` - Interactive map interface
- `GET /flood-height-calculator` - Calculator page
- `GET /recent-floods` - Flood events dashboard
- `GET /elevation?lat=<lat>&lng=<lng>` - Get elevation data
- `GET /api/recent-floods` - Fetch GDACS flood data
- `POST /chat` - AI chat endpoint

## Configuration

### Environment Variables
- `GEMINI_API_KEY` - Required for AI chat functionality

### Port Configuration
The application runs on port 5000 by default. To change:
```python
app.run(debug=True, port=YOUR_PORT)
```

## Contributing

This project was developed for Hack the Valley 10. Contributions, issues, and feature requests are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GDACS for real-time disaster data
- OpenStreetMap contributors for map tiles and geocoding
- Open-Elevation for elevation data
- Google for Gemini AI API
- Hack the Valley organizing team

## Contact

Project Link: https://github.com/ThatMasterCoder/hackthevalley10-floodevac

## Future Enhancements

- Mobile application version
- Push notifications for local flood alerts
- Historical flood data visualization
- Community reporting features
- Multi-language support
- Offline map capabilities
