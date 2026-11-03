import uuid

from flask import Flask, jsonify, make_response, render_template, request

from endpoints import api_bp

from .extention import cors

app = Flask(__name__)
app.config.from_pyfile("config.py")

cors.init_app(app)

app.register_blueprint(api_bp)


@app.get("/")
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

    return res


@app.get("/<url>")
def goto_url(url: str):
    return jsonify({"url": url})