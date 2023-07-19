from flask import Flask, render_template, request
from lyrics import prompt_lyric
from utils import get_base_url

port = 81
base_url = get_base_url(port)
if base_url == '/':
  app = Flask(__name__)
else:
  app = Flask(__name__, static_url_path=base_url + 'static')

@app.route(f'{base_url}')
def home():
  return render_template('index.html')


@app.route('/generate_text', methods = ['POST'])
def generate_text():
    user_input = request.form['prompt']
    lyric = prompt_lyric(user_input)
    return render_template('index.html', scroll = 'swift_gen', generated=lyric)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)