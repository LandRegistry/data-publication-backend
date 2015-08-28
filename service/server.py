from flask import jsonify, Response  # type: ignore
import json
from operator import itemgetter

from service import app, amazon_s3_connector

@app.route('/list-files/<prefix>', methods=['GET'])
def get_available_files(prefix):
    file_list = amazon_s3_connector.get_file_list(prefix)

    new_list = []
    for file in file_list['Contents']:
        list_item = {
            "Name": file['Key'],
            "Size": file['Size'],
            "Checksum": file['ETag'],
            "URL": amazon_s3_connector.get_download_url(file['Key'])
        }
        new_list.append(list_item.copy())

    # ensure list is ordered by date in filename
    if new_list:
        new_list.sort(key=itemgetter('Key'))

    available_file_details = {
        "File_List": new_list,
        "Link_Duration": app.config['AWS_LINK_DURATION']
    }

    return jsonify(available_file_details)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"Status": "OK"})

@app.route('/', methods=['GET'])
def menu():
    return jsonify({"Endpoints": ['/health', '/list-files/<prefix>']})
