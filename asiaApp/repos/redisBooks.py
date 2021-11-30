from typing import List
from schemas.books import Book, BookData
from repos.books import BookRepo
import redis as _redis
import json as _json
import uuid as _uuid
import datetime as _datetime

class RedisBookRepo(BookRepo):

    def __init__(self, redis: _redis.Redis):
        self.redis = redis

    def _get_key(self, id: str) -> str:
        return 'book:' + id

    def _json_to_book(self, json: str) -> Book:
        book_data = _json.loads(json)
        book = Book(id=book_data['id'], title=book_data['title'], author=book_data['author'], synopsis=book_data['synopsis'])
        return book

    def _book_to_json(self, book: Book) -> str:
        book_dict = book.dict()
        book_dict['created_at'] = str(book_dict['created_at'])
        book_dict['updated_at'] = str(book_dict['updated_at'])
        return _json.dumps(book_dict)

    def find_by_id(self, id: str) -> Book:
        key = self._get_key(id)
        json = self.redis.get(key)
        return self._json_to_book(json)

    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        keys = self.redis.keys('book:*')
        books: List[Book] = []
        for key in keys:
            book = self.find_by_id(key)
            books.append(book)
        return books

    def insert(self, book_data: BookData) -> Book:
        id = str(_uuid.uuid4())
        key = self._get_key(id)
        book = Book(id=id, title=book_data.title, author=book_data.author, synopsis=book_data.synopsis, created_at=_datetime.datetime.utcnow(), updated_at=_datetime.datetime.utcnow())
        json = self._book_to_json(book)
        self.redis.set(key, json)
        return book

    def update(self, id: str, book_data: BookData) -> Book:
        book = self.find_by_id(id)
        book.title = book_data.title
        book.author = book_data.author
        book.synopsis = book_data.synopsis
        book.updated_at = _datetime.datetime.utcnow()
        json = self._book_to_json(book)
        key = self._get_key(id)
        self.redis.set(key, json)
        return book

    def delete(self, id: str) -> Book:
        book = self.find_by_id(id)
        key = self._get_key(id)
        self.redis.delete(key)
        return book
