from flask import Flask, render_template, request, redirect, session
from captcha.image import ImageCaptcha
import random, string, time

app = Flask(__name__)
app.secret_key='tcc'

usuarios={"admin":"1234"}
metricas=[]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    session['inicio']=time.time()
    session['user']=request.form['usuario']
    session['senha']=request.form['senha']
    return redirect('/captcha')

@app.route('/captcha')
def captcha():
    code=''.join(random.choices(string.ascii_uppercase+string.digits,k=5))
    session['captcha']=code
    image=ImageCaptcha()
    image.write(code,'static/captcha.png')
    return render_template('captcha.html')

@app.route('/validar', methods=['POST'])
def validar():
    tempo=time.time()-session['inicio']
    captcha_ok=request.form['captcha']==session['captcha']
    login_ok=usuarios.get(session['user'])==session['senha']
    sucesso=captcha_ok and login_ok

    metricas.append({
        'tempo':tempo,
        'sucesso':sucesso
    })

    if sucesso:
        return redirect('/dashboard')
    return render_template('captcha.html', erro=True)

@app.route('/dashboard')
def dashboard():
    total=len(metricas)
    sucessos=sum(m['sucesso'] for m in metricas)
    media=sum(m['tempo'] for m in metricas)/total if total else 0
    return render_template('dashboard.html',total=total,sucessos=sucessos,media=round(media,2))

if __name__=='__main__':
    app.run(debug=True)