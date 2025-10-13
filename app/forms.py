from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(
            '(?=.*[0-9])(?=.*[A-Z])(?=.*[!@#$%^&*])',
            message="Senha deve ter ao menos 1 maiúscula, 1 número e 1 caractere especial"
        )
    ])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
