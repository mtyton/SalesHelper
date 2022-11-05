

class StopPaginationException(Exception):
    ...


class DefaultPaginatedSpiderMixin:
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_page_number = 1

    def _get_next_page_url(self, response):
        ...
