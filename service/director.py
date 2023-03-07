from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did):
        """
        реализует логику получения записи о жанре
        :param gid: id режиссера
        :return genre data: данные о режиссере из БД
        """
        return self.dao.get_one(did)

    def get_all(self):
        """
        реализует логику получения списка со всеми записями о жанре в БД
        :return genre data: данные о жанрах из БД
        """
        return self.dao.get_all()

    def get_all_paginated(self, page_number):
        """
        реализует логику получения списка со всеми записями о режиссерах в БД,
        разделенного на страницы
        :param page_number: номер страницы, получаемый из query string
        :return: данные о режиссерах из БД постранично
        """
        page = int(page_number)
        items_per_page = 12
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page
        paginated_items = self.dao.get_all()[pagination_from:pagination_to]
        return paginated_items