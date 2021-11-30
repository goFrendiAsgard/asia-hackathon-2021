from repos.books import BookRepo
from api.booksRpc import register_books_rpc
from typing import Mapping, List, Any
from helpers.transport import RPC

import traceback

def register_rpc_handler(rpc: RPC, book_repo: BookRepo):

    register_books_rpc(rpc, book_repo)

    print('register api RPC handler')
