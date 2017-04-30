from flask import Flask, render_template, request, redirect, escape, session, copy_current_request_context
from vsearch import search4letter
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in
from threading import Thread
import time
app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1',
				'user':'vsearch',
				'password':'vsearchpasswd',
				'database':'vsearchlogDB',}

@app.route('/')
def hello () -> '302':
    return redirect('/entry')

@app.route('/search4', methods=['post'])
def do_search() -> 'html':
	@copy_current_request_context
	def log_request(req:'flask_request', res: str) ->None:
		time.sleep(15)
		with UseDatabase(app.config['dbconfig']) as curor:
			_SQL = """ insert into log (phrase,letters,ip,browser_string,results) values (%s,%s,%s,%s,%s) """
			cursor.execute(_SQL,(req.form['phrase'],req.form['letters'],req.remote_addr,req.user_agent.browser,res,))

	phrase = request.form['phrase']
	letters = request.form['letters']
	results = str(search4letter(phrase,letters))
	try:
		t= Thread(target=log_request,args=(request,results))
		t.start()
	except Exception as e:
		print('***Logging failed with error: ', str(e))

	return render_template('results.html',
    						the_title='Welcome to search4letters on the web!',
    						the_phrase= phrase,
    						the_letters = letters,
    						the_results = results,)

@app.route('/entry')
def entry_page() -> 'html':
	return render_template('entry.html',
							the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() ->'html':
	try:
		with UseDatabase(app.config['dbconfig']) as cursor:
			_SQL= """select phrase, letters, ip, browser_string, results from log"""
			cursor.execute(_SQL)
			contents = cursor.fetchall()
			titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
		return render_template('viewlog.html',
								the_title='View Log',
								the_row_titles=titles,
								the_data=contents,)
	except ConnectionError as e:
		print('Is your database switched on? Error: ', str(e))
	except CredentialsError as e:
		print('User-id/Password issues. Error: ', str(e))
	except SQLError as e:
		print ('Is your query correct? Error: ', str(e))
	except Exception as e:
		print('Someting went wrong: ', str(e))

	return 'Error'
	
	##contents=[]
	##with open('vsearch.log') as log:
	##	for line in log:
	##		contents.append([])
	##		for item in line.split('|'):
	##			contents[-1].append(escape(item))
	
	

@app.route('/login')
def do_login() ->str:
	session['logged_in'] = True
	return 'You are now logged in.'

@app.route('/logout')
def do_logout() ->str:
	session.pop('logged_in')
	return 'You are now logged out.'
app.secret_key="weoadmfwoefaffasd"

if __name__ == '__main__':
	app.run(debug=True)

