# Welcome To SwiftGen!

# Website hosted at: 
[https://morning-meadow-85564-c8d5f713d93f.herokuapp.com/](url)

# Overview:

SwiftGen is a website that allows users to randomly generate AI lyrics which follow in the style of Taylor Swift. I believe that this is a great way to inspire youth to gain interest for the field!

# Tech Stack:
- Flask
- HTML
- CSS
- Bootstrap
- Hugging Face
- GPT-Neo


# Project Summary:

- Utilized GPT-2 embeddings and the GPT-Neo model from Hugging Face to implement a full-stack website using HTML, CSS, and Flask that outputs lyrics in the style of Taylor Swift
- Preprocessed the dataset containing lyrics from her six best-selling albums by reformatting each sequence to contain 4 lines of lyrics and removed sequences with outlier lengths or overly repetitive tokens
- Deployed the model with a training loss of 0.138 to Hugging Face and fine-tuned the output of API calls by adjusting hyperparameters, resulting in a 20% increase in cohesive and accurate lyrics
- Created a second thread which is responsible for handling the random lyric generation in the background
