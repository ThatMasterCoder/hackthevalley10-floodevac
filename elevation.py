from flask import Flask, request, jsonify
import requests, time


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