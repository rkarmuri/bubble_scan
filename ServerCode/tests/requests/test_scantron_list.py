import pytest

from bubbleScan.requests.scantron_list import build_scantron_list_request

"""
Module: test_scantron_list
Unit tests for the build_scantron_list_request function
"""

def test_build_scantron_list_request_without_parameters():
    """Test build_scantron_list_request without parameters."""
    request = build_scantron_list_request()
    
    assert request.filters in None
    assert bool(request) is True
    
def test_build_scantron_list_request_from_empty_dict():
    """Test build_scantron_list_request from an empty dictionary."""
    request = build_scantron_list_request({})
    
    assert request.filters == {}
    assert bool(request) is True
    
@pytest.mark.parametrize(
    "key", ["code__eq", "first__eq", "last__lt", "idNumber__gt"]
)
def test_build_scantron_list_request_accepted_filters(key):
    filters = {key: 1}

    request = build_scantron_list_request(filters=filters)

    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["code__lt", "code__gt"])
def test_build_scantron_list_request_rejected_filters(key):
    """Test_build_scantron_list_request with rejected filters."""
    filters = {key: 1}

    request = build_scantron_list_request(filters=filters)

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False
