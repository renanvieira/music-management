from flask import request

#####################################
# Before Requests
#####################################


#####################################
# After Requests
#####################################

def add_content_type_header(response):

    if request.accept_mimetypes.accept_html is True:
        response.headers['Content-Type'] = "text/html"
    else:
        response.headers['Content-Type'] = "application/json;charset=utf-8"

    return response
