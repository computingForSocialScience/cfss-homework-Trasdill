from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

db = pymysql.connect(
  db="playlists", host="localhost",
  user="root", passwd="Fanficfan2", charset='utf8')

@app.route('/', methods=['GET','POST'])
def show_albums():
    cur = db.cursor()
    if request.method=="POST":
        title = request.form.get("albumName")
        year = int(request.form.get("albumYear"))
        cur.execute('''
            INSERT INTO albums (title,year)
            VALUES (%s,%s)''', (title,year))
        db.commit()
    sql = '''SELECT title, year
        FROM albums ORDER BY year'''
    cur.execute(sql)
    albumList = cur.fetchall()
    return render_template(
        'show_albums.html',
        albumList=albumList)



if __name__ == '__main__':
    app.debug=True
    app.run()
