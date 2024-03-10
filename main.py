from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(30))
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'<posts {self.id}>'
    
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/create_post", methods=("POST", "GET"))
def create_post():
    if request.method == "POST":
        
        try:
            p = Posts(heading=request.form['heading'], description = request.form['description'])
            db.session.add(p)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка!")
    return render_template('create_post.html')

@app.route("/posts")
def posts():
    posts_list = []
    try:
        posts_list = Posts.query.all()
        print(posts_list)
    except:
        print("Ошибка чтения!")

    return render_template('posts.html', list=posts_list)

if __name__ == '__main__':
    app.run(debug=True)