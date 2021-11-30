from typing import Any, List, Mapping
from helpers.transport import RPC
from schemas.books import Book, BookData
from repos.books import BookRepo

def register_books_rpc(rpc: RPC, book_repo: BookRepo):

    @rpc.handle('find_books')
    def find_books(keyword: str, limit: int, offset: int) -> List[Mapping[str, Any]]:
        results = book_repo.find(keyword, limit, offset)
        return [result.dict() for result in results]


    @rpc.handle('find_books_by_id')
    def find_books_by_id(id: str) -> Mapping[str, Any]:
        result = book_repo.find_by_id(id)
        return None if result is None else result.dict()


    @rpc.handle('insert_books')
    def insert_books(data: Mapping[str, Any]) -> Mapping[str, Any]:
        result = book_repo.insert(BookData.parse_obj(data))
        return None if result is None else result.dict()


    @rpc.handle('update_books')
    def update_books(id: str, data: Mapping[str, Any]) -> Mapping[str, Any]:
        result = book_repo.update(id, BookData.parse_obj(data))
        return None if result is None else result.dict()


    @rpc.handle('delete_books')
    def delete_books(id: str) -> Mapping[str, Any]:
        result = book_repo.delete(id)
        return None if result is None else result.dict()
    

    print('Handle RPC for api.Books')

