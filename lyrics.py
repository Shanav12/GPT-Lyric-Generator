import requests
import json
from nltk.corpus import brown

API_URL = "https://api-inference.huggingface.co/models/Shanav12/swift_lyrics_final"
headers = {"Authorization": "Bearer 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"}


invalid_characters = '.#$%&()-*+,/:;<=>?@[\\]^_`{|}~0123456789'
brown_corpus = set(brown.words())


# Private function to validate the generated quote
def valid(text):
  # If the text is empty, return False
  if len(text) == 0:
    return False

  # Split the text into individual words
  words = text.split(' ')

  # Iterate through each word
  for index in range(0, len(words)):
    word = words[index]

    # Replace each invalid character with a space
    for char in invalid_characters:
      word = word.replace(char, ' ')

    # Remove leading/trailing spaces and split the resulting string in case the removal of invalid characters led to multiple words
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
    # If the word is not in the corpus or it contains an apostrophe in the last three characters in the word
    if (word not in brown_corpus
        and word[-1] != 's') or (word.find('\'') != -1
                                 and word.find('\'') < len(word) - 3):
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
    response = requests.request("POST", API_URL, headers=headers, data=data)
    content = json.loads(response.content.decode('utf-8'))
    # If response is empty or contains an error, raise an exception to retry quote generation
    if len(content) <= 0 or 'error' in content[0]:
      raise Exception
    # Extract generated quote text from response
    quote = content[0]['generated_text'].replace('\n', '')
    if valid(quote):
      return quote
    
    if count >= 10:
      raise Exception
    
    return prompt_lyric(prompt, count + 1)

  except Exception:
    # Retry generating quote in case of exceptions, up to 10 retries
    if count < 10:
      return prompt_lyric(prompt, count + 1)