from flask import Flask, request, render_template, jsonify
from geopy.geocoders import Nominatim
import math

app = Flask(__name__)
geolocator = Nominatim(user_agent="route_optimization")

def haversine(coord1, coord2):
    # Haversine formula to calculate distance
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    start_address = data['start']
    goal_address = data['goal']
    # Additional fields: cargo needed, truck capacity, etc.
    
    start_coords = geocode_address(start_address)
    goal_coords = geocode_address(goal_address)
    
    if not start_coords or not goal_coords:
        return jsonify({'error': 'Invalid addresses'}), 400
    
    # Implement Dijkstra's or other algorithm to compute the route
    # For demo purposes, we'll just compute the distance
    distance = haversine(start_coords, goal_coords)
    
    result = {
        'optimized_path': [start_address, goal_address],
        'total_distance': distance
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
