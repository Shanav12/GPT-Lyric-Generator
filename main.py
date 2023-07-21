from flask import Flask, render_template
import lyrics
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


@app.route('/generate_text', methods=["POST"])
def generate_text():
  lyric = lyrics.get_random_lyric()
  if lyric == None:
    lyric = 'Sorry, try again'
  lyric = lyric.replace('?,', '?')
  lyric = lyric.replace('!,', '!')
  return render_template("index.html", generated=lyric, scroll='swift_gen')


def main():
  app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
  lyrics.start_lyric_generation()
  main()