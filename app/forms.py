from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, SubmitField, BooleanField, EmailField, IntegerField, RadioField, SelectField, DateField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo, ValidationError, Optional
from app.models.user import User

#FORMULÁRIO DO CADASTRO
class Cadastro_Formulario(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já existente! Tente outro.')
        
    email = EmailField('E-mail',
                            validators=[DataRequired(), Email(), Length(max=256)])
    senha = PasswordField('Senha',
                          validators=[DataRequired(), Length(min=8, max=50)])
    confirm_senha = PasswordField('Confirme a senha',
                          validators=[DataRequired(), EqualTo('senha', message='As senhas estão diferentes')])
    nome = StringField('Nome',
                          validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('Confirmar')

#FORMULÁRIO DO LOGIN
class Login_Formulario(FlaskForm):
    email = EmailField('E-mail',
                            validators=[DataRequired(), Email(), Length(max=256)])
    senha = PasswordField('Senha',
                            validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Entrar')

#FORMULARIO DA TASK
class TaskForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[Optional(), Length(max=500)])
    data_limite = DateField('Data Limite', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Salvar')