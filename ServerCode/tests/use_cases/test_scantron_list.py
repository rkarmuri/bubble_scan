import pytest
import uuid
from unittest import mock

from bubbleScan.domain.scantron import Scantron
from bubbleScan.use_cases.scantron_list import scantron_list_use_case
from bubbleScan.requests.room_list import build_room_list_request, build_scantron_list_request
from bubbleScan.responses import ResponseTypes

"""
Module: test_scantron_list_use_case
Unit tests for the scantron_list_use_case function.
"""

@pytest.fixture
def domain_scantrons():
    scantron_1 = Scantron(
        code = uuid.uuid4(),
        first = "Hannah",
        last = "Stevenson",
        idNumber = 45435,
	)
    
    scantron_2 = Scantron(
        code = uuid.uuid4(),
        first = "Tracy",
        last = "Richards",
        idNumber = 56346,
	)
    
    scantron_3 = Scantron(
        code = uuid.uuid4(),
        first = "Kevin",
        last = "Peters",
        idNumber = 89343,
	)
    
    return [scantron_1, scantron_2, scantron_3]

def test_scantron_list_without_parameters(domain_scantrons):
    """Test scantron_list_use_case without parameters."""
    repo = mock.Mock()
    repo.list.return_value = domain_scantrons
    
    request = build_room_list_request()

    response = scantron_list_use_case(repo, request)

    assert bool(response) is True
    repo.list.assert_called_with(filters = None)
    assert response.value == domain_scantrons

def test_scantron_list_with_filters(domain_scantrons):
    """Test scantron_list_use_case with filters."""
    repo = mock.Mock()
    repo.list.return_value = domain_scantrons

    qry_filters = {"code__eq": 5}
    request = build_scantron_list_request(filters=qry_filters)

    response = scantron_list_use_case(repo, request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response.value == domain_scantrons


def test_scantron_list_handles_generic_error():
    """Test scantron_list_use_case handling generic error."""
    repo = mock.Mock()
    repo.list.side_effect = Exception("Just an error message")

    request = build_scantron_list_request(filters={})

    response = scantron_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message",
    }


def test_scantron_list_handles_bad_request():
    """Test scantron_list_use_case handling bad request."""
    repo = mock.Mock()

    request = build_scantron_list_request(filters=5)

    response = scantron_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
