# import pyttsx3

# engine = pyttsx3.init()

# # List available voices
# voices = engine.getProperty('voices')
# for index, voice in enumerate(voices):
#     print(f"Voice {index}: {voice.name}")

# # Set properties before adding anything to speak
# # Change the index to select a different voice
# engine.setProperty('voice', voices[1].id)  # Example: Change to a different index for another voice
# engine.setProperty('rate', 100)  # Speed of speech

# engine.say("The Wise King and the Golden Land")
# engine.runAndWait()

# from gtts import gTTS
# import os

# text = "The Wise King and the Golden Land"
# tts = gTTS(text, lang='en', slow=False)  # Set lang='hi' for Hindi, if needed
# tts.save("king_story.mp3")
# os.system("start king_story.mp3")  # For Windows
# # os.system("afplay king_story.mp3")  # For macOS
# # os.system("mpg321 king_story.mp3")  # For Linux
from gtts import gTTS
import io
import pygame

# Initialize pygame mixer
pygame.mixer.init()

text = "The Wise King and the Golden Land Once upon a time, in the kingdom of Avalora, there lived a wise and kind king named Aric. His people adored him, for he ruled with justice and compassion. Avalora was a prosperous land, blessed with golden fields, clear rivers, and towering mountains"
tts = gTTS(text, lang='en', slow=False, tld='co.uk')  # Use 'co.uk' for a British accent

# Save to a file-like object
fp = io.BytesIO()
tts.write_to_fp(fp)
fp.seek(0)

# Load and play the audio
pygame.mixer.music.load(fp, 'mp3')
pygame.mixer.music.play()

# Keep the program running until the audio finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
