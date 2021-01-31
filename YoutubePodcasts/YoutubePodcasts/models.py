from YoutubePodcasts import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'{self.username}'

    def create(self):
        db.session.add(self)
        db.session.commit()

class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(80), unique=False, nullable=False)
    yt_link      = db.Column(db.String(256), unique=False, nullable=False)
    title        = db.Column(db.String(128), unique=False, nullable=False)
    uploader     = db.Column(db.String(80), unique=False, nullable=False)
    uploader_url = db.Column(db.String(256), unique=False, nullable=False)
    thumbnail    = db.Column(db.String(256), unique=False, nullable=False)

    def __init__(self, username, yt_link, title, uploader, uploader_url, thumbnail):
        self.username = username
        self.yt_link = yt_link
        self.title = title
        self.uploader = uploader
        self.uploader_url = uploader_url
        self.thumbnail = thumbnail

    def __repr__(self):
        return f'{self.yt_link}'

    def create(self):
        db.session.add(self)
        db.session.commit()
