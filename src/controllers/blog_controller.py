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

@blog_bp.route('/blog/<int:blog_id>', methods=['PUT', 'PATCH'])
@auth_required
def edit_blog(blog_id):
    """
    Edit a blog post. Only the author (owner) can edit their blog.
    Request body JSON: { "content": "updated content" }
    """
    data = request.get_json() or {}
    content = data.get('content')
    if content is None:
        return jsonify({'message': 'Content required'}), 400

    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({'message': 'Blog post not found'}), 404

    # Ensure the current user is the owner
    if blog.user_id != g.user_id:
        return jsonify({'message': 'Forbidden: you can only edit your own posts'}), 403

    blog.content = content
    db.session.commit()

    return jsonify({
        'message': 'Blog post updated',
        'blog': {
            'id': blog.id,
            'author_id': blog.user_id,
            'content': blog.content,
            'created_at': str(blog.created_at)
        }
    }), 200