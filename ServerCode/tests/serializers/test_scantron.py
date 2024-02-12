import json
import uuid

from BubbleScan.serializers.scantron import ScantronJsonEncoder
from BubbleScan.domain.scantron import Scantron

def test_serialize_domain_scantron():
    code = uuid.uuid4()
    
scantron = Scantron(
        code = code,
        first = "John",
        last = "Charlie", 
        idNumber = 34563,
    )
    
expected_json = f"""{{"code": "{code}", "first": "John", "last": "Charlie", "idNumber": 34563 }}
    """
    
json_scantron = json.dumps(scantron, cls = ScantronJsonEncoder)
    
assert json.loads(json_room) == json.loads(expected_json)