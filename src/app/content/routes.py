from flask import jsonify, request, current_app, url_for, redirect

from . import bp
from ..store.models import Post, Tag
from ..store.files import content_file
from ..store.schema import PostSchema


post_schema = PostSchema()


@bp.route("/post/<int:id_>", methods=["GET"])
def get_post(id_):
    """
    Fetch a single entry from the post table.
    """
    raw = Post.query.get_or_404(id_)
    return jsonify(raw.list_entry()), 200


@bp.route("/post/list", methods=["GET"])
def get_posts():
    """
    Fetch a list of entries from the post table.
    """
    # TODO: Implement paging.
    raw = Post.query.all()
    data = dict(Posts=[x.list_entry() for x in raw])
    return jsonify(data), 200


@bp.route("/post/content/<uuid:id_>", methods=["GET"])
def get_post_content(id_):
    """
    Request the uri for the html-rendered content of a post.
    """
    result = Post.query.filter_by(content_id=str(id_)).first_or_404()
    content_uri = url_for("static", filename=result.content_id)
    return redirect(content_uri)


@bp.route("/post/new", methods=["POST"])
def post_content():
    """
    Post new content to the server. Creates a
    new entry in the database and saves the post content
    to disk after converting it to html.
    """
    # TODO:
    # This endpoint should only be accessible to a specific
    # client authenticated to a jwt-session.
    raw = request.get_json(force=True)
    data = post_schema.dump(raw)[0]
    content_id = content_file(data["PostContent"], current_app.config["CONTENTPATH"])
    result = Post.create(data["Title"], content_id, data["Tags"])
    return jsonify(result), 201
