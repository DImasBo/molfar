from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from application.make_short_url import generate_random_string

DOMAIN_URL = 'http://localhost:5000'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_local.sqlite3'
db = SQLAlchemy(app)


class MagicURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin_url = db.Column(db.String, nullable=False)
    short_path = db.Column(db.String)

    def __repr__(self):
        return f'<MagicURL {self.id}-{self.short_path}: origin=self.origin_url>'


db.create_all()


@app.route('/')
def index():
    short_url = None

    if request.args.get('url'):
        short_path = generate_random_string()

        magic_url = MagicURL(origin_url=request.args.get('url'), short_path=short_path)
        db.session.add(magic_url)
        db.session.commit()

        short_url = f'{DOMAIN_URL}/{short_path}'

    return render_template('index.html', short_url=short_url)


@app.route('/<short_path>')
def magic(short_path):
    result = db.session.query(MagicURL.origin_url).filter(
        MagicURL.short_path == short_path).first()

    if not result:
        flash('не вигадуй нема такого запита. Начаклуй новує!')
        return redirect(url_for('index'))

    magic_url = result[0]
    return redirect(magic_url)


if __name__ == '__main__':
    app.run()
