"""
Simple test script to verify MRMS data fetching works
Run with: python test_mrms.py
"""

from mrms_service import MRMSService
import json

def test_mrms_service():
    print("=" * 60)
    print("Testing MRMS Service")
    print("=" * 60)
    
    service = MRMSService()
    
    print("\n1. Getting service info...")
    try:
        info = service.get_data_info()
        print(f"   ✓ Service: {info['service']}")
        print(f"   ✓ Update frequency: {info['update_frequency']}")
        print(f"   ✓ Cache duration: {info['cache_duration']}")
        print(f"   ✓ Cache fresh: {info['cache_fresh']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n2. Fetching latest radar data...")
    print("   (This may take 30-60 seconds on first run)")
    try:
        data = service.get_latest_radar_data()
        
        if data is None:
            print("   ✗ No data returned")
            return False
        
        print(f"   ✓ Data received!")
        print(f"   ✓ Features: {data['metadata']['count']}")
        print(f"   ✓ Timestamp: {data['metadata']['timestamp']}")
        print(f"   ✓ Product: {data['metadata']['product']}")
        
        # Save sample to file
        with open('sample_radar_data.json', 'w') as f:
            # Save only first 10 features as sample
            sample = {
                'type': data['type'],
                'features': data['features'][:10],
                'metadata': data['metadata']
            }
            json.dump(sample, f, indent=2)
        print("\n   ✓ Sample data saved to: sample_radar_data.json")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the Flask server: python app.py")
    print("2. Test API: http://localhost:5000/api/health")
    print("3. Get radar data: http://localhost:5000/api/radar/latest")
    
    return True

if __name__ == "__main__":
    test_mrms_service()
