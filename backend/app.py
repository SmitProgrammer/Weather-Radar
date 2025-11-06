from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .mrms_service import MRMSService

load_dotenv()

# Initialize Flask with static folder
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, static_folder=static_folder, static_url_path='')
CORS(app)

mrms_service = MRMSService()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Weather Radar API'})

@app.route('/api/radar/latest', methods=['GET'])
def get_latest_radar():
    """Get the latest MRMS radar data"""
    try:
        print("Fetching latest radar data...")
        data = mrms_service.get_latest_radar_data()
        if data is None:
            print("No radar data available")
            return jsonify({'error': 'No radar data available'}), 404
        
        print(f"Returning radar data with {data.get('metadata', {}).get('count', 0)} features")
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching radar data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/radar/info', methods=['GET'])
def get_radar_info():
    """Get information about available radar data"""
    try:
        info = mrms_service.get_data_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
