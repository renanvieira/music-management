from http import HTTPStatus

import marshmallow


class ResponseError(object):

    def __init__(self):
        pass

    @classmethod
    def new_generic_error(cls, msg="An internal error ocurred."):
        return dict(error={"message": msg})


class ValidationError(ResponseError):
    HTTP_STATUS_CODE = HTTPStatus.BAD_REQUEST

    @classmethod
    def new_from_marshmallow_error_dict(cls, error_dict: marshmallow.ValidationError):
        errors = list()

        for key, val in error_dict.messages.items():
            error_item = dict(field=key, message=val[0])
            errors.append(error_item)

        return {"error": dict(validation_errors=errors)}


class ObjectAlreadyRegisteredError(ValidationError):
    MESSAGE = "{} '{}' already registered."

    @classmethod
    def new(cls, resource, field, value):
        error = dict({field: [cls.MESSAGE.format(resource.capitalize(), value)]})

        return cls.new_from_marshmallow_error_dict(marshmallow.ValidationError(error))


class ObjectNotFound(ValidationError):
    MESSAGE = "Resource Not Found."
    MESSAGE_FORMATTED = "{} '{}' Not Found."
    HTTP_STATUS_CODE = HTTPStatus.NOT_FOUND

    @classmethod
    def new(cls):
        return cls.new_generic_error(cls.MESSAGE)

    @classmethod
    def new_detailed(cls, resource_name, field, value):
        error = dict({field: [cls.MESSAGE_FORMATTED.format(resource_name.capitalize(), value)]})
        return cls.new_from_marshmallow_error_dict(marshmallow.ValidationError(error))
