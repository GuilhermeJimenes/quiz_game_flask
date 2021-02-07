from database import database


class RankModel(database.Model):
    __tablename__ = 'rank'

    id_rank = database.Column(database.Integer, primary_key=True)
    points = database.Column(database.Integer, default=0)
    category_name = database.Column(database.String, database.ForeignKey('category.name'))
    id_user = database.Column(database.Integer, database.ForeignKey('user.id_user'))

    def __init__(self, category_name, id_user):
        self.category_name = category_name
        self.id_user = id_user

    def rank_json(self):
        return {
            'id_rank': self.id_rank,
            'points': self.points,
            'category_name': self.category_name,
            'id_user': self.id_user
        }

    @classmethod
    def find_rank_by_user_and_category(cls, category_name, id_user):
        rank = cls.query.filter_by(category_name=category_name, id_user=id_user).first()
        if rank:
            return rank
        return

    @classmethod
    def find_category_point_by_user(cls, category_name, id_user):
        category_point = cls.query.filter_by(category_name=category_name, id_user=id_user).get('points').first()
        if category_point:
            return category_point
        return

    @classmethod
    def find_global_point_by_user(cls, id_user):
        global_point = sum(cls.query.filter_by(id_user=id_user).all().get('points'))
        if global_point:
            return global_point
        return

    def save_rank(self):
        database.session.add(self)
        database.session.commit()

    def delete_rank(self):
        database.session.delete(self)
        database.session.commit()

    def right(self):
        self.points += 1
        self.save_rank()

    def wrong(self):
        if self.points > 0:
            self.points -= 1
        self.save_rank()
