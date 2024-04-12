import pytest

from bubbleScan.domain.scantron import Scantron
from bubbleScan.repository.memrepo import memRepo

@pytest.fixture
def scantron_dicts():
    return [
        {
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "first": "Jimmy",
            "last": "Johnson",
            "idNumber": 45894,
		},
        {
            "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "first": "Sophia",
            "last": "Carter",
            "idNumber": 23423,
		},
        {
            "code": "913694c6-435a-4366-ba0d-da5334a611b2",
            "first": "Henry",
            "last": "Lockwood",
            "idNumber": 12354,
		},
	]

def test_repository_list_without_parameters(scantron_dicts):
	repo = MemRepo(scantron_dicts)
      
	scantrons = [Scantron,from_dict(i) for i in scantron_dicts]
      
	assert repo.list() == scantrons
