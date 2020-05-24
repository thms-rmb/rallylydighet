from flask import (abort, Blueprint, redirect, render_template, request, Response, url_for)

from rallylydighet.sequences.dblayer import (new_sequence,
                                             get_sequence,
                                             get_sequence_signs)

bp = Blueprint("sequences", __name__, url_prefix="/sequences")

@bp.route("/<int:sequence_id>", methods=("GET",))
def sequence(sequence_id):
    sequence = get_sequence(sequence_id)
    signs = get_sequence_signs(sequence_id)

    if not (sequence and signs):
        return abort(404)

    return render_template("sequences/sequence.html", sequence=sequence, signs=signs)

@bp.route("/<int:sequence_id>/<int:priority>", methods=("GET",))
def sequence_item(sequence_id, priority):
    sequence = get_sequence(sequence_id)
    signs = get_sequence_signs(sequence_id)
    
    if not (sequence and signs):
        return abort(404)

    prev, c, next = None, None, None

    for sign in signs:
        p = sign["priority"]
        if priority - 1 == p:
            prev = sign
        elif priority == p:
            c = sign
        elif priority + 1 == p:
            next = sign

    if c is None:
        return abort(404)

    accept = request.accept_mimetypes.best_match(["text/html",
                                                  "test/plain",
                                                  "image/jpeg",
                                                  "image/png"], "text/html")
    if accept.startswith("text"):
        return render_template("signs/sign.html", sequence=sequence, prev=prev, next=next, sign=c)
    elif accept.startswith("image"):
        return redirect(url_for("signs.sign", sign_id=sign["id"]))
    else:
        return abort(400)
