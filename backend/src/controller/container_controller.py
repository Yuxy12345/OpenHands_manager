from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.model import User, db, Container
from dao.container import ContainerDao
from service.docker_service import create_user_container, start_container

container_bp = Blueprint('container', __name__)


container_dao = ContainerDao()

@container_bp.route('/api/container', methods=['GET'])
@jwt_required()
def get_container():
    user_id = get_jwt_identity()
    current_user = container_dao.get_by_id(user_id)
    containers = container_dao.get_containers_by_user(current_user)
    print(containers)
    
    # 如果用户没有容器，则创建一个新的容器
    if not containers:
        container = create_user_container(current_user)
        # 保存到数据库
        db.session.add(Container(
            container_id=container['container_id'],
            port=container['port'],
            user_id=user_id,
            status=True
        ))
        db.session.commit()
        return jsonify(container)
    # 如果用户已经有容器，则获取第一个容器
    container = containers[0]
    if not container.status:
        # 如果容器未启动，则启动容器
        start_container(container.container_id)
        container.status = True
        db.session.commit()

    return jsonify({
        "port": container.port
    })
