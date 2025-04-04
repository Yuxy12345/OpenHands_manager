from flask import Flask
from flask_jwt_extended import JWTManager

from model.model import db, init_db
# 导入蓝图
from controller.auth_controller import auth_bp
from controller.container_controller import container_bp

from flask_apscheduler import APScheduler
from service.docker_service import stop_inactive_containers

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config["JWT_VERIFY_SUB"] = False
db.init_app(app)
jwt = JWTManager(app)
init_db()

app.config.from_object(Config)

scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(container_bp)

# 定时任务：每 10 分钟检查并停止未活动的容器
@scheduler.task('interval', id='stop_inactive_containers', minutes=10)
def scheduled_task():
    stop_inactive_containers("docker.all-hands.dev/all-hands-ai/openhands:latest")

scheduler.start()