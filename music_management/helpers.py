class PaginatorHelper:

    @staticmethod
    def get_paginator_dict(paginator):
        paginator_schema = dict()
        paginator_schema["total"] = paginator.total
        paginator_schema["total_pages"] = paginator.pages
        paginator_schema["has_more"] = paginator.has_next
        paginator_schema["items"] = paginator.items

        return paginator_schema
