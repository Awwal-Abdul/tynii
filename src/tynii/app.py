import uuid

from flask import Flask, jsonify, make_response, redirect, render_template, request

from .extention import cors, r

app = Flask(__name__)
app.config.from_pyfile("config.py")


cors.init_app(app)


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

    return res


@app.post("/api/register")
def shorten():
    data = request.json

    short_code = data.get("short_code")
    original_url = data.get("original_url")

    if not short_code or not original_url:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        r.set(short_code, original_url)
        return jsonify(
            {"status": "success", "message": "Link registered for routing"}
        ), 201
    except Exception as err:
        return jsonify({"Error": f"Someting went wrong ({err})"}), 500


@app.get("/<code>")
def goto_url(code):
    original_url = r.get(code)

    if not original_url:
        return jsonify({"error": "Link not found"}), 404

    return redirect(str(original_url), code=302)


def main() -> None:
    return app.run(port=8000)
