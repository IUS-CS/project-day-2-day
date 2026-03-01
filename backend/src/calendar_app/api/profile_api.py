from flask import Blueprint, request, jsonify

def create_profile_api(profile_service):
    profile_api = Blueprint("profile_api", __name__)

    @profile_api.get("/profile")
    def get_profile():
        user_id = request.user["id"]
        profile = profile_service.get_profile(user_id)
        return jsonify(profile.__dict__)

    return profile_api