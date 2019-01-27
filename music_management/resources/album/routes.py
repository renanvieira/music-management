import json
from datetime import datetime
from http import HTTPStatus

import marshmallow
from flask import Blueprint
from flask import request, current_app as app

from music_management.db import db_context as db
from music_management.helpers import PaginatorHelper
from music_management.models import (Album)
from music_management.resources.album.schemas import (album_schema, album_update_schema, album_list_schema)
from music_management.resources.error import (ResponseError,
                                              ValidationError,
                                              ObjectAlreadyRegisteredError, ObjectNotFound)

album_blueprint = Blueprint("album", __name__, url_prefix="/api")


@album_blueprint.route("/albums", methods=["POST"])
def create_album():
    try:
        schema = album_schema.load(request.get_json()).data

        if Album.query.filter_by(name=schema["name"]).count() > 0:
            return json.dumps(
                ObjectAlreadyRegisteredError().new("album", "name", schema["name"])), HTTPStatus.BAD_REQUEST

        album = Album(name=schema["name"], artist=schema["artist"], release_date=schema["release_date"])

        db.session.add(album)
        db.session.commit()

        return json.dumps(album_schema.dump(album).data)

    except marshmallow.ValidationError as validation_err:
        app.logger.exception(validation_err)
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(validation_err)), HTTPStatus.BAD_REQUEST

    except Exception as e:
        app.logger.exception(e)
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@album_blueprint.route("/albums/<album_id>", methods=["GET"])
def get_album(album_id):
    try:

        album = Album.query.filter(Album.id == album_id, Album.deleted_at.is_(None)).first()

        if album is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        return json.dumps(album_schema.dump(album).data)

    except Exception as e:
        app.logger.exception(e)
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@album_blueprint.route("/albums/<album_id>", methods=["POST"])
def edit_album(album_id):
    try:
        schema = album_update_schema.load(request.get_json()).data

        album = Album.query.filter(Album.id == album_id, Album.deleted_at.is_(None)).first()

        if album is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        if "name" in schema:
            criterion = [Album.name == schema["name"]]
            if "artist" in schema:
                criterion.append(Album.artist == schema["artist"])
            else:
                criterion.append(Album.artist == album.artist)

            if Album.query.filter(*criterion).count() > 0:
                return json.dumps(
                    ObjectAlreadyRegisteredError().new("album", "name", schema["name"])), HTTPStatus.BAD_REQUEST

        for key, val in schema.items():
            setattr(album, key, val)

        db.session.add(album)
        db.session.commit()

        return json.dumps(album_schema.dump(album).data)

    except marshmallow.ValidationError as validation_err:
        app.logger.exception(validation_err)
        return json.dumps(ValidationError.new_from_marshmallow_error_dict(validation_err)), HTTPStatus.BAD_REQUEST
    except Exception as e:
        app.logger.exception(e)
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@album_blueprint.route("/albums/<int:id>", methods=["DELETE"])
def delete_album(id):
    try:
        plan = Album.query.filter(Album.id == id, Album.deleted_at.is_(None)).first()

        if plan is None:
            return json.dumps(ObjectNotFound().new()), HTTPStatus.NOT_FOUND

        plan.deleted_at = datetime.utcnow()

        db.session.add(plan)
        db.session.commit()

        return album_schema.dumps(plan).data, HTTPStatus.OK

    except Exception as e:
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR


@album_blueprint.route("/albums", methods=["GET"])
def list_all_albums():
    try:
        criterion = [Album.deleted_at.is_(None)]
        get_deleted = request.args.get('deleted')
        page = int(request.args.get("page", 1))

        if get_deleted is not None and get_deleted.lower() in ["true", "false"] and bool(get_deleted) is True:
            criterion = []

        plan_paginator = Album.query.filter(*criterion).paginate(page, app.config['ITEMS_PER_PAGE'])

        paginated_data = PaginatorHelper.get_paginator_dict(plan_paginator)

        return album_list_schema.dumps(paginated_data).data

    except Exception as e:
        app.logger.exception(e)
        return json.dumps(ResponseError.new_generic_error()), HTTPStatus.INTERNAL_SERVER_ERROR
