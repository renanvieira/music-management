from http import HTTPStatus

from flask import Blueprint, render_template, current_app as app, request, flash, redirect, url_for
from flask_wtf.csrf import CSRFError

from web.models import AlbumTable, AddAlbumForm, AlbumItem
from web.resources.error import APIValidationError, APIError
from web.services import MusicManagementAPIClient

blueprint = Blueprint("album", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    current_route = "index"
    current_page = int(request.args.get("page", 1))
    table_data = AlbumTable(list(), 0, 0)

    try:
        result, status_code = MusicManagementAPIClient.list_all(current_page)

        table_data = result
    except APIError as e:
        app.logger.exception(e)
        e.flash_custom_error("Error trying to load album list.")

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
        payload["artist"] = request.form["artist"]
        payload["name"] = request.form["name"]
        payload["release_date"] = request.form["release_date"]

        try:
            result, status_code = MusicManagementAPIClient.add_album(payload)

            if status_code != HTTPStatus.OK:
                flash(f"Error while trying to talk with API: API returned HTTP {status_code}.", "danger")
            else:
                flash(f"Album added successfully.", "success")
                return redirect("/")

        except APIValidationError as err:
            err.flash_messages()
        except APIError as e:
            app.logger.exception(e)
            e.flash_custom_error("Error trying to adding a new album.")


    else:
        for field, msg_list in form.errors.items():
            flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg_list[0]}", "validation_error")

    return render_template("albums/add.html", form=form, page_name=current_route)


@blueprint.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    current_route = "edit_form"
    form = AddAlbumForm(request.form)

    try:
        data, status_code = MusicManagementAPIClient.get_album_by_id(id)

        if status_code == HTTPStatus.OK:
            form = AddAlbumForm(request.form, obj=data)
        elif status_code == HTTPStatus.NOT_FOUND:
            flash(f"Album could be not found.", "danger")
            return redirect(url_for("album.index"))
        else:
            flash(f"Something went wrong while trying to load the requested album.", "danger")
            return redirect(url_for("album.index"))

    except APIError as e:
        app.logger.exception(e)
        e.flash_custom_error("Error trying to load album details.")

    return render_template("albums/add.html", page_name=current_route, form=form)


@blueprint.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    current_route = "edit_form"
    form = AddAlbumForm(request.form)

    if form.validate():
        payload = dict()
        payload["artist"] = request.form["artist"]
        payload["name"] = request.form["name"]
        payload["release_date"] = request.form["release_date"]

        try:
            result, status_code = MusicManagementAPIClient.update_album(id, payload)

            if status_code == HTTPStatus.OK:
                flash(f"Album updated successfully.", "success")
            elif status_code == HTTPStatus.NOT_FOUND:
                flash(f"Album could be not found.", "danger")
            else:
                flash(f"Something went wrong while trying to update the requested album.", "danger")

            return redirect("/")
        except APIValidationError as e:
            app.logger.exception(e)
            e.flash_messages(form)
        except APIError as err:
            app.logger.exception(err)
            err.flash_custom_error("Something went wrong while trying to update the requested album.")

    else:
        for field, msg_list in form.errors.items():
            flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg_list[0]}", "validation_error")

    return render_template("albums/add.html", form=form, page_name=current_route)


@blueprint.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    current_route = "delete_form"
    form = AddAlbumForm(request.form)

    try:
        data, status_code = MusicManagementAPIClient.get_album_by_id(id)

        if status_code == HTTPStatus.NOT_FOUND:
            flash(f"Album not found for deletion.", "danger")
            return redirect(url_for("album.index"))
        elif status_code != HTTPStatus.OK:
            flash(f"Something went wrong while trying to load the requested album.", "danger")
            return redirect(url_for("album.index"))

        form = AddAlbumForm(request.form, obj=data)
    except APIError as e:
        app.logger.exception(e)

        e.flash_custom_error("Error trying to load album details.")

    return render_template("albums/add.html", page_name=current_route, form=form, read_only_all=True)


@blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    try:

        result, status_code = MusicManagementAPIClient.delete_album(id)

        if status_code == HTTPStatus.OK:
            flash("Album deleted successfully", "success")
        elif status_code == HTTPStatus.NOT_FOUND:
            flash("Album not found.", "danger")
        else:
            flash("Something went wrong while trying to delete the requested album.", "danger")

        return redirect("/")
    except APIError as e:
        app.logger.exception(e)
        e.flash_custom_error("Something went wrong while trying to delete the requested album.")

    return redirect(url_for("album.delete", id=id))


@blueprint.errorhandler(CSRFError)
def handle_csrf_error(e):
    current_route = "add_form"
    form = AddAlbumForm(request.form)

    flash("Somenthing went wrong, please try again.", "danger")

    return render_template("albums/add.html", form=form, page_name=current_route)
