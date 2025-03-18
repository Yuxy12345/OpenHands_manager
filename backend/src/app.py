from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.models import db, User, Container
from services.docker_service import create_user_container, find_user_container

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config["JWT_VERIFY_SUB"] = False
db.init_app(app)
jwt = JWTManager(app)

@app.route('/api/register', methods=['POST'])
def register():
    # 实现用户注册逻辑
    # ...
    pass

@app.route('/api/login', methods=['POST'])
def login():
    # 获取请求数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 参数校验
    if not username or not password:
        return jsonify({"error": "需要提供用户名和密码"}), 400

    # 查询数据库
    user = User.query.filter_by(username=username).first()

    # 验证用户
    if not user:
        return jsonify({"error": "用户不存在"}), 401

    if user.password != password:
        return jsonify({"error": "密码错误"}), 401

    # 生成JWT令牌（这里使用小写user变量）
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@app.route('/api/container', methods=['GET'])
@jwt_required()
def get_container():
    current_user = get_jwt_identity()
    container = Container.query.filter_by(user_id=current_user).first()
    print(container)

    if not container:
        container = create_user_container(current_user)
        # 保存到数据库
        db.session.add(Container(
            container_id=container['container_id'],
            port=container['port'],
            user_id=current_user
        ))
        db.session.commit()
        return jsonify(container)

    return jsonify({
        "port": container.port
    })