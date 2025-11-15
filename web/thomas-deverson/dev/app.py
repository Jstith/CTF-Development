from flask import (Flask, flash, redirect, render_template, request, send_from_directory, session, url_for)
from datetime import datetime

app = Flask(__name__)

c = datetime.now() 
f = c.strftime("%Y%m%d%H%M")
app.secret_key = f'THE_REYNOLDS_PAMPHLET-179708250845'

# No Federalists Allowed!!!!
allowed_users = ['Jefferson', 'Madison', 'Burr']

@app.route('/')
def index():
    session['name'] = 'guest'
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get user input from HTML form
        name = request.form['user_input']
        
        # Unbreakable User Authentication!
        if(name in allowed_users):
            flash('Cannot login as ' + name + ', account is protected!')
            return redirect(url_for('index'))
        
        session['name'] = request.form['user_input']
    except: ()
    return redirect(url_for('messages'))

@app.route('/messages')
def messages():
    try:
        if(session['name'] in allowed_users):
            return render_template('flag.html')
    except: ()

    return render_template('denied.html')

@app.route('/backup')
def backup():
    return render_template('backup.html', data=open('static/backup.txt', 'r').read().replace('\n', '<br>').replace('    ', '&emsp;'))

@app.route('/status')
def status():
    start_date = datetime(1797, 8, 25, 8, 45)
    current_date = datetime.now()
    time_difference = current_date - start_date
    days = time_difference.days
    hours, r_seconds = divmod(time_difference.seconds, 3600)
    minutes = r_seconds // 60
    return f'System healthy! Computing uptime...\n{days} days {hours} hours {minutes} minutes'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)