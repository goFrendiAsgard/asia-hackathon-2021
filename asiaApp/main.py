from repos.dbBooks import DBBookRepo
from repos.redisBooks import RedisBookRepo
# -- api
from api.route import register_route_handler as register_api_route_handler
from api.event import register_event_handler as register_api_event_handler
from api.rpc import register_rpc_handler as register_api_rpc_handler
# -- common
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from helpers.transport import RMQEventMap, KafkaEventMap
from configs.helper import get_abs_static_dir, get_rmq_connection_parameters, get_kafka_connection_parameters, create_message_bus, create_rpc

import os
import redis as _redis

db_url = os.getenv('APP_SQLALCHEMY_DATABASE_URL', 'sqlite://')
redis_url = os.getenv('APP_REDIS_URL', 'redis://localhost:6379')
rmq_connection_parameters = get_rmq_connection_parameters()
rmq_event_map = RMQEventMap({})
kafka_connection_parameters = get_kafka_connection_parameters()
kafka_event_map = KafkaEventMap({})

mb_type = os.getenv('APP_MESSAGE_BUS_TYPE', 'local')
rpc_type = os.getenv('APP_RPC_TYPE', 'local')
book_storage_engine = os.getenv('APP_BOOK_STORAGE_ENGINE', 'db')

enable_route_handler = os.getenv('APP_ENABLE_ROUTE_HANDLER', '1') != '0'
enable_event_handler = os.getenv('APP_ENABLE_EVENT_HANDLER', '1') != '0'
enable_rpc_handler = os.getenv('APP_ENABLE_RPC_HANDLER', '1') != '0'
static_url = os.getenv('APP_STATIC_URL', '/static')
static_dir = get_abs_static_dir(os.getenv('APP_STATIC_DIR', ''))

if book_storage_engine == 'redis':
    redis = _redis.from_url(redis_url)
    book_repo = RedisBookRepo(redis)
else:
    engine = create_engine(db_url, echo=True)
    book_repo = DBBookRepo(engine=engine, create_all=True)

app = FastAPI(title='asiaApp')
mb = create_message_bus(mb_type, rmq_connection_parameters, rmq_event_map, kafka_connection_parameters, kafka_event_map)
rpc = create_rpc(rpc_type, rmq_connection_parameters, rmq_event_map)

@app.on_event('shutdown')
def on_shutdown():
    mb.shutdown()
    rpc.shutdown()
 
if static_dir != '':
    app.mount(static_url, StaticFiles(directory=static_dir), name='static')

# -- api

if enable_route_handler:
    register_api_route_handler(app, mb, rpc)

if enable_event_handler:
    register_api_event_handler(mb)

if enable_rpc_handler:
    register_api_rpc_handler(rpc, book_repo)