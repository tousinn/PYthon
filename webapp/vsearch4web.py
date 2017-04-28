from flask import Flask, render_template, request, redirect, escape
from vsearch import search4letter
from DBcm import UseDatabase
app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1',
				'user':'vsearch',
				'password':'vsearchpasswd',
				'database':'vsearchlogDB',}
def log_request(req:'flask_request', res: str) ->None:

	###conn = mysql.connector.connect(**dbconfig)
	###cursor = conn.cursor()
	with UseDatabase(app.config['dbconfig']) as curor:
		_SQL = """ insert into log (phrase,letters,ip,browser_string,results) values (%s,%s,%s,%s,%s) """
		cursor.execute(_SQL,(req.form['phrase'],req.form['letters'],req.remote_addr,req.user_agent.browser,res,))
	###conn.commit()
	###cursor.close()
	###conn.close()
	###with open('vsearch.log','a') as log:
	###	print(req.form, req.remote_addr,req.user_agent, res, file=log, sep='|')

@app.route('/')
def hello () -> '302':
    return redirect('/entry')

@app.route('/search4', methods=['post'])
def do_search() -> 'html':
    #return str(search4letter('life, the universe, and everything', 'eiru,!'))
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letter(phrase,letters))
    log_request(request,results)
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
def view_the_log() ->'html':

	with UseDatabase(app.config['dbconfig']) as cursor:
		_SQL= """select phrase, letters, ip, browser_string, results from log"""
		cursor.execute(_SQL)
		contents = cursor.fetchall()
	##contents=[]
	##with open('vsearch.log') as log:
	##	for line in log:
	##		contents.append([])
	##		for item in line.split('|'):
	##			contents[-1].append(escape(item))
	
	titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
	return render_template('viewlog.html',
							the_title='View Log',
							the_row_titles=titles,
							the_data=contents,)

if __name__ == '__main__':
	app.run(debug=True)

