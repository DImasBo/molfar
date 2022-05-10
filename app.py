from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from application.crud import MagicUlrCRUD
from application.make_short_url import generate_random_string

DOMAIN_URL = 'http://localhost:5000'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_local.sqlite3'
db = SQLAlchemy(app)


class MagicURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String, nullable=False)
    id_path = db.Column(db.String)
    count_open = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<MagicURL {self.id}-{self.id_path}: origin={self.origin_url}>'


db.create_all()
magic_crud = MagicUlrCRUD(MagicURL)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        origin_url = request.form.get('origin_url')
        magic_url = magic_crud.get_by_origin_url(db.session, origin_url)

        if not magic_url:
            id_path = generate_random_string()

            magic_url = magic_crud.create(db.session, origin_url=origin_url, id_path=id_path)
        short_url = f'{DOMAIN_URL}/{magic_url.id_path}'
        return render_template('index.html', short_url=short_url, magic_url=magic_url)

    return render_template('index.html')


@app.route('/<id_path>')
def magic(id_path):
    magic_url = magic_crud.get_by_id_path(db.session, id_path)
    if not magic_url:
        return redirect(url_for('index'))

    magic_url = magic_crud.count_plus(db.session, magic_url)
    return redirect(magic_url.origin_url)


if __name__ == '__main__':
    app.run()
