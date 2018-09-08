from uuid import uuid4
from datetime import datetime

from .. import db

tag_post_relation = db.Table(
    "relationship_table",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), nullable=False),
    db.Column("tags_id", db.Integer, db.ForeignKey("tags.id"), nullable=False),
    db.PrimaryKeyConstraint("post_id", "tags_id"),
)


class Post(db.Model):
    """
    Represents content-file of a post. Stores content ID,
    title and creation date and enable relating posts via tags.
    Provides methods for easy de-/serialization.
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.now)
    title = db.Column(db.String(128))
    content_id = db.Column(db.String(36), index=True)
    tags = db.relationship("Tag", secondary=tag_post_relation, backref="posts")

    def list_entry(self):
        return {
            "ID": self.id,
            "Title": self.title.title(),
            "Published": datetime.strftime(self.created, "%m/%d/%Y"),
            "ContentID": self.content_id,
            "Tags": [{"Name": tag.name.title(), "TagID": tag.id} for tag in self.tags],
        }

    def create(title, content_id, tags):
        post = Post()
        post.title = title.lower()

        post.content_id = content_id

        for item in tags:
            tag = Tag.check(item["Name"])
            if tag:
                post.tags.append(tag)
            else:
                tag = Tag(name=item["Name"].lower())
                db.session.add(tag)
                post.tags.append(tag)

        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        return post.list_entry()


class Tag(db.Model):
    """
    Allow for tagging posts with a single, descriptive term.
    """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def check(tag_name):
        return Tag.query.filter_by(name=tag_name.lower()).first()
