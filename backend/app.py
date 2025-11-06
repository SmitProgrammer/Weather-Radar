from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .mrms_service import MRMSService

load_dotenv()

app = Flask(__name__)
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
        data = mrms_service.get_latest_radar_data()
        if data is None:
            return jsonify({'error': 'No radar data available'}), 404
        
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching radar data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/radar/info', methods=['GET'])
def get_radar_info():
    """Get information about available radar data"""
    try:
        info = mrms_service.get_data_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
