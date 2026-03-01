from flask import Blueprint, request, jsonify

def create_admin_api(admin_service):
    admin_api = Blueprint("admin_api", __name__)

    @admin_api.get("/admin/users")
    def list_users():
        users = admin_service.get_all_users()
        return jsonify([u.to_dict() for u in users])

    @admin_api.put("/admin/users/<user_id>/role")
    def update_role(user_id):
        data = request.json
        new_role = data.get("role")
        updated = admin_service.update_role(user_id, new_role)
        if updated is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(updated.to_dict())

    return admin_api