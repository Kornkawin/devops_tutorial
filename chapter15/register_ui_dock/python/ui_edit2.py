from flask import Flask, request, render_template, redirect, session
from model import OTPForm, AuthenForm, RegForm
from flask_bootstrap import Bootstrap
from requests.auth import HTTPBasicAuth
import requests
import json
import redis
from flask_session import Session
from flask_caching import Cache
import socket

config = {
    'DEBUG': True,
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://session_server:6379')

sess = Session()
sess.init_app(app)

auth = HTTPBasicAuth('admin', 'devops101')

def getSession(key):
    return session.get(key, 'none')

def setSession(key, value):
    session[key] = value
    
def resetSession():
    session.clear()

app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def otp():
    name = socket.gethostname()

    form = OTPForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        headers = {'content-type': 'application/json'}
        URL = 'https://service.lab20.cpsudevops.com/getotp/'
        data = {'email': form.email.data}
        res = requests.post(URL, data = json.dumps(data), headers=headers, auth=auth)
        result = res.json().get('results')

        if result != '0':
            setSession('email', form.email.data)
            return redirect('https://service.lab20.cpsudevops.com/authenui')
        else:
            return 'Email ของคุณไม่ถูกต้อง/คุณเคยลงทะเบียนแล้ว'

    return render_template('otp.html', form=form, name=name)

@app.route('/authen', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def authen():
    name = socket.gethostname()

    form = AuthenForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        headers = {'content-type': 'application/json'}
        URL = 'https://service.lab20.cpsudevops.com/authen/'
        data = {'email': getSession('email'), 'otp':  form.otp.data}
        res = requests.post(URL, data = json.dumps(data), headers=headers, auth=auth)
        result = res.json().get('results')

        if result == 1:
            setSession('authen', 'yes')
            return redirect('https://service.lab20.cpsudevops.com/regui')
        else:
            return 'กรุณาใส่ OTP/Email ใหม่'

    return render_template('authen.html', form=form, name=name)

@app.route('/reg', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def registration():
    if getSession('authen') != 'yes':
        return 'คุณไม่ได้รับอนุญาตให้เข้าถึงหน้านี้'

    name = socket.gethostname()

    form = RegForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        headers = {'content-type': 'application/json'}
        URL = 'https://service.lab20.cpsudevops.com/register/'
        data = {'firstname': form.name_first.data, 'lastname': form.name_last.data, 'email': getSession('email')}
        res = requests.post(URL, data = json.dumps(data), headers=headers, auth=auth)
        resetSession()
        return 'ระบบจะแจ้งยืนยันการลงทะเบียนทาง Email'

    return render_template('reg.html', form=form, name=name)
    