from flask import Flask, jsonify
from flask_cors import CORS
from calculation_functions import get_speed, calculate_eta_for_waypoints, get_estimated_delay

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Example fixed input values (can be dynamic later)
start_time = [10, 0, 0, 0]  # [hour, minute, second, microsecond]
planned_speed = 10  # knots

@app.route('/')
def index():
    return "Skippo Navigation API is running 🚤"

@app.route('/api/speed')
def api_speed():
    speed = get_speed()
    return jsonify({"speed": speed})

@app.route('/api/eta')
def api_eta():
    eta = calculate_eta_for_waypoints(start_time, planned_speed)
    return jsonify({"eta": eta})

@app.route('/api/delay')
def api_delay():
    eta_list = calculate_eta_for_waypoints(start_time, planned_speed)
    delay = get_estimated_delay(start_time, eta_list, waypoint_index=3)
    return jsonify({"delay": delay})

@app.route('/api/all')
def api_all():
    current_speed = get_speed()
    eta = calculate_eta_for_waypoints(start_time, current_speed)
    delay = get_estimated_delay(start_time, eta, waypoint_index=3)

    return jsonify({
        "speed": current_speed,
        "eta": eta,
        "delay": delay
    })

if __name__ == '__main__':
    app.run(debug=True)
