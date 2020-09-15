from flask import Flask, render_template, request
from wtforms import SelectField, StringField, FloatField, FormField, validators, BooleanField
import backend
import mpld3
import os

from flask_wtf import FlaskForm, CSRFProtect  # Flask-WTF provides your Flask application integration with WTForms.

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.environ['csrf']

class FormulaForm(FlaskForm):
	formula = StringField('Enter the formula to check')


@csrf.exempt  # I believe we don't need CSRF for a site without any user accounts
@app.route('/', methods=['GET','POST'])
def index():
	form = FormulaForm()
	if request.method == 'GET':
		return render_template('index.html', form=form,symbols=['→','∀','∃','¬','∧','∨'])
	if request.method == 'POST':
		formula = form.data['formula']
		formula = parse_unicode(formula)
		result = backend.output_as_string(formula)
		result = result.replace('\n','<br>')
		result = result.replace('    ','&emsp;&emsp;&emsp;&emsp;')
		return render_template('index.html', form=form,result=result,symbols=['→','∀','∃','¬','∧','∨'])


def parse_unicode(formula):
	formula = formula.replace('→','>')
	formula = formula.replace('∀','@')
	formula = formula.replace('∃','!')
	formula = formula.replace('¬','-')
	formula = formula.replace('∧','*')
	formula = formula.replace('∨','+')
	return formula


if __name__ == "__main__":
	app.run(debug=True)
