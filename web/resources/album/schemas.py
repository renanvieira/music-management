from marshmallow import Schema
from marshmallow.fields import Integer, String, DateTime, Date, Nested, Boolean
from marshmallow.validate import Length


class AlbumSchema(Schema):
    id = Integer(dump_only=True)
    artist = String(validate=Length(1, 64), allow_none=False, required=True)
    name = String(validate=Length(1, 64), allow_none=False, required=True)
    release_date = Date(allow_none=False)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)
    deleted_at = DateTime(dump_only=True)


class AlbumUpdateSchema(Schema):
    artist = String(validate=Length(1, 64), allow_none=False)
    name = String(validate=Length(1, 64), allow_none=False)
    release_date = Date(allow_none=False)


class AlbumListSchema(Schema):
    limit = Integer(default=10)
    total = Integer()
    total_pages = Integer(load_from="pages")
    items = Nested(AlbumSchema, many=True)
    has_more = Boolean(load_from="has_next")


album_schema = AlbumSchema(strict=True)
album_update_schema = AlbumUpdateSchema(strict=True)
album_list_schema = AlbumListSchema(strict=True)
