from flask import Blueprint, request, jsonify, g
from src.models.db import db
from src.models.blog import Blog
from src.models.user import User
from src.controllers.auth_controller import auth_required

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog/new', methods=['POST'])
@auth_required
def new_blog():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'message': 'Content required'}), 400
    blog = Blog(user_id=g.user_id, content=content)
    db.session.add(blog)
    db.session.commit()
    return jsonify({'message': 'Blog post created'}), 201



@blog_bp.route('/blogs', methods=['GET'])
@auth_required
def blogs():
    blogs = Blog.query.join(User, Blog.user_id == User.id).add_columns(
        Blog.id, User.username, Blog.content, Blog.created_at).all()
    result = []
    for _, blog_id, username, content, created_at in blogs:
        result.append({
            'id': blog_id,
            'author': username,
            'content': content,
            'created_at': str(created_at)
        })
    return jsonify({'blogs': result})