from database import database


class UserModel(database.Model):
    __tablename__ = 'user'

    id_user = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String, unique=True)
    password = database.Column(database.String)
    # activated = database.Column(database.Boolean, default=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password
        # self.activated = activated

    def user_json(self):
        return {
            'id_user': self.id_user,
            'login': self.login,
            # 'activated': self.activated
        }

    @classmethod
    def find_user(cls, id_user):
        user = cls.query.filter_by(id_user=id_user).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, login, password):
        self.login = login
        self.password = password
        self.save_user()

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
