from flask import Flask, request, jsonify
import requests, time, re


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
