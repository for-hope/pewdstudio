from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,RadioField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
import sys
from app.search import search_query

class TranslationForm(FlaskForm):
    text = TextAreaField('',render_kw={'rows': 4,'cols': 50,'style':'resize: none;'},validators=[DataRequired()])
    radio = RadioField('Search', choices=[('normal','Normal Search'),('advanced','Advanced Search')],default='normal')
    submit = SubmitField('Search')
  
    def searchLines(self):
        return search_query(self.text.data)
    def getRadio(self):
        return radio.data



    
