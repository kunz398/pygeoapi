import os
import subprocess
from flask import Flask
from flask_cors import CORS

if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)  # directory where main.py is located

    # Absolute paths to your config and openapi files
    config_path = os.path.join(base_dir, 'pygeoapi-generate-config', 'pygeoapi-config.yml')
    openapi_path = os.path.join(base_dir, 'pygeoapi-generate-config', 'openapi.yml')

    # Set environment variables for pygeoapi
    os.environ['PYGEOAPI_CONFIG'] = config_path
    os.environ['PYGEOAPI_OPENAPI'] = openapi_path
    os.environ.setdefault('PYGEOAPI_SERVER_URL', 'http://localhost:5000')
    print(f"PYGEOAPI_SERVER_URL={os.environ.get('PYGEOAPI_SERVER_URL')}")

    # run with Flask and CORS
    from pygeoapi.flask_app import APP as app
    
    # Enable CORS for all routes
    CORS(app, origins=[
        "*"
    ], supports_credentials=True)
    
    # Add custom headers for tile requests to comply with OSM usage policy
    @app.before_request
    def add_headers():
        from flask import request, g
        if request.endpoint and 'tile' in str(request.endpoint):
            g.user_agent = 'DMS-PyGeoAPI/1'
    
    app.run(host='0.0.0.0', port=5000, debug=True)

    # run pygeoapi with Django (commented out for now)
    # subprocess.run(['pygeoapi', 'serve', '--django'])
