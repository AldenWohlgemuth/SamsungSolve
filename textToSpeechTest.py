#imports
from gtts import gTTS
import os

def readOut(read):
    #set speech components
    lang="en"
    myobj=gTTS(text=read, lang=lang, slow=False)

    #Save as wav or overwrites the original file in the folder
    myobj.save("output.mp3")

    #Open wav with default mediaplayer
    os.system("output.mp3")

readOut("Testing testing 1 2 3!")