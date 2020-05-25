from flask import Blueprint, request
from flask_cors import CORS
from .utils.discord import try_discord_send
from .utils.functions import now
from app.db import rdb, bdb, wdb


api_bp = Blueprint('api_bp', __name__)
"""
TODO:
Due to nature of Chrome extensions, we have to accept
all origins. However it would be unsafe to accept all,
so we need to add a token/key check.
- Trinity
"""
cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})


@api_bp.route("/api/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()['data']
    org_id = request.get_json()['org_id']
    data['timestamp'] = now()
    rdb[org_id].insert(data)
    return data, 200


@api_bp.route("/api/feedback", methods=['POST', 'PUT']) # keep as is
def handle_feedback():
    data = request.get_json()['data']
    data['timestamp'] = now()
    # fdb = db.get_table('feedback')
    # fdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/bug", methods=['POST', 'PUT']) # keep as is
def handle_bug():
    data = request.get_json()['data']
    data['timestamp'] = now()
    # bdb = db.get_table('bugs')
    # bdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/delete", methods=['POST', 'PUT'])
def delete_item():
    json = request.get_json()
    rdb[json.get('org_id')].delete(id=json.get('id'))
    return json, 200


@api_bp.route("/api/blacklist", methods=['GET'])
def get_blacklist():
    json = request.get_json()
    b1 = [item['address'] for item in bdb[json.get('org_id')].all()]
    return {
        'data': b1,
    }


@api_bp.route("/api/blacklist", methods=['POST', 'PUT'])
def blacklist_address():
    json = request.get_json()
    bdb[json.get('org_id')].upsert(json, ['address'])
    return json, 200


@api_bp.route("/api/whitelist", methods=['POST', 'PUT'])
def whitelist_address():
    json = request.get_json()
    wdb[json.get('org_id')].insert(json)
    return json, 200
