# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os




app = Flask(__name__)
app.secret_key = os.urandom(24)


def check_bosh_url(cimp,secure=False):
    try:
        url='https://{}:7335/httpbinding'.format(cimp) if secure else 'http://{}:7335/httpbinding'.format(cimp)
        res=requests.get(url,verify=False)
        if res.status_code:
            return url
    except:
        return None
        
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        url=check_bosh_url(session['cimp'])
        if not url:
            url=check_bosh_url(session['cimp'],True)
            if not url:
                return render_template('errors.html',error="BOSH interface is down")
        return render_template('index.html',user=session['user'], password=session['password'], bosh_url=url, chat=session['chat'])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        session['user'] = request.form['username']
        session['password']=request.form['password']
        session['cimp']=request.form['cimp']
        session['chat']=request.form['chat']
        return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    error = None
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=80,host='0.0.0.0',debug=True,use_reloader=False)


