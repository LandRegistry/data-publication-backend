import pytest
import datetime
import json

from service.server import app
from unittest import mock

no_files = {
    'IsTruncated': False,
    'Marker': 'Marker1',
    'NextMarker': 'Marker2',
    'Name': 'Name',
    'Prefix': 'OV',
    'Delimiter': '',
    'MaxKeys': 1000,
    'CommonPrefixes': [
        {
            'Prefix': ''
        },
    ],
    'EncodingType': 'url'
}
one_file = {
    'IsTruncated': False,
    'Marker': 'Marker1',
    'NextMarker': 'Marker2',
    'Contents': [
        {
            'Key': app.config['AWS_FOLDER_PREFIX'] + 'overseas-ownership/OV_FULL_2015_08.zip',
            'LastModified': datetime.date(2015, 1, 1),
            'ETag': 'ETag1234567890',
            'Size': 12345,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'DisplayName',
                'ID': 'id_string'
            }
        },
    ],
    'Name': 'Name',
    'Prefix': 'OV',
    'Delimiter': '',
    'MaxKeys': 1000,
    'CommonPrefixes': [
        {
            'Prefix': ''
        },
    ],
    'EncodingType': 'url'
}
multiple_files = {
    'IsTruncated': False,
    'Marker': 'Marker1',
    'NextMarker': 'Marker2',
    'Contents': [
        {
            'Key': app.config['AWS_FOLDER_PREFIX'] + 'overseas-ownership/',
            'LastModified': datetime.date(2015, 1, 1),
            'ETag': 'ETag1234567890',
            'Size': 0,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'DisplayName',
                'ID': 'id_string'
            }
        },{
            'Key': app.config['AWS_FOLDER_PREFIX'] + 'overseas-ownership/OV_FULL_2015_08.zip',
            'LastModified': datetime.date(2015, 1, 1),
            'ETag': 'ETag1234567890',
            'Size': 12345,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'DisplayName',
                'ID': 'id_string'
            }
        },
        {
            'Key': app.config['AWS_FOLDER_PREFIX'] + 'overseas-ownership/OV_UPDATE_2015_08.zip',
            'LastModified': datetime.date(2015, 1, 1),
            'ETag': 'ETag1234567891',
            'Size': 12345,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'DisplayName',
                'ID': 'id_string'
            }
        },
    ],
    'Name': 'Name',
    'Prefix': 'OV',
    'Delimiter': '',
    'MaxKeys': 1000,
    'CommonPrefixes': [
        {
            'Prefix': ''
        },
    ],
    'EncodingType': 'url'
}

presigned_url = "http://s3.amazon.uk/eu-west-1/presignedtokenstring"

class TestRetrieveFileDetails:

    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch('service.amazon_s3_connector.get_file_list', return_value=no_files)
    def test_get_available_files_none_found(self, mock_list):
        response = self.app.get('/list-files/overseas-ownership')
        content = response.data.decode()
        file_details = json.loads(content)
        assert response.status_code == 200
        assert len(file_details['File_List']) == 0

    @mock.patch('service.amazon_s3_connector.get_file_list', return_value=one_file)
    @mock.patch('service.amazon_s3_connector.get_download_url', return_value=presigned_url)
    def test_get_available_files_one_found(self, mock_list, mock_url):
        response = self.app.get('/list-files/overseas-ownership')
        content = response.data.decode()
        file_details = json.loads(content)
        assert response.status_code == 200
        assert len(file_details['File_List']) == 1
        assert file_details['File_List'][0]['Name'] == 'OV_FULL_2015_08.zip'
        assert file_details['File_List'][0]['URL'] == presigned_url

    @mock.patch('service.amazon_s3_connector.get_file_list', return_value=multiple_files)
    @mock.patch('service.amazon_s3_connector.get_download_url', return_value=presigned_url)
    def test_get_available_files_multiple_found(self, mock_list, mock_url):
        response = self.app.get('/list-files/overseas-ownership')
        content = response.data.decode()
        file_details = json.loads(content)
        assert response.status_code == 200
        assert len(file_details['File_List']) == 2
        assert file_details['File_List'][0]['Name'] == 'OV_FULL_2015_08.zip'
        assert file_details['File_List'][0]['URL'] == presigned_url
        assert file_details['File_List'][1]['Name'] == 'OV_UPDATE_2015_08.zip'
        assert file_details['File_List'][1]['URL'] == presigned_url
