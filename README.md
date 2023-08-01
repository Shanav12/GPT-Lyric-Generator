# TaylorSwiftLyricGenerator

**Welcome To SwiftGen!**

SwiftGen is a website that allows users to randomly generate AI lyrics which follow in the style of Taylor Swift.


**Tech Stack:**
- Flask
- HTML
- CSS
- Bootstrap
- Hugging Face
- GPT-Neo



**Project Summary:**

- Utilized GPT-2 embeddings and the GPT-Neo model from Hugging Face to implement a full-stack website using HTML, CSS, and Flask that outputs - lyric in the style of Taylor Swift
- Preprocessed the dataset containing lyrics from her six best-selling albums by reformatting each sequence to contain 4 lines of lyrics and removed sequences with outlier lengths or overly repetitive tokens
- Deployed the trained model which had a training loss of 0.138 to HuggingFace and fine-tuned the output of API calls by adjusting hyperparameters such as max tokens and repetition penalty
- Created a second thread which is responsible for handling the random lyric generation in the background
