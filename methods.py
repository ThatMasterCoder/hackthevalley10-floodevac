from flask import Flask, request, jsonify
import requests, time, re
from datetime import datetime, timedelta


def get_severity_label(severity):
    """
    Convert GDACS alert level codes to human-readable severity labels
    Red = Extreme, Orange = Severe, Green = Moderate
    """
    severity_str = str(severity).lower().strip()
    
    severity_map = {
        'red': 'Extreme',
        'orange': 'Severe', 
        'green': 'Moderate',
        '3': 'Extreme',
        '2': 'Severe',
        '1': 'Moderate'
    }
    
    return severity_map.get(severity_str, 'Unknown')


def get_elevation():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    # Try OpenTopodata SRTM90m first
    try:
        resp = requests.get(f'https://api.opentopodata.org/v1/srtm90m?locations={lat},{lng}', timeout=5)
        data = resp.json()
        if data and 'results' in data and data['results'][0]['elevation'] is not None:
            return jsonify(data)
    except Exception:
        pass
    # Fallback to Open-Elevation
    try:
        resp = requests.get(f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}', timeout=5)
        data = resp.json()
        if data and 'results' in data and data['results'][0]['elevation'] is not None:
            return jsonify(data)
    except Exception:
        pass
    # If all fail, return N/A
    return jsonify({"results": [{"elevation": None}]})


def get_recent_floods():
    """
    Fetch recent flood events from GDACS (Global Disaster Alert and Coordination System)
    Returns a list of recent flood disasters worldwide
    """
    try:
        # GDACS RSS feed for floods
        url = 'https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH'
        params = {
            'eventtype': 'FL',  # FL = Flood
            'fromdate': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),  # Last 90 days
            'todate': datetime.now().strftime('%Y-%m-%d')
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse and structure the flood data
            floods = []
            if 'features' in data:
                for feature in data.get('features', []):
                    props = feature.get('properties', {})
                    geom = feature.get('geometry', {})
                    coords = geom.get('coordinates', [None, None])
                    
                    flood_info = {
                        'name': props.get('name', 'Unknown Location'),
                        'country': props.get('country', 'Unknown'),
                        'description': props.get('description', 'No description available'),
                        'date': props.get('fromdate', 'Unknown date'),
                        'severity': props.get('alertlevel', 'Unknown'),
                        'severity_label': get_severity_label(props.get('alertlevel', 'Unknown')),
                        'affected_population': props.get('population', 'Unknown'),
                        'latitude': coords[1] if len(coords) > 1 else None,
                        'longitude': coords[0] if len(coords) > 0 else None,
                        'event_id': props.get('eventid', None)
                    }
                    floods.append(flood_info)
            
            # Sort floods by date in descending order (most recent first)
            floods.sort(key=lambda x: x['date'] if x['date'] != 'Unknown date' else '', reverse=True)
            
            return {
                'status': 'success',
                'count': len(floods),
                'floods': floods
            }
        else:
            return {
                'status': 'error',
                'message': f'API returned status code {response.status_code}',
                'floods': []
            }
            
    except Exception as e:
        print(f"Error fetching flood data: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'floods': []
        }


# regular expressions lol i love regex (i hate it)
def convert_markdown_to_html(text):
    """Convert basic markdown formatting to HTML"""
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em>italic</em>
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Convert line breaks to <br> tags
    text = text.replace('\n', '<br>')
    
    # Convert bullet points starting with * or - to HTML lists
    lines = text.split('<br>')
    in_list = False
    result_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('* ') or stripped.startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{stripped[2:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    return '<br>'.join(result_lines)
