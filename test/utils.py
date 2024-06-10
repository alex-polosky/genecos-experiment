import uuid
from geneco.models import *
from geneco.models._base import BaseModel

_ID_MAP: dict[int, int] = {}

def gen_id(instance: BaseModel) -> BaseModel:
    match instance:
        case Agency():
            type_id = 1
        case Client():
            type_id = 2
        case Contract():
            type_id = 3
        case Consumer():
            type_id = 4
        case AddressLead():
            type_id = 5
        case Account():
            type_id = 6
        case AccountConsumer():
            type_id = 7
        case _:
            type_id = 0
    if type_id not in _ID_MAP:
        _ID_MAP[type_id] = 100
    _ID_MAP[type_id] += 1
    id_ = _ID_MAP[type_id]

    instance.uuid = uuid.UUID(f'{{00000000-0000-0000-{str(type_id).rjust(4, "0")}-{str(id_).rjust(12, "0")}}}')

    return instance

def gen_id_save(instance: BaseModel) -> BaseModel:
    gen_id(instance)
    instance.save()
    return instance

def normalize_for_compare(obj: object) -> dict:
    normed = {}
    for k, v in vars(obj).items():
        match k:
            case '_state':
                cache = vars(v).get('fields_cache')
                if not cache:
                    continue
                for rel, rel_obj in cache.items():
                    normed[rel] = normalize_for_compare(rel_obj)
            case 'id' | 'uuid' | 'created' | 'updated' | 'reported':
                continue
            case s if s.endswith('_id'):
                continue
            case _:
                normed[k] = v
    return normed
