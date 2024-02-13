import json

from flask import Blueprint, request, Response

from bubbleScan.repository.memrepo import MemRepo
from bubbleScan.use_cases.scantron_list import scantron_list_use_case
from bubbleScan.serializers.scantron import ScantronJsonEncoder
from bubbleScan.requests.scantron_list import build_scantron_list_request
from bubbleScan.responses import ResponseTypes

blueprint = Blueprint("scantron", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

scantrons = [
    {
        "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "first": "Larry",
        "last": "Johnson",
        "idNumber": 45874,
	},
    {
        "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "first": "Sarah",
        "last": "Alice",
        "idNumber": 78498,
	},
    {
        "code": "913694c6-435a-4366-ba0d-da5334a611b2",
        "first": "Robert",
        "last": "Randy",
        "idNumber": 97564,
	},   
]

@blueprint.route("/scantrons", methods=["GET"])
def scantron_list():
    qrystr_params = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_scantron_list_request(
        filters=qrystr_params["filters"]
    )

    repo = MemRepo(rooms)
    response = scantron_list_use_case(repo, request_object)

    return Response(
        json.dumps(response.value, cls=ScantronJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )