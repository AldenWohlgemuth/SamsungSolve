#imports
from PyQt5 import QtCore, QtGui, QtWidgets
from openai import OpenAI
import time
from gtts import gTTS
import os
import speech_recognition as sr
import pyaudio
import RPi.GPIO as GPIO

#buttons
OPTION_1 = 5
OPTION_2 = 6
OPTION_3 = 13
OPTION_4 = 19
REFRESH = 26
GPIO.setmode(GPIO.BCM)

GPIO.setup(OPTION_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(OPTION_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(OPTION_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(OPTION_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(REFRESH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_option1_state = GPIO.input(OPTION_1)
previous_option2_state = GPIO.input(OPTION_2)
previous_option3_state = GPIO.input(OPTION_3)
previous_option4_state = GPIO.input(OPTION_4)
previous_refresh_state = GPIO.input(REFRESH)

#create ai model
client = OpenAI(api_key="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")
assistant = client.beta.assistants.retrieve("asst_5vZDiGTQa8b4RnALXLaCUjhP")

question = ""

#setup UI
class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        mainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(10, 20, 391, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setMouseTracking(False)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 240, 391, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(400, 240, 391, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 20, 391, 221))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.Refresh = QtWidgets.QPushButton(self.centralwidget)
        self.Refresh.setGeometry(QtCore.QRect(280, 180, 241, 121))

        font = QtGui.QFont()
        font.setPointSize(12)
        self.Refresh.setFont(font)
        self.Refresh.setObjectName("Refresh")
        self.Refresh.clicked.connect(update)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.pushButton_1.setStyleSheet("QPushButton { background-color: #ff6e6e; color: black; }")
        self.pushButton_2.setStyleSheet("QPushButton { background-color: #ffa66e; color: black; }")
        self.pushButton_3.setStyleSheet("QPushButton { background-color: #7fff6e; color: black; }")
        self.pushButton_4.setStyleSheet("QPushButton { background-color: #6e92ff; color: black; }")
        self.Refresh.setStyleSheet("QPushButton { background-color: #ffffff; color: black; }")

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.pushButton_1.clicked.connect(lambda: readOut(ui.pushButton_1.text()))
        self.pushButton_2.clicked.connect(lambda: readOut(ui.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: readOut(ui.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: readOut(ui.pushButton_4.text()))

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Samsung Solve LHS"))
        self.pushButton_1.setText(_translate("mainWindow", "..."))
        self.pushButton_2.setText(_translate("mainWindow", "..."))
        self.pushButton_3.setText(_translate("mainWindow", "..."))
        self.pushButton_4.setText(_translate("mainWindow", "..."))
        self.Refresh.setText(_translate("mainWindow", "Refresh"))

def listen_for_question():
    recognizer = sr.Recognizer()
    while True:  # This is an infinite loop
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            global question
            question = recognizer.recognize_google(audio)
            print(question)


            ui.Refresh.setEnabled(False)
            ui.pushButton_1.setEnabled(False)
            ui.pushButton_2.setEnabled(False)
            ui.pushButton_3.setEnabled(False)
            ui.pushButton_4.setEnabled(False)
            update()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass
        except Exception as e:
            pass

#format ai response
def stringed(long):
    stringer = long.split('\n')
    stringy = []
    for i in stringer:
        for x in range(0,3):
            i = i.replace(i[0],"",1)
        stringy.append(i)

    return stringy

def readOut(read):
    out = read[3:]

    #set speech components
    lang="en"
    myobj=gTTS(text=out, lang=lang, slow=False)

    #Save as wav or overwrites the original file in the folder
    myobj.save("output.mp3")

    #Open wav with default mediaplayer
    os.system("mpg123 output.mp3")

#get responses from question variable
def getResponses(que):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=que
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, 
                                                    run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            return ["error", "error", "error", "error"]
            break
        time.sleep(2)  # wait for 2 seconds before checking again
        
    # Step 5: Parse the Assistant's Response to Print the Results
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in reversed(messages.data):
        for content in message.content:
            if content.type == 'text':
                response = content.text.value 
                answer = stringed('{}'.format(response))
    return answer

def update():
    array = getResponses(question)

    ui.pushButton_1.setText("1. {}".format(array[0]))
    ui.pushButton_2.setText("2. {}".format(array[1]))
    ui.pushButton_3.setText("3. {}".format(array[2]))
    ui.pushButton_4.setText("4. {}".format(array[3]))
    
    ui.Refresh.setEnabled(True)
    ui.pushButton_1.setEnabled(True)
    ui.pushButton_2.setEnabled(True)
    ui.pushButton_3.setEnabled(True)
    ui.pushButton_4.setEnabled(True)

#run the UI
if __name__ == "__main__":
    import sys
    import threading

    os.close(sys.stderr.fileno())
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    # Start the listening thread
    listener_thread = threading.Thread(target=listen_for_question)
    listener_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
    listener_thread.start()

    try:
        while True:
            time.sleep(0.1)
            option1_state = GPIO.input(OPTION_1)
            option2_state = GPIO.input(OPTION_2)
            option3_state = GPIO.input(OPTION_3)
            option4_state = GPIO.input(OPTION_4)
            refresh_state = GPIO.input(REFRESH)
            if option1_state != previous_option1_state:
                previous_option1_state = option1_state
                if option1_state == GPIO.LOW:
                    print("OPTION_1 has just been pressed")
            if option2_state != previous_option2_state:
                previous_option2_state = option2_state
                if option2_state == GPIO.LOW:
                    print("OPTION_2 has just been pressed")
            if option3_state != previous_option3_state:
                previous_option3_state = option3_state
                if option3_state == GPIO.LOW:
                    print("OPTION_3 has just been pressed")
            if option4_state != previous_option4_state:
                previous_option4_state = option4_state
                if option4_state == GPIO.LOW:
                    print("OPTION_4 has just been pressed")
            if refresh_state != previous_refresh_state:
                previous_refresh_state = refresh_state
                if refresh_state == GPIO.LOW:
                    print("REFRESH has just been pressed")
    except KeyboardInterrupt:
        GPIO.cleanup()

    sys.exit(app.exec_())
