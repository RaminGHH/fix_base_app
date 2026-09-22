from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 200

    allowed_page_sizes = (10, 20, 50, 100, 200)

    def get_page_size(self, request):
        raw_size = request.query_params.get(self.page_size_query_param)

        if raw_size is None:
            return self.page_size

        try:
            size = int(raw_size)
        except (TypeError, ValueError):
            raise ValidationError({
                "page_size": "تعداد ردیف باید یک عدد صحیح باشد."
            })

        if size not in self.allowed_page_sizes:
            raise ValidationError({
                "page_size": "یکی از 10، 20، 50، 100 یا 200 را انتخاب کنید."
            })

        return size

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        response.data.update({
            "page": self.page.number,
            "page_size": self.page.paginator.per_page,
            "total_pages": self.page.paginator.num_pages,
            "start_index": self.page.start_index(),
            "end_index": self.page.end_index(),
        })

        return response