from flask import request

#####################################
# Before Requests
#####################################


#####################################
# After Requests
#####################################

def add_content_type_header(response):
    response.headers['Content-Type'] = "application/json;charset=utf-8"

    return response
