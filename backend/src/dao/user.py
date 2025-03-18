from models import User, db

class UserDao:
    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_all_users(self):
        return User.query.all()
    
    def create_user(self, username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def update_user(self, user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user
    
    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()
