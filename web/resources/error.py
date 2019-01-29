from flask import flash
from flask_wtf import Form


class APIError(Exception):

    def __init__(self, inner_error=None):
        self.inner_error = inner_error

    def flash_custom_error(self, msg):
        flash(f"{msg}", "danger")


class APIValidationError(Exception):
    def __init__(self, errors={}):
        self.errors = errors

    def flash_messages(self, form: Form):
        for field, msg in self.errors.items():
            flash(f"<strong>{getattr(form, field).label.text}&nbsp;</strong>{msg}", "validation_error")
