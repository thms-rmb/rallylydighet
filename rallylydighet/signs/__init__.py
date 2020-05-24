from flask import (abort, Blueprint, render_template, request, Response)

from rallylydighet.signs.dblayer import get_sign

bp = Blueprint("signs", __name__, url_prefix="/signs")

@bp.route("/<int:sign_id>", methods=("GET",))
def sign(sign_id):
    s = get_sign(sign_id)
    if s is None:
        return abort(404)

    accept = request.accept_mimetypes.best_match(["text/html",
                                                  "test/plain",
                                                  "image/jpeg",
                                                  "image/png"], "text/html")

    if accept.startswith("text"):
        return render_template("signs/sign.html", sign=s)
    elif accept.startswith("image"):
        response = Response(s["content"], mimetype=s["mime"])
        response.headers["Content-Length"] = s["size"]
        return response
    else:
        return abort(400)
