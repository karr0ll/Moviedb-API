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

    def create(self, data):
        """
        реализует логику внесния в БД данных о новом фильме
        (принимаются строчные значения жанра и режиссера)
        """

        requested_genre = self.genre_dao.get_genre(data.get("genre"))
        requested_director = self.director_dao.get_director(data.get("director"))

        genre_id = [requested_genre.id for requested_genre in requested_genre]
        director_id = [requested_director.id for requested_director in requested_director]

        id_ = data.get("id")
        title = data.get("title")
        description = data.get("description")
        trailer = data.get("trailer")
        year = data.get("year")
        rating = data.get("rating")
        genre_id = genre_id[0]
        director_id = director_id[0]

        return self.dao.create(id_, title, description, trailer, year, rating, genre_id, director_id)


    def update(self, data):
        """
        реализует логику обновления данных об одном фильме по его id
        (принимаются строчные значения жанра и режиссера)
        """
        mid = data.get("id")
        movie = self.get_one(mid)

        requested_genre = self.genre_dao.get_genre(data.get("genre"))
        requested_director = self.director_dao.get_director(data.get("director"))

        genre_id = [requested_genre.id for requested_genre in requested_genre]
        director_id = [requested_director.id for requested_director in requested_director]

        movie.id = mid
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.rating = data.get("rating")
        movie.genre_id = genre_id[0]
        movie.director_id = director_id[0]

        return self.dao.update(movie)

    def delete(self, aid):
        """
        реализует логику удаления данных об одном фильме по его id
        """
        return self.dao.delete(aid)
