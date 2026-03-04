import jwt
import datetime

SECRET = "dev-secret"  # must match your auth.py

payload = {
    "id": "test-admin-id",
    "email": "admin@example.com",
    "role": "admin",
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)