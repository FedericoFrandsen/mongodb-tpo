from bson import ObjectId

def custom_jsonable_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [custom_jsonable_encoder(x) for x in obj]
    if isinstance(obj, dict):
        return {k: custom_jsonable_encoder(v) for k, v in obj.items()}
    return obj