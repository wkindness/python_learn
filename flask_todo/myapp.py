"""
flask todo app
host 127.0.0.1:5000
"""
import json
import sqlite3
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from flask import Flask
from flask import g
from flask import render_template
from flask import redirect
from flask import Response
from flask import request


app = Flask(__name__)

# engine = sqlalchemy.create_engine('sqlite3:///test_sqlite.db', echo=True)
# Base = sqlalchemy.ext.declarative.declarative_base()
# class TodoWord(Base):
#     __tablename___ = 'todowords'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('test_sqlite.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# デコレーター
def print_more(func):
    def wrapper(*args, **kwargs):
        print('func:', func.__name__)
        print('args:', args)
        print('kwargs:', kwargs)
        result = func(*args, **kwargs)
        # print('result:', result)
        return result
    return wrapper

# デコレーター
def print_info(func):
    def wrapper(*args, **kwargs):
        print('------- start -------')
        result = func(*args, **kwargs)
        print('-------  end  -------')
        return result
    return wrapper

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@print_info
@print_more
def top():
    db = get_db()
    curs = db.cursor()
    curs.execute('SELECT * FROM todowords')
    todowords = curs.fetchall() # [(1, "word1"), (2, "word2"), ...]
    words = [word[1] for word in todowords] # ["word1", "word2", ...]
    curs.close()
    return render_template('index.html', title='一覧', words=words), 200

@app.route('/post', methods=['POST'])
def adddata():
    word = request.form['add']
    # 登録する
    try:
        db = get_db()
        curs = db.cursor()
        curs.execute(f'INSERT INTO todowords(todo) values("{word}")')
        db.commit()
        curs.close()
        return json.dumps({'success':True, 'word': word}), 200, {'ContentType':'application/json'}
    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

@app.route('/delete', methods=['POST'])
def delconfirm():
    params = request.form.getlist('delwords')
    if params:
        return render_template('confirm.html', title='確認画面', todowords=params)
    else:
        return render_template('selecterr.html', title='選択エラー画面')

@app.route('/delexe', methods=['POST'])
def delexe():
    params = request.form.getlist('delwords')

    # 削除する
    db = get_db()
    curs = db.cursor()
    for word in params:
        curs.execute(f'DELETE FROM todowords where todo = "{word}"')
    db.commit()
    curs.close()

    return redirect('/')

def main():
    app.debug = True
    app.run() # app.run(host='127.0.0.1', port='5000')

if __name__ == '__main__':
    main()
