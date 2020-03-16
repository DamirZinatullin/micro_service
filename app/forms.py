from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Regexp


class BuildForm(FlaskForm):
    address = StringField('Адрес дома', validators=[DataRequired()])
    build_date = IntegerField('Год постройки',
                              validators=[NumberRange(min=1800, max=2100,
                                                      message='''Год постройки должен быть между 
                                                      1900 и 2050 годами''')])


class AddBricks(FlaskForm):
    count_of_bricks = IntegerField('Количество кирпичей', validators=[
        DataRequired(message='Необходимо вводить целое число'),
        NumberRange(min=0, message='Число кирпичей должно быть положительно')])
    date = DateField('Дата добавления',
                     validators=[
                         DataRequired(message='Дату необходимо вводить в формате гггг-мм-дд')])
