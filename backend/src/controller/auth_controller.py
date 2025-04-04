from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from dao.user import UserDao
from model.model import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

user_dao = UserDao()

@auth_bp.route('/api/register', methods=['POST'])
def register():
    # 获取请求数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # 参数校验
    if not username or not password:
        return jsonify({"error": "需要提供用户名和密码"}), 400
    # 查询数据库
    user = user_dao.get_by_username(username)
    # 4. 用户名已存在
    if user:
        return jsonify({"error": "用户名已存在"}), 400
    # 6. 保存到数据库
    user_dao.create_user(username=username, password=generate_password_hash(password))
    # 7. 返回成功响应
    return jsonify({"message": "注册成功"}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    # 获取请求数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 参数校验
    if not username or not password:
        return jsonify({"error": "需要提供用户名和密码"}), 400

    # 查询数据库
    user: User = user_dao.get_by_username(username)

    # 验证用户
    if not user:
        return jsonify({"error": "用户不存在"}), 401

    if check_password_hash(user.password, password):
        return jsonify({"error": "密码错误"}), 401

    # 生成JWT令牌
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200