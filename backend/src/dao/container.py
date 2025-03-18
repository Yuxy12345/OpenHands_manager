from models import Container, User, db

class ContainerDao:
    def get_by_id(self, container_id):
        return Container.query.get(container_id)
    
    def get_all_containers(self):
        return Container.query.all()
    
    def get_containers_by_user(self, user):
        return Container.query.filter(Container.user == user).all()
    
    def create_container(self, user, container_id, port):
        new_container = Container(user=user, container_id=container_id, port=port)
        db.session.add(new_container)
        db.session.commit()
        return new_container
    
    def update_container(self, container, **kwargs):
        for key, value in kwargs.items():
            setattr(container, key, value)
        db.session.commit()
        return container
    
    def delete_container(self, container):
        db.session.delete(container)
        db.session.commit()
