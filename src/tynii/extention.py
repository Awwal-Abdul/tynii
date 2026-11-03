import os

import redis
from dotenv import load_dotenv

# from flask_cors import CORS

load_dotenv()


# cors = CORS(
#     resources={
#         r"/api/*": {
#             "origins": os.environ.get("ALLOWED_ORIGINS"),
#             "supports_credentials": True,  # REQUIRED: Allows cookies (client_id) to be sent cross-origin
#             "methods": ["GET", "POST", "PUT", "DELETE"],
#             "allow_headers": ["Content-Type", "Authorization"],
#         }
#     }
# )

redis_url: str = os.environ.get("REDIS_URL")
r = redis.Redis.from_url(redis_url, decode_responses=True)
