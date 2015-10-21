from flask import jsonify, Response  # type: ignore
import json
from operator import itemgetter

from service import app, amazon_s3_connector


@app.route('/list-files/<dataset>', methods=['GET'])
def get_available_files(dataset):
    prefix = '{}{}/'.format(app.config['AWS_FOLDER_PREFIX'], dataset)
    file_list = amazon_s3_connector.get_file_list(prefix)

    new_list = []
    if 'Contents' in file_list:
        for file in file_list['Contents']:
            if file['Size'] > 0:
                list_item = {
                    "Name": file['Key'].replace(prefix, ''),
                    "Size": file['Size'],
                    "Checksum": file['ETag'],
                    "URL": amazon_s3_connector.get_download_url(file['Key'])
                }
                new_list.append(list_item.copy())

    # ensure list is ordered by date in filename
    if len(new_list) > 0:
        new_list.sort(key=itemgetter('Name'))

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
    return jsonify({"Endpoints": ['/health', '/list-files/<dataset>']})
