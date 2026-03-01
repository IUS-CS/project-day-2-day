from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET = os.getenv("JWT_SECRET", "dev-secret")

def require_auth(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Missing token"}), 401

            try:
                payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            except Exception:
                return jsonify({"error": "Invalid token"}), 401

            if role and payload.get("role") != role:
                return jsonify({"error": "Forbidden"}), 403

            request.user = payload
            return fn(*args, **kwargs)
        return wrapper
    return decorator