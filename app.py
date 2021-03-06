from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import time as tm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=1)
    img = db.Column(db.Text, unique=False, nullable=True)
    title = db.Column(db.Text, nullable=True)

def update_photos(datas):
    db.drop_all()
    db.session.commit()
    db.create_all()
    for data in datas:
        fname = data
        info =  datas[data]
        photo = Img(img=fname, title=info)
        db.session.add(photo)
    db.session.commit()
    print("Database updated on " + str(tm.localtime().tm_mday) + '/' +
        str(tm.localtime().tm_mon) + '/' +
        str(tm.localtime().tm_year) + ' ' +
        str(tm.localtime().tm_hour) + ':' +
        str(tm.localtime().tm_min))

@app.route('/')
def home_page():
    pics = {
        "static\photos\cases.png" : "Total Covid-19 Cases in Europe",
        "static\photos\deaths.png" : "Total Covid-19 Deaths in Europe"
    }
    update_photos(pics)
    images = Img.query.all()
    return render_template('home.html', images=images)

if __name__ == "__main__":
    app.run(debug=True)