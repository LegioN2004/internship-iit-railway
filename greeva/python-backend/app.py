from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime
import os

# Flask app setup
app = Flask(
    __name__,
    template_folder='../templates',  # Point to Django templates
    static_folder='../static'        # Point to Django static files
)
CORS(app)

trains_data = [
    {"id": 1, "name": "debojeetor rajdhani express", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/007bff/ffffff?text=Train1"},
    {"id": 2, "name": "debo2 goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/28a745/ffffff?text=Train2"},
    {"id": 3, "name": "mili goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/dc3545/ffffff?text=Train3"},
    {"id": 4, "name": "goru goods Train", "status": "Finished", "image": "https://via.placeholder.com/120x80/ffc107/000000?text=Train4"},
    {"id": 5, "name": "manuh goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/6f42c1/ffffff?text=Train5"},
    {"id": 6, "name": "sixth goods Train", "status": "Finished", "image": "https://via.placeholder.com/120x80/20c997/ffffff?text=Train6"},
    {"id": 7, "name": "seventh goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/fd7e14/ffffff?text=Train7"},
    {"id": 8, "name": "eighth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/e83e8c/ffffff?text=Train8"},
    {"id": 9, "name": "ninth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/6610f2/ffffff?text=Train9"},
    {"id": 10, "name": "tenth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/198754/ffffff?text=Train10"},
    {"id": 11, "name": "eleventh goods Train", "status": "Finished", "image": "https://via.placeholder.com/120x80/0d6efd/ffffff?text=Train11"},
    {"id": 12, "name": "twelfth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/bb2d3b/ffffff?text=Train12"},
    {"id": 13, "name": "thirteenth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/f59e0b/000000?text=Train13"},
    {"id": 14, "name": "fourteenth goods Train", "status": "Finished", "image": "https://via.placeholder.com/120x80/059669/ffffff?text=Train14"},
    {"id": 15, "name": "fifteenth goods Train", "status": "Unfinished", "image": "https://via.placeholder.com/120x80/7c3aed/ffffff?text=Train15"},
]

@app.route('/trains', methods=['GET'])
def get_trains():
    """API endpoint to get all trains data"""
    return jsonify(trains_data)

@app.route('/train/<int:train_id>', methods=['GET'])
def get_train_details(train_id):
    """API endpoint to get specific train details"""
    train = next((t for t in trains_data if t['id'] == train_id), None)
    if train:
        return jsonify(train)
    return jsonify({"error": "Train not found"}), 404

@app.route('/train-report-data', methods=['GET'])
def get_train_report_data():
    """API endpoint to get train report data"""
    train_name = request.args.get('name', 'Unknown Train')
    train_status = request.args.get('status', 'Unknown')
    train_id = request.args.get('id', '1')

    # Sample train bogie images (you can replace with actual image URLs)
    sample_images = [
        'https://via.placeholder.com/100x60/007bff/ffffff?text=Bogie1',
        'https://via.placeholder.com/100x60/28a745/ffffff?text=Bogie2',
        'https://via.placeholder.com/100x60/dc3545/ffffff?text=Bogie3',
        'https://via.placeholder.com/100x60/ffc107/000000?text=Bogie4',
        '', # No image example
    ]

    # Generate detailed door data based on train
    door_details = []
    for i in range(1, 21):  # 20 doors for example
        marking_options = ['LI-SI', 'LI-SM', 'Broken-SI', 'Broken-SM', 'OTLI-SI', 'OTLI-SM']
        import random
        marking = random.choice(marking_options)

        # Randomly assign images (some doors have images, some don't)
        image_url = random.choice(sample_images) if i % 3 != 0 else ''

        door_details.append({
            'position': i,
            'door_number': i,
            'wagon_number': f'WG{str(i//4 + 1).zfill(3)}',
            'marking': marking,
            'image': image_url
        })

    # Count markings for summary
    marking_counts = {}
    for detail in door_details:
        marking = detail['marking']
        marking_counts[marking] = marking_counts.get(marking, 0) + 1

    report_data = {
        'train_name': train_name,
        'train_status': train_status,
        'train_number': f'TN{train_id.zfill(3)}',
        'train_side': 'Right Side',
        'station_name': 'Katihar Junction',
        'current_time': datetime.now().strftime("%I:%M %p"),
        'current_date': datetime.now().strftime("%d/%m/%Y"),
        'total_doors': len(door_details),
        'otli_si': marking_counts.get('OTLI-SI', 0),
        'otli_sm': marking_counts.get('OTLI-SM', 0),
        'li_si': marking_counts.get('LI-SI', 0),
        'li_sm': marking_counts.get('LI-SM', 0),
        'broken_si': marking_counts.get('Broken-SI', 0),
        'broken_sm': marking_counts.get('Broken-SM', 0),
        'door_details': door_details
    }

    return jsonify(report_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)