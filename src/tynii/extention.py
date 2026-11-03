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

# redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
r = redis.Redis.from_url("redis://default:cy7xe6wGgC09rISM5h7zClOYkH2TQV80@rhubarb-ensuring-drop-24903.db.redis.io:19840", decode_responses=True)
