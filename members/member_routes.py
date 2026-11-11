from flask import Blueprint, jsonify, request

from . import member_service


bp = Blueprint("members", __name__)


def member_json(member):
    return {
        "id": member["id"],
        "name": member["name"],
        "email": member["email"],
        "type": member["type"],
    }


@bp.route("/members", methods=["GET"])
def list_members():
    return jsonify([member_json(member) for member in member_service.list_members()])


@bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    return jsonify(member_json(member_service.get_member(member_id)))


@bp.route("/members", methods=["POST"])
def create_member():
    data = request.get_json(silent=True) or {}
    return jsonify(member_json(member_service.create_member(data))), 201


@bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    return jsonify(member_service.member_account(member_id))
