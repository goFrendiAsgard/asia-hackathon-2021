from typing import TypedDict


from typing import Any, Callable, Mapping, TypedDict
from helpers.transport.serial import create_json_byte_encoder, create_json_byte_decoder

class KafkaEventConfig(TypedDict):
    topic: str
    group_id: str
    encoder: Callable[[Any], bytes]
    decoder: Callable[[bytes], Any]


class KafkaEventMap:

    def __init__(self, mapping: Mapping[str, KafkaEventConfig]):
        self.mapping = mapping
        self.default_encoder = create_json_byte_encoder()
        self.default_decoder = create_json_byte_decoder()

    def get_topic(self, event_name: str) -> str:
        if event_name in self.mapping and 'topic' in self.mapping[event_name] and self.mapping[event_name]['topic'] != '':
            return self.mapping[event_name]['topic']
        return event_name

    def get_group_id(self, event_name: str) -> str:
        if event_name in self.mapping and 'group_id' in self.mapping[event_name] and self.mapping[event_name]['group_id'] != '':
            return self.mapping[event_name]['group_id']
        return 'default'

    def get_encoder(self, event_name: str) -> Callable:
        if event_name in self.mapping and 'encoder' in self.mapping[event_name]:
            return self.mapping[event_name]['encoder']
        return self.default_encoder

    def get_decoder(self, event_name: str) -> Callable:
        if event_name in self.mapping and 'decoder' in self.mapping[event_name]:
            return self.mapping[event_name]['decoder']
        return self.default_decoder
