from app import db

class Line(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    flavor = db.Column(db.Text(),index=True)
    start = db.Column(db.Float(),index=True)
    duration = db.Column(db.Float(),index=True)
    videoId = db.Column(db.Text())

    def __repr__(self):
        return '<Line : {}>'.format(self.flavor) 