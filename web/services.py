import logging
from http import HTTPStatus

import requests
from flask import flash, current_app

from web.models import API_FORM_MAP, AlbumTable, AlbumItem
from web.resources.error import APIValidationError, APIError

logger = logging.getLogger(__name__)


class MusicManagementAPIClient(object):

    @staticmethod
    def list_all(current_page=1):
        try:
            if current_page <= 0:
                current_page = 1

            result = requests.get(f"{current_app.config['BASE_API_ENDPOINT']}/albums?page={current_page}")

            if result.status_code == HTTPStatus.OK:
                json_result = result.json()
                return AlbumTable.parse_from_json_dict(json_result), HTTPStatus.OK

        except Exception as e:
            current_app.logger.exception(e)
            raise APIError()

    @staticmethod
    def get_album_by_id(id):
        try:
            result = requests.get(f"{current_app.config['BASE_API_ENDPOINT']}/albums/{id}")

            if result.status_code == HTTPStatus.OK:
                data = AlbumItem.parse_from_json_dict(result.json())
            else:
                data = result.content.decode("utf-8")

            return data, result.status_code
        except Exception as e:
            current_app.logger.exception(e)
            raise APIError()

    @staticmethod
    def add_album(data: dict):
        try:
            result = requests.post(f"{current_app.config['BASE_API_ENDPOINT']}/albums", json=data)

            if result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                return None, result.status_code
            elif result.status_code == HTTPStatus.BAD_REQUEST:

                field_messages = MusicManagementAPIClient.__parser_validation_errors(result.json())

                raise APIValidationError(field_messages)

            return result.json(), result.status_code
        except APIValidationError as v_err:
            raise
        except Exception as e:
            current_app.logger.exception(e)
            raise APIError()

    @staticmethod
    def update_album(id, payload):
        try:
            result = requests.post(f"{current_app.config['BASE_API_ENDPOINT']}/albums/{id}", json=payload)

            if result.status_code == HTTPStatus.OK:
                return result.json(), result.status_code
            elif result.status_code == HTTPStatus.NOT_FOUND:
                return result.content.decode("utf-8"), result.status_code
            elif result.status_code == HTTPStatus.BAD_REQUEST:
                field_messages = MusicManagementAPIClient.__parser_validation_errors(result.json())

                raise APIValidationError(field_messages)
            else:
                current_app.logger.info(result.content)
                raise APIError()
        except APIValidationError as v_err:
            raise
        except Exception as e:
            current_app.logger.exception(e)
            raise APIError()

    @staticmethod
    def delete_album(id):
        try:
            result = requests.delete(f"{current_app.config['BASE_API_ENDPOINT']}/albums/{id}")

            if result.status_code == HTTPStatus.OK:
                return result.json(), result.status_code
            elif result.status_code == HTTPStatus.NOT_FOUND:
                return result.content.decode("utf-8"), result.status_code
            else:
                current_app.logger.info(result.content)
                raise APIError()
        except Exception as e:
            current_app.logger.exception(e)
            raise APIError()

    @staticmethod
    def __parser_validation_errors(errors):
        if "error" in errors and "validation_errors" in errors["error"]:
            field_messages = dict()

            for err in errors["error"]["validation_errors"]:
                field = API_FORM_MAP[err['field']]
                msg = err['message']
                field_messages[field] = msg

            return field_messages
