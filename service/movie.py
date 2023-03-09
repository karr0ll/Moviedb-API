from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        """
        реализует логику получения записи о жанре
        :param mid: id фильма
        :return: данные о фильме из БД
        """
        return self.dao.get_one(mid)

    def get_all(self):
        """
        реализует логику получения списка со всеми записями о фильмах в БД
        :return: данные о фильмах из БД
        """
        return self.dao.get_all()

    def get_all_paginated(self, page_number):
        """
       реализует логику получения списка со всеми записями о фильмах в БД,
       разделенного на страницы
       :param page_number: номер страницы, получаемый из query string
       :return: данные о фильмах из БД постранично
       """
        page = int(page_number)
        items_per_page = 12
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page
        paginated_items = self.dao.get_all()[pagination_from:pagination_to]
        return paginated_items

    def get_all_new_movies_by_page(self, page_number=None):
        """
        реализует логику получения списка со всеми записями о фильмах в БД,
        отсортированных по id в порядке убывания и разделенного на страницы
        :param page_number: номер страницы, получаемый из query string
        :return: данные о фильмах из БД постранично
        """
        page = int(page_number)
        items_per_page = 12
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page
        paginated_items = self.dao.get_all_by_date_added()[pagination_from:pagination_to]
        return paginated_items


