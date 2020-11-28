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
	user_input = False

	if request.method == 'GET':
		try:
			formula = request.args['formula']
			form.formula.data = formula  # put URL param into form
			user_input = True
		except KeyError:  # if invalid URL params are given
			pass

	if request.method == 'POST':
		formula = form.data['formula']
		formula = parse_unicode(formula)
		user_input = True

	if user_input:
		try:
			result = backend.output_as_string(formula)
		except Exception as e:
			result = str(e)
		result = result.replace('\n','<br>')
		result = result.replace('    ','&emsp;&emsp;&emsp;&emsp;')
		return render_template('index.html', form=form, result=result, symbols=['→', '∀', '∃', '¬', '∧', '∨'])

	else:
		return render_template('index.html', form=form,symbols=['→','∀','∃','¬','∧','∨'])



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
