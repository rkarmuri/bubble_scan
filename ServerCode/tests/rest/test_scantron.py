import json
from unittest import mock

import pytest

from bubbleScan.domain.scantron import Scantron
from bubbleScan.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)


scantron_dict = {
    
	"code": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "first": "John",
    "last": "Charlie",
    "idNumber": 35443
}

scantrons = [Scantron.from_dict(scantron_dict)]

@mock.patch("application.rest.scantron.scantron_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(scantrons)
    
    http_response = client.get("/scantrons")
    
    assert json.loads(http_response.data.decode("UTF-8")) == [scantron_dict]
    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}
    
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"