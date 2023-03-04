from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_all_paginated(self, page_number):
        page = int(page_number)
        items_per_page = 12
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page
        paginated_items = self.dao.get_all()[pagination_from:pagination_to]
        return paginated_items

    def get_all_new_movies_by_page(self, page_number=None):
        page = int(page_number)
        items_per_page = 12
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page
        paginated_items = self.dao.get_all_by_date_added()[pagination_from:pagination_to]
        return paginated_items

    def get_one(self, mid):
        """
        реализует логику получения данных об одном фильме по его id
        """
        return self.dao.get_one(mid)
