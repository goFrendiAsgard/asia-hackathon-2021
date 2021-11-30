from api.booksRoute import register_books_route
from typing import Mapping, List, Any
from fastapi import FastAPI, HTTPException
from helpers.transport import MessageBus, RPC

import traceback

def register_route_handler(app: FastAPI, mb: MessageBus, rpc: RPC):

    register_books_route(app, mb, rpc)

    print('register api route handler')

