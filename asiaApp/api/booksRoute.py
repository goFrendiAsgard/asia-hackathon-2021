from typing import Any, List, Mapping
from helpers.transport import MessageBus, RPC
from fastapi import FastAPI, HTTPException
from schemas.books import Book, BookData

import traceback

def register_books_route(app: FastAPI, mb: MessageBus, rpc: RPC):

    @app.get('/books/', response_model=List[Book])
    def find_books(keyword: str='', limit: int=100, offset: int=0) -> List[Book]:
        results = []
        try:
            results = rpc.call('find_books', keyword, limit, offset)
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return [Book.parse_obj(result) for result in results]


    @app.get('/books/{id}', response_model=Book)
    def find_books_by_id(id: str) -> Book:
        result = None
        try:
            result = rpc.call('find_books_by_id', id)
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        if result is None:
            raise HTTPException(status_code=404, detail='Not Found')
        return Book.parse_obj(result)


    @app.post('/books/', response_model=Book)
    def insert_books(data: BookData) -> Book:
        result = None
        try:
            result = rpc.call('insert_books', data.dict())
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        if result is None:
            raise HTTPException(status_code=404, detail='Not Found')
        return Book.parse_obj(result)


    @app.put('/books/{id}', response_model=Book)
    def update_books(id: str, data: BookData) -> Book:
        result = None
        try:
            result = rpc.call('update_books', id, data.dict())
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        if result is None:
            raise HTTPException(status_code=404, detail='Not Found')
        return Book.parse_obj(result)


    @app.delete('/books/{id}')
    def delete_books(id: str) -> Book:
        result = None
        try:
            result = rpc.call('delete_books', id)
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        if result is None:
            raise HTTPException(status_code=404, detail='Not Found')
        return Book.parse_obj(result)


    print('Handle HTTP routes for api.Books')
