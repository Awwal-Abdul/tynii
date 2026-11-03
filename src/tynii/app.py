import uuid

from flask import Flask, jsonify, make_response, render_template, request

# from .extention import cors

app = Flask(__name__)
app.config.from_pyfile("config.py")

# cors.init_app(app)


@app.route("/")
def home():
    res = make_response(render_template("index.html"))
    client_id = request.cookies.get("client_id")
    is_new_user = False

    if not client_id:
        client_id = str(uuid.uuid4())
        is_new_user = True

    if is_new_user:
        res.set_cookie(
            "client_id", client_id, httponly=True, secure=True, samesite="Lax"
        )

    print(f"Client-id: {client_id}")
    return res


@app.post("/api/shorten")
def shorten():
    return jsonify({"message": "Successful"})





def main() -> None:
    return app.run(port=8000)