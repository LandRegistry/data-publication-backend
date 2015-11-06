from flask import jsonify, Response, abort  # type: ignore
import json
from operator import itemgetter

from service import app, amazon_s3_connector, logger_config

import botocore.exceptions

logger = logger_config.LoggerConfig(app)
logger.setup_logger(__name__)

@app.route('/list-files/<dataset>', methods=['GET'])
@logger.start_stop_logging
def get_available_files(dataset):
    prefix = '{}{}/'.format(app.config['AWS_FOLDER_PREFIX'], dataset)
    try:
        file_list = amazon_s3_connector.get_file_list(prefix)
    except botocore.exceptions.ClientError as e:
        logger.log("An error occurred while retrieving file list.", level="ERROR", exception=e)
        file_list = {}

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
    try:
        amazon_s3_connector.get_file_list(app.config['AWS_FOLDER_PREFIX'])
        status = "OK"
    except botocore.exceptions.ClientError:
        status = "Error"

    response_body = {'status': status}

    if status == "Error":
        status_code = 500
        response_body['error'] = 'Error contacting Amazon S3 bucket'
    else:
        status_code = 200

    return Response(
        json.dumps(response_body),
        status=status_code,
        mimetype='application/json',
    )
