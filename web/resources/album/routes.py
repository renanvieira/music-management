from http import HTTPStatus

import requests
from flask import Blueprint, render_template, current_app as app, request, flash, redirect
from flask_wtf.csrf import CSRFError

from web.models import AlbumTable, AddAlbumForm, AlbumItem, API_FORM_MAP

blueprint = Blueprint("album", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    current_route = "index"
    current_page = int(request.args.get("page", 1))
    table_data = AlbumTable(list(), 0, 0)

    try:
        result = requests.get(f"{app.config['BASE_API_ENDPOINT']}/albums?page={current_page}")

        if result.status_code == HTTPStatus.OK:
            json_result = result.json()
            table_data = AlbumTable.parse_from_json_dict(json_result)
    except Exception as e:
        app.logger.exception(e)
        flash("Error trying to load album list.", "danger")

    if current_page != 1 and table_data.total_pages == 0:
        current_page = 1

    return render_template("albums/index.html",
                           data=table_data,
                           page_name=current_route,
                           current_page=current_page,
                           prev_page=current_page - 1 if current_page > 1 else False,
                           next_page=current_page + 1 if current_page < table_data.total_pages else False,
                           page_list=range(1, table_data.total_pages + 1))


@blueprint.route("/add", methods=["GET"])
def add():
    current_route = "add_form"
    form = AddAlbumForm(request.form)

    return render_template("albums/add.html", form=form, page_name=current_route)


@blueprint.route("/add", methods=["POST"])
def add_album():
    current_route = "add_form"
    form = AddAlbumForm(request.form)

    if form.validate():
        payload = dict()
        payload["artist"] = request.form["artist_name"]
        payload["name"] = request.form["name"]
        payload["release_date"] = request.form["release_date"]

        try:
            result = requests.post(f"{app.config['BASE_API_ENDPOINT']}/albums", json=payload)
            if result.status_code != HTTPStatus.OK:
                flash(f"Error while trying to talk with API: API returned HTTP {result.status_code}", "danger")
            else:
                flash(f"Album added successfully.", "success")
                return redirect("/")
        except Exception as e:
            app.logger.exception(e)
            flash(f"Error while trying to talk with API.", "danger")
    else:
        for field, msg_list in form.errors.items():
            flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg_list[0]}", "validation_error")

    return render_template("albums/add.html", form=form, page_name=current_route)


@blueprint.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    current_route = "edit_form"

    try:
        result = requests.get(f"{app.config['BASE_API_ENDPOINT']}/albums/{id}")

        if result.status_code == HTTPStatus.OK:
            json_result = result.json()
            data = AlbumItem.parse_from_json_dict(json_result)
            form = AddAlbumForm(request.form, obj=data)

    except Exception as e:
        app.logger.exception(e)
        flash("Error trying to load album details.", "danger")

    return render_template("albums/add.html", page_name=current_route, form=form, data=data)


@blueprint.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    current_route = "edit_form"
    form = AddAlbumForm(request.form)
    data = None

    if form.validate():
        payload = dict()
        payload["artist"] = request.form["artist_name"]
        payload["name"] = request.form["name"]
        payload["release_date"] = request.form["release_date"]

        data = AlbumItem(id, name=payload["name"], artist_name=payload["artist"], release_date=payload["release_date"])
        try:
            result = requests.post(f"{app.config['BASE_API_ENDPOINT']}/albums/{id}", json=payload)
            if result.status_code == HTTPStatus.OK:
                flash(f"Album updated successfully.", "success")
                data = AlbumItem.parse_from_json_dict(result.json())
                return redirect("/")
            elif result.status_code == HTTPStatus.BAD_REQUEST:
                errors = result.json()
                if "error" in errors and "validation_errors" in errors["error"]:
                    for err in errors["error"]["validation_errors"]:
                        field = API_FORM_MAP[err['field']]
                        msg = err['message']
                        flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg}", "validation_error")

            else:

                app.logger.info(result.json())
                flash(f"Error while trying to talk with API: API returned HTTP {result.status_code}", "danger")
                return redirect("/")

        except Exception as e:
            app.logger.exception(e)
            flash(f"Error while trying to talk with API.", "danger")
    else:
        for field, msg_list in form.errors.items():
            flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg_list[0]}", "validation_error")

    return render_template("albums/add.html", form=form, data=data, page_name=current_route)


@blueprint.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    current_route = "delete_form"

    try:
        result = requests.get(f"{app.config['BASE_API_ENDPOINT']}/albums/{id}")

        if result.status_code == HTTPStatus.OK:
            json_result = result.json()
            data = AlbumItem.parse_from_json_dict(json_result)
            form = AddAlbumForm(request.form, obj=data)

    except Exception as e:
        app.logger.exception(e)
        flash("Error trying to load album details.", "danger")

    return render_template("albums/add.html", page_name=current_route, form=form, data=data, read_only_all=True)


@blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    current_route = "delete_form"

    try:
        result = requests.delete(f"{app.config['BASE_API_ENDPOINT']}/albums/{id}")
        if result.status_code != HTTPStatus.OK:
            flash(f"Error while trying to talk with API: API returned HTTP {result.status_code}", "danger")
        else:
            flash(f"Album deleted successfully.", "success")
            return redirect("/")
    except Exception as e:
        app.logger.exception(e)
        flash(f"Error while trying to talk with API.", "danger")

    return render_template("albums/add.html", page_name=current_route)


@blueprint.errorhandler(CSRFError)
def handle_csrf_error(e):
    current_route = "add_form"
    form = AddAlbumForm(request.form)

    flash("Somenthing went wrong, please try again.", "danger")

    return render_template("albums/add.html", form=form, page_name=current_route)
