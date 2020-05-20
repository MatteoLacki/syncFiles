import argparse
from flask import Flask, jsonify, request
import socket
from pathlib import Path
from platform import system as OS

from syncFiles.syncFiles import check_sum


DEBUG = True
currentIP = socket.gethostbyname(socket.gethostname())



ap = argparse.ArgumentParser(description='Run a deamon that checks sums of sent files.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

ap.add_argument('storage_folder_path',
                help='Path to the folder where the data is supposed to be moved.',
                type=Path)
ap.add_argument('--host',
                help="Host's IP.",
                default=currentIP)
ap.add_argument('--port', 
                help='Port to listen to.', 
                default=9001, 
                type=int)
ap = ap.parse_args()
app  = Flask(__name__)




@app.route('/')
def index():
    return 'checkSummer operating.'

@app.route('/check', methods=['POST'])
def get_project_id():
    if request.data:
        print(request.data)
        print(ap.storage_folder_path)
        relative_path, check_sum_kwds = request.get_json()
        local_abs_file_path = ap.storage_folder_path/relative_path
        cs = check_sum(local_abs_file_path, **check_sum_kwds)
        return jsonify(cs)



if __name__ == '__main__':
    app.run(debug=DEBUG,
            host=ap.host,
            port=ap.port,
            threaded=True)