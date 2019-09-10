from manage import create, marsh

db = create()
ma = marsh()


class User(db.Model):
    __tablename__ = 'awsfile'
    id = db.Column(db.Integer, primary_key=True)
    TAG_VALUE = db.Column(db.String(25), nullable=False)
    PUBLIC_DNS = db.Column(db.String(50), nullable=False)
    DATE = db.Column(db.String(50), nullable=False)
    SPOTINSTANCE = db.Column(db.String(50), nullable=False)
    INSTANCEID = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"User('{self.TAG_VALUE}', '{self.PUBLIC_DNS}', '{self.DATE}', '{self.SPOTINSTANCE}', '{self.INSTANCEID}')"


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'TAG_VALUE', 'PUBLIC_DNS', 'DATE', 'INSTANCEID')


# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

db.create_all()
