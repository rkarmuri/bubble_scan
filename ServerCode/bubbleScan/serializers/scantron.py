import json

class ScantronJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": str(o.code),
                "first": o.first,
                "last": o.last,
                "idNumber": o.idNumber,
			}
            return to_serialize
        except AttributeError: 
            return super().default(o)