'''import sys
import numpy as np
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class AudioVisualizer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.labels = []
        for _ in range(20):
            label = QtWidgets.QLabel()
            self.labels.append(label)
            layout.addWidget(label)
        
        self.setLayout(layout)
        
    def update_visualizer(self, amplitude_data):
        for i, label in enumerate(self.labels):
            scaled_height = int(amplitude_data[i] * 1000)
            label.setFixedHeight(scaled_height)
            label.setStyleSheet(f"background-color: blue;")

class AudioPlayer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.visualizer = AudioVisualizer()
        layout.addWidget(self.visualizer)
        
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)
        
        self.setLayout(layout)
        
        self.media_player = QMediaPlayer()
        self.media_player.setNotifyInterval(100)  # Set the interval for audio level notifications
        
        self.media_player.positionChanged.connect(self.update_visualizer)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        
    def play_audio(self):
        file_path = "audio/Tobu - Candyland.mp3"  # Replace with your audio file's path
        media_content = QMediaContent(QtCore.QUrl.fromLocalFile(file_path))
        self.media_player.setMedia(media_content)
        self.media_player.play()
        
    def update_visualizer(self, position):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            audio_level = self.media_player.audioLevel()
            amplitude_data = np.random.rand(20)  # Replace with your audio analysis logic
            self.visualizer.update_visualizer(amplitude_data)
            
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.stop()
            self.visualizer.update_visualizer(np.zeros(20))  # Reset visualizer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    player = AudioPlayer()
    player.show()
    
    sys.exit(app.exec_())
'''
'''import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer
import pyqtgraph as pg
from pydub import AudioSegment

class AudioVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Create a PlotWidget for the audio visualization
        self.plot = pg.PlotWidget()
        self.plot.setLabel('left', 'Amplitude')
        self.plot.setLabel('bottom', 'Time')
        self.plot.showGrid(x=True, y=True)
        self.layout.addWidget(self.plot)

        self.setLayout(self.layout)

        # Initialize variables for audio visualization
        self.audio_data = np.array([])
        self.sample_rate = 44100
        self.current_position_line = None

    def updatePlot(self, current_position):
        self.plot.clear()
        self.plot.plot(self.audio_data, pen=(255, 0, 0))
        
        if current_position is not None:
            # Add a vertical line at the current position
            if self.current_position_line is not None:
                self.plot.removeItem(self.current_position_line)
            self.current_position_line = pg.InfiniteLine(pos=current_position, angle=90, movable=False)
            self.plot.addItem(self.current_position_line)

    def setAudioData(self, audio_data, sample_rate):
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.updatePlot(None)

class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Create a button to open an audio file
        self.file_button = QPushButton('Open Audio File')
        self.layout.addWidget(self.file_button)
        self.file_button.clicked.connect(self.openAudioFile)

        # Create a button to play the audio
        self.play_button = QPushButton('Play')
        self.layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.playAudio)

        # Create an audio visualizer widget
        self.visualizer = AudioVisualizer()
        self.layout.addWidget(self.visualizer)

        self.central_widget.setLayout(self.layout)

        # Initialize variables for audio playback
        self.audio_data = np.array([])
        self.sample_rate = 44100
        self.current_position = None

        # Create a QMediaPlayer for audio playback
        self.media_player = QMediaPlayer()
        self.media_player.positionChanged.connect(self.updateCurrentPosition)

    def openAudioFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav);;All Files (*)", options=options)
        if file_path:
            self.loadAudioFile(file_path)

    def loadAudioFile(self, file_path):
        # Use pydub to load and decode the audio file
        audio = AudioSegment.from_file(file_path)
        self.audio_data = np.array(audio.get_array_of_samples())
        self.sample_rate = audio.frame_rate

        # Create a media content from the file
        media_content = QMediaContent(QUrl.fromLocalFile(file_path))
        self.media_player.setMedia(media_content)

        # Set audio data for visualization
        self.visualizer.setAudioData(self.audio_data, self.sample_rate)

    def playAudio(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText('Play')
        else:
            self.media_player.play()
            self.play_button.setText('Pause')

    def updateCurrentPosition(self, position):
        if position >= 0:
            # Calculate the current position in seconds
            self.current_position = position / 1000.0  # Convert to seconds
            self.visualizer.updatePlot(self.current_position)

def main():
    app = QApplication(sys.argv)
    window = AudioPlayer()
    window.setWindowTitle('Audio Player with Visualizer')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()'''

'''import subprocess

# Print something to the console
print("Hello World")

# Define the command to capture console output (e.g., 'ls' on Unix-like systems)
command = "test.py"  # Replace with the appropriate command for your system

# Run the command and capture its output
try:
    console_output = subprocess.check_output(command, shell=True, universal_newlines=True)
except subprocess.CalledProcessError as e:
    console_output = e.output
print(console_output)
print("printed console")

# Define the string you want to check for
search_string = "Hello World" 


# Check if the search string is in the console output
if search_string in console_output:
    print(f"The console contains '{search_string}'.")
else:
    print(f"The console does not contain '{search_string}'.")'''

from contextlib import redirect_stdout

# Create a StringIO object to capture stdout
from io import StringIO
stdout_buffer = StringIO()

x = 0
# Use the context manager to redirect stdout to the buffer
while x != 1:
    with redirect_stdout(stdout_buffer):
        import logging

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        logger.info("This message will be logged to the console.")

    # Check if there is any content in the captured stdout
    captured_stdout = stdout_buffer.getvalue()
    if captured_stdout:
        print("Captured stdout:", captured_stdout)
    x += 1
    stdout_buffer = StringIO()






