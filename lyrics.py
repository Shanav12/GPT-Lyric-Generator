import requests
import json
from nltk.corpus import brown
import threading
import time
import random
import linecache
import os


API_URL = "https://api-inference.huggingface.co/models/Shanav12/swift_lyrics_final"
API_KEY = os.environ['Bearer']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


invalid_characters = '.#$%&()-*+,/:;<=>?@[\\]^_`{|}~0123456789'
brown_corpus = set(brown.words())


def valid(text):
  if len(text) == 0:
    return False

  # Split the text into individual words
  words = text.split(' ')

  for index in range(0, len(words)):
    word = words[index]

    for char in invalid_characters:
      word = word.replace(char, ' ')

    word = word.strip()
    new_words = word.split(' ')

    # Remove the old word before adding new word(s)
    words.pop(index)
    for new_word in new_words:
      # Add each new word to the list of words
      words.insert(index, new_word.strip().lower())
      index += 1

  # Remove any empty strings from the word list
  words = [word for word in words if word != '']
  
  for word in words:
    if word not in brown_corpus:
      return False
    
  return True


def prompt_lyric(prompt, count = 0):
  # Prepare data for the HuggingFace API call
  data = json.dumps({
    "inputs": str(prompt.strip()),
    "parameters": {
      "top_k": None,
      "top_p": 0.75,
      "temperature": 1.0,
      "repetition_penalty": 5,
      "max_new_tokens": 250,
      "max_time": 10,
      "return_full_text": True,
      "num_return_sequences": 1,
      "do_sample": True
    },
    "options": {
      "use_cache":
      False,  # Not using previously identical cached output
      "wait_for_model":
      True  # Wait for the model to finish loading
    }
  })

  try:
    # Make POST request to HuggingFace API
    response = requests.post(API_URL, headers=headers, data=data)
    content = json.loads(response.content.decode('utf-8'))
    # If response is empty or contains an error, raise an exception to retry lyric generation
    if len(content) <= 0 or 'error' in content[0]:
      raise Exception

    lyric = content[0]['generated_text'].replace('\n', '')
    if valid(lyric):
      return lyric
    
    if count >= 10:
      raise Exception
    
    return prompt_lyric(prompt, count + 1)

  except Exception:
    # Retry generating lyric in case of exceptions, up to 10 retries
    if count < 10:

      # Waiting 5 seconds before making another API call to avoid rate limits
      time.sleep(5)
      return prompt_lyric(prompt, count + 1)
    

# Private function to generate random lyric using a random lyric starter
def random_lyric():
  number = random.randint(1, 951)
  lyric = linecache.getline('lyric_starters.txt', number)
  lyric = str(lyric).replace('\n', '')
  return prompt_lyric(lyric)


lyrics_lock = threading.Lock()
lyrics = []  
queue_size = 50  
wait_time_seconds = 5  
should_end = False  

# Private function running in second thread to generate random lyrics and fill the lyric queue
def generate_lyrics():
  # Ensuring changes exist outside of this function
  global should_end, lyric_thread, lyrics_lock, lyrics
  end = False
  temp_lyrics = []

  while not end:
    start_time = time.time()

    # Attempt to fill up half the queue size with new lyrics
    for i in range(0, round(queue_size / 2) - len(temp_lyrics)):
      temp_lyrics.append(random_lyric())

      # Break the loop if lyric generation took longer than the wait time
      if time.time() - start_time > wait_time_seconds:
        break

    # If lyric generation was faster than the wait time, sleep for the remaining duration
    if time.time() - start_time < wait_time_seconds:
      time.sleep(wait_time_seconds - (time.time() - start_time))

    with lyrics_lock:
      end = should_end

      for i in range(0, round(queue_size / 2) - len(lyrics)):
        # Break the loop if there are no more new lyrics
        if len(temp_lyrics) == 0:
          break

        # Add the new lyric to the queue and remove from the new lyrics list
        lyrics.append(temp_lyrics[0])
        temp_lyrics.pop(0)


lyric_thread = threading.Thread(target=generate_lyrics)


def get_random_lyric():
  global should_end, lyric_thread, lyrics_lock, lyrics

  with lyrics_lock:
    if len(lyrics) > 0:
      # Return the first lyric from the queue and delete it
      lyric = lyrics[0]
      lyrics.pop(0)
      return lyric
    else:
      return random_lyric()


# Public function to start the lyric generation thread
def start_lyric_generation():
  global lyric_thread
  lyric_thread.start()


# Public function to stop the lyric generation thread
def end_lyric_generation():
  global lyric_thread, lyrics_lock, should_end
  with lyrics_lock:
    should_end = True
  lyric_thread.join(timeout=5)