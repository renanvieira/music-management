from wtforms import Form, validators, StringField, DateField


class AlbumItem(object):
    def __init__(self, id, name, artist_name, release_date):
        self.id = id
        self.name = name
        self.artist = artist_name
        self.release_date = release_date

    @classmethod
    def parse_from_json_dict(cls, json_dict):
        return AlbumItem(id=json_dict["id"],
                         name=json_dict["name"],
                         artist_name=json_dict["artist"],
                         release_date=json_dict["release_date"])


class AlbumTable(object):

    def __init__(self, items: list, total_pages, total_items):
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items

    @classmethod
    def parse_from_json_dict(cls, json_dict):
        items = list()

        for item in json_dict["items"]:
            items.append(AlbumItem.parse_from_json_dict(item))

        return AlbumTable(items, json_dict["total_pages"], json_dict["total"])


class AddAlbumForm(Form):
    artist_name = StringField('Artist Name:', validators=[validators.required(), validators.Length(min=1, max=64)])
    name = StringField('Album Name:', validators=[validators.required(), validators.Length(min=1, max=64)])
    release_date = DateField('Release Date:', validators=[validators.required()])


API_FORM_MAP = {
    "artist": "artist_name",
    "name": "name",
    "release_date": "release_date"
}
