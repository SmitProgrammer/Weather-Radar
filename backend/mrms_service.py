import requests
import xarray as xr
import numpy as np
import os
import tempfile
from datetime import datetime, timedelta
import json
from pathlib import Path

class MRMSService:
    """Service for fetching and processing MRMS radar data"""
    
    # MRMS RALA (Reflectivity at Lowest Altitude) via AWS S3 (publicly accessible)
    # NOAA hosts MRMS data on AWS Open Data Program
    MRMS_BASE_URLS = [
        "https://noaa-mrms-pds.s3.amazonaws.com/CONUS/MergedReflectivityAtLowestAltitude_00.50/",
        "https://noaa-mrms-pds.s3.amazonaws.com/CONUS/MergedReflectivityQCComposite_00.50/",
        "https://noaa-mrms-pds.s3.amazonaws.com/CONUS/MergedBaseReflectivity_00.50/",
    ]
    
    def __init__(self, cache_dir='cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_duration = 300  # 5 minutes cache
        
    def get_latest_file_url(self):
        """
        Get the URL of the latest MRMS RALA file from AWS S3.
        S3 bucket structure: CONUS/Product/YYYYMMDD/filename.grib2.gz
        """
        import xml.etree.ElementTree as ET
        from datetime import datetime, timedelta
        
        # Try each base URL
        for base_url in self.MRMS_BASE_URLS:
            try:
                print(f"Trying S3 bucket: {base_url}")
                
                # Try last 7 days to find recent data
                for days_ago in range(0, 7):
                    check_date = datetime.utcnow() - timedelta(days=days_ago)
                    date_str = check_date.strftime('%Y%m%d')
                    prefix = f"{base_url.replace('https://noaa-mrms-pds.s3.amazonaws.com/', '')}{date_str}/"
                    
                    # List objects in S3 bucket for this date
                    list_url = f"https://noaa-mrms-pds.s3.amazonaws.com/?prefix={prefix}&max-keys=1000"
                    response = requests.get(list_url, timeout=10)
                    
                    if response.status_code != 200:
                        continue
                    
                    # Parse S3 XML listing
                    root = ET.fromstring(response.content)
                    
                    # Extract all .grib2.gz files with their timestamps
                    namespace = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
                    files = []
                    
                    for contents in root.findall('s3:Contents', namespace):
                        key_elem = contents.find('s3:Key', namespace)
                        last_modified = contents.find('s3:LastModified', namespace)
                        
                        if key_elem is not None and key_elem.text:
                            filename = key_elem.text
                            if filename.endswith('.grib2.gz') or filename.endswith('.grib2'):
                                timestamp_str = last_modified.text if last_modified is not None else None
                                files.append({
                                    'filename': filename.split('/')[-1],  # Just the filename
                                    'url': f"https://noaa-mrms-pds.s3.amazonaws.com/{filename}",
                                    'timestamp': timestamp_str
                                })
                    
                    if files:
                        # Sort by timestamp (most recent first)
                        files.sort(key=lambda x: x['timestamp'] if x['timestamp'] else '', reverse=True)
                        latest = files[0]
                        print(f"Latest file: {latest['filename']} from {date_str}")
                        return latest['url'], latest['filename']
                    
            except Exception as e:
                print(f"Error with {base_url}: {e}")
                continue
        
        # If all URLs fail, raise error
        raise Exception("Could not fetch MRMS data from any S3 bucket")
    
    
    def download_grib_file(self, url):
        """Download GRIB2 file to temporary location (handles .gz compression)"""
        import gzip
        
        try:
            print(f"Downloading: {url}")
            
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, timeout=60, headers=headers, allow_redirects=True)
            response.raise_for_status()
            
            # Check if file is gzipped
            is_gzipped = url.endswith('.gz')
            
            # Save to temporary file
            if is_gzipped:
                # Decompress gzip file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.grib2')
                temp_file.write(gzip.decompress(response.content))
                temp_file.close()
                print(f"Downloaded and decompressed {len(response.content)} bytes")
            else:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.grib2')
                temp_file.write(response.content)
                temp_file.close()
                print(f"Downloaded {len(response.content)} bytes")
            
            return temp_file.name
        except requests.exceptions.HTTPError as e:
            print(f"Error downloading file: {e}")
            print(f"Final URL after redirects: {e.response.url if hasattr(e, 'response') else 'unknown'}")
            raise
        except Exception as e:
            print(f"Error downloading file: {e}")
            raise
    
    def process_grib_data(self, grib_file_path):
        """Process GRIB2 file and extract radar data"""
        try:
            # Open GRIB2 file with xarray and cfgrib
            # Use chunks to reduce memory usage
            ds = xr.open_dataset(grib_file_path, engine='cfgrib', 
                                backend_kwargs={'errors': 'ignore'})
            
            # Get reflectivity data (variable name may vary)
            # Common names: 'unknown', 'refc', 'reflectivity'
            var_name = None
            for var in ds.data_vars:
                if 'unknown' in var.lower() or 'refc' in var.lower() or 'reflectivity' in var.lower():
                    var_name = var
                    break
            
            if var_name is None:
                # Just use the first variable
                var_name = list(ds.data_vars)[0]
            
            print(f"Processing variable: {var_name}")
            reflectivity = ds[var_name]
            
            # Get coordinates
            lats = ds['latitude'].values
            lons = ds['longitude'].values
            values = reflectivity.values
            
            print(f"Data shape: {values.shape}, Lat range: [{lats.min():.2f}, {lats.max():.2f}], Lon range: [{lons.min():.2f}, {lons.max():.2f}]")
            
            # Get timestamp
            if 'time' in ds.coords:
                timestamp = str(ds['time'].values)
            else:
                timestamp = datetime.utcnow().isoformat()
            
            ds.close()
            
            return {
                'lats': lats,
                'lons': lons,
                'values': values,
                'timestamp': timestamp
            }
            
        except Exception as e:
            print(f"Error processing GRIB file: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def convert_to_geojson(self, data):
        """Convert radar data to GeoJSON format for frontend"""
        lats = data['lats']
        lons = data['lons']
        values = data['values']
        
        # Create GeoJSON features
        features = []
        
        # Sample the data to reduce size (every Nth point)
        # MRMS has very high resolution, we can downsample for web display
        step = 10  # Increased from 3 to 10 for better performance
        
        for i in range(0, len(lats), step):
            for j in range(0, len(lons), step):
                val = float(values[i, j])
                
                # Skip invalid/missing values (typically -999 or NaN)
                if np.isnan(val) or val < -90:
                    continue
                
                # Only include significant reflectivity (>= 15 dBZ for performance)
                # Lower values are usually light precipitation/clutter
                if val >= 15:
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [float(lons[j]), float(lats[i])]
                        },
                        'properties': {
                            'reflectivity': round(val, 1)
                        }
                    })
        
        return {
            'type': 'FeatureCollection',
            'features': features,
            'metadata': {
                'timestamp': data['timestamp'],
                'count': len(features),
                'product': 'MRMS Reflectivity at Lowest Altitude'
            }
        }
    
    def get_cached_data(self):
        """Get cached radar data if available and fresh"""
        cache_file = self.cache_dir / 'latest_radar.json'
        
        if cache_file.exists():
            # Check if cache is still fresh
            cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
            
            if cache_age < self.cache_duration:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        return None
    
    def cache_data(self, data):
        """Cache processed radar data"""
        cache_file = self.cache_dir / 'latest_radar.json'
        
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    
    def get_latest_radar_data(self):
        """Main method to get latest radar data (with caching)"""
        # Check cache first
        cached = self.get_cached_data()
        if cached:
            print("Returning cached data")
            return cached
        
        try:
            # Get latest file URL
            url, filename = self.get_latest_file_url()
            print(f"Latest file: {filename}")
            
            # Download GRIB file
            grib_path = self.download_grib_file(url)
            
            try:
                # Process GRIB data
                processed_data = self.process_grib_data(grib_path)
                
                # Convert to GeoJSON
                geojson = self.convert_to_geojson(processed_data)
                
                # Cache the result
                self.cache_data(geojson)
                
                return geojson
                
            finally:
                # Clean up temp file
                if os.path.exists(grib_path):
                    os.remove(grib_path)
                    
        except Exception as e:
            print(f"Error in get_latest_radar_data: {e}")
            # Return cached data even if stale, if available
            cache_file = self.cache_dir / 'latest_radar.json'
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
            return None
    
    def get_data_info(self):
        """Get information about the service and cached data"""
        cache_file = self.cache_dir / 'latest_radar.json'
        
        info = {
            'service': 'MRMS Reflectivity at Lowest Altitude',
            'update_frequency': '2 minutes',
            'cache_duration': f'{self.cache_duration} seconds'
        }
        
        if cache_file.exists():
            cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
            info['cache_age_seconds'] = round(cache_age, 1)
            info['cache_fresh'] = cache_age < self.cache_duration
        else:
            info['cache_age_seconds'] = None
            info['cache_fresh'] = False
        
        return info
