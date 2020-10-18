import db
import uuid
from flask import Flask, render_template, redirect, url_for, request, session, flash
from pages import pages, DOMAIN, active_sessions
from datetime import timedelta

app = Flask(__name__)
app.register_blueprint(pages, url_prefix='/pages')
app.secret_key = b'\xd3b\x9d~4\xf5\xda<\x91\xa73\xf2\x7f\xf4\x0c|'
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/home')
def index():
    return render_template('index.html', domain=DOMAIN)


@app.route('/')
def index_redirect():
    """Redirects to /home on empty path"""
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    user = db.get_user(request.form["email"], request.form["psw"])
    if user:
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = user
        if request.form.get("remember"):
            session.permanent = True
        session['session_id'] = session_id
    else:
        flash('Invalid email or password!')

    return redirect(request.referrer)


@app.route('/register', methods=['POST'])
def register():
    # Check password and reentered password are the same
    if request.form['psw'] == request.form['repsw']:
        user = db.create_user(request.form['email'], request.form['username'], request.form['psw'])
        # User created if everything worked correctly
        if user:
            # Create uuid for session identifier and store in session
            session_id = str(uuid.uuid4())
            active_sessions[session_id] = user
            session['session_id'] = session_id
        else:
            # Prob email taken
            flash('A user with this email is already registered!')
    else:
        flash('Received passwords are not equal!')

    return redirect(request.referrer)

@app.route('/logout', methods=['POST'])
def logout():
    if 'session_id' in session and session['session_id'] in active_sessions.keys():
        del active_sessions[session['session_id']]
        session.pop('session_id', None)
        return redirect(request.referrer)
    else:
        return '<h1>Unauthorized Request!</h1>', 403
    

@app.route('/delete', methods=['POST'])
def delete():
    if 'session_id' in session and session['session_id'] in active_sessions.keys():
        user = active_sessions[session['session_id']]
        result = db.delete_user(user.email)
        del active_sessions[session['session_id']]
        session.pop('session_id', None)
        if result == 1:
            flash('Account deleted successfully!')
        else:
            flash('An error occurred during the operation')
        return redirect(request.referrer)
    else:
        return '<h1>Unauthorized Request!</h1>', 403
    

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'session_id' in session and session['session_id'] in active_sessions.keys():
        # Re fetch user with given curr password
        user = db.get_user(active_sessions[session['session_id']].email, request.form['currpsw'])
        if user and request.form['newpsw'] == request.form['renewpsw']:
            # Correct password and new pass equals re entered new pass
            result = db.update_user(user.email, 'password', request.form['newpsw'])
            if result == 1:
                flash('Password changed!')
            else:
                flash('Password must contain 8 to 20 alphanumeric characters or the following characters (*, +, !, &)')
        else:
            flash('Invalid password!')
        return redirect(request.referrer)
    else:
        return '<h1>Unauthorized Request!</h1>', 403


if __name__ == '__main__':
    app.run()