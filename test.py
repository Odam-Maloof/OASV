import sys
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
