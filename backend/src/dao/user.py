from models.models import db, User, Container


class UserService:
    @staticmethod
    def create_user(data):
        try:
            if not data.get('username'):
                return {"message": "Username is required"}, 400
            if User.query.filter_by(username=data['username']).first():
                return {"message": "Username already exists"}, 400

            user = User(
                username=data['username'],
                password=data['password']
            )
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully", "user": user.__dict__}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

    @staticmethod
    def get_user(id):
        try:
            user = User.query.get(id)
            if not user:
                return {"message": "User not found"}, 404
            return {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "containers_count": len(user.containers)
                }
            }, 200
        except Exception as e:
            return {"message": str(e)}, 500

    @staticmethod
    def update_user(id, data):
        try:
            user = User.query.get(id)
            if not user:
                return {"message": "User not found"}, 404

            if 'username' in data and data['username']:
                if User.query.filter_by(username=data['username']).first():
                    return {"message": "Username already exists"}, 400
                user.username = data['username']

            if 'password' in data:
                user.password = data['password']

            db.session.commit()
            return {"message": "User updated successfully", "user": user.__dict__}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

    @staticmethod
    def delete_user(id):
        try:
            user = User.query.get(id)
            if not user:
                return {"message": "User not found"}, 404

            # 删除用户及其所有容器
            Container.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500

    @staticmethod
    def get_all_users():
        try:
            users = User.query.all()
            return {
                "users": [user.__dict__ for user in users]
            }, 200
        except Exception as e:
            return {"message": str(e)}, 500
