from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange
from random import choice
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class Gameform(FlaskForm):
    napravlenie = SelectField('Выбери направление', coerce=int, choices=[(0, 'Север'),(1, 'Восток'),(2, 'Юг'),(3, 'Запад')],)
    step = IntegerField('Как далеко планируете продвинуться', validators=[NumberRange(min=1, max=5), DataRequired()], default=1)
    submit = SubmitField('В путь!')

class Button(FlaskForm):
    submit = SubmitField('Принять испытание')

@app.route('/', methods=['GET', 'POST'])
def button():
    form = Button()
    if request.method == 'POST':
        return redirect('/index')
    return render_template('basic.html', form=form)

class Counter():
    def __init__(self, c):
        self.c = c
counter = Counter(0)

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Gameform()
    if request.method == 'POST':
        napravlenie = request.form['napravlenie']
        step = request.form['step']
        global counter
        if counter.c == 0:
            result, position = location(int(napravlenie), int(step))
            counter.c += 1
            counter.position = position
            print(counter.position)
            return render_template('index.html', form=form, result=result)
        else:
            result, position = location(int(napravlenie), int(step), counter.position)
            counter.c += 1
            counter.position = position
            print(counter.position)
            return render_template('index.html', form=form, result=result)
    return render_template('index.html', form=form)


@app.route('/<int:number>', methods=['GET', 'POST'])
def number_location(number):
    form = Gameform()
    if request.method == 'POST':
        napravlenie = request.form['napravlenie']
        step = request.form['step']
        global counter
        if counter.c == 0:
            result, position = location(int(napravlenie), int(step))
            counter.c += 1
            counter.position = position
            print(counter.position)
            return render_template('index.html', form=form, result=result)
        else:
            result, position = location(int(napravlenie), int(step), counter.position)
            counter.c += 1
            counter.position = position
            print(counter.position)
            return render_template('index.html', form=form, result=result)
    return render_template('index.html', form=form)


def location(direction,steps, position=None):
  result = []
  dir = {1:'"Балкон"', 2:'"Спальня"', 3:'"Холл"', 4:'"Кухня"', 5:'"Подземелье"', 6:'"Коридор"', 7:'"Оружейная"'}
  mtrx = [[0,1,0],
          [2,3,4],
          [5,6,7]]

  if position:
      index_1 = position[0]
      index_2 = position[1]
      print('Вы находитесь в комнате', dir[mtrx[index_1][index_2]])
      result.append(f'Вы находитесь в комнате {dir[mtrx[index_1][index_2]]}')
  else:
      index_1 = choice([0,1,2])
      index_2 = choice([0,1,2])

      while  mtrx[index_1][index_2] == 0 or mtrx[index_1][index_2] == 1:
        index_1 = choice([0,1,2])
        index_2 = choice([0,1,2])
      print('Вы заспавнились в комнате',dir[mtrx[index_1][index_2]])
      result.append(f'Вы заспавнились в комнате {dir[mtrx[index_1][index_2]]}')


  for i in range(steps):

    if direction == 0:
      index_1 = index_1 - 1

    elif direction == 2:
      index_1 = index_1 + 1

    elif direction == 1:
      index_2 = index_2 + 1

    elif direction == 3:
      index_2 = index_2 - 1

    if index_1 < 0 or index_2 < 0 or index_1 > 2 or index_2 > 2:
        print('Вы не можете идти сюда')
        result.append('Вы не можете идти сюда')
        break
    try:
        print('Вы находитесь в комнате', dir[mtrx[index_1][index_2]])
        result.append(f'Вы находитесь в комнате {dir[mtrx[index_1][index_2]]}')
        position = [index_1, index_2]
    except:
      print('Вы не можете идти сюда')
      result.append('Вы не можете идти сюда')
      break
    for i in result:
        if 'Балкон' in i:
            result.append('Вы выбрались на чистный воздух')
  return result, position

if __name__ == '__main__':
    app.run(debug=True)