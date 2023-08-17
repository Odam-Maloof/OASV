import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aac import AAC

# make labels clickable with this class
class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        QLabel.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("")  # Remove the pressed state styles
        QLabel.mouseReleaseEvent(self, event)

class SpecialClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.setStyleSheet("background-color: #cc5d00;")
        QLabel.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("")  # Remove the pressed state styles
        QLabel.mouseReleaseEvent(self, event)

class UploadBox(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("")  # Remove the pressed state styles
        QLabel.mouseReleaseEvent(self, event)

    def dragEnterEvent(self, event):
        # Check if the event contains URLs or file paths
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Check if the event contains URLs or file paths
        if event.mimeData().hasUrls():
            # Get the list of dropped URLs
            urls = event.mimeData().urls()

            # If you expect only audio files to be dropped, you can filter them here
            file_url = [url for url in urls if url.toString().lower().endswith(('.mp3', '.wav', '.aac', '.flac'))]

            # If there are any audio files, call the drag_audio function for it
            if file_url:
                for url in file_url:
                    file_qurl = file_url[0]
                    file_stripped = file_qurl.path()
                    file_name = file_stripped.lstrip('/')
                    drag_audio(file_name)
            else:
                drag_error()

            event.acceptProposedAction()

class LoadingBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0

    def setProgress(self, value):
        self.progress = value
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the white circle first
        white_brush = QBrush(Qt.white)
        painter.setBrush(white_brush)
        rect = self.rect()
        painter.drawEllipse(rect)
        
        pen = QPen(QColor("#FF7600"), 25, Qt.SolidLine)  # Set pen width to 18
        painter.setPen(pen)
        
        rect = self.rect()
        start_angle = 0  # Start angle remains at 0 to start from the top
        span_angle = self.progress * 6  # Arc finishes after 60 progress increments
        rect.adjust(20, 20, -20, -20)  # Adjust the margins as needed
        painter.drawArc(rect, start_angle * 16, span_angle * 16)  # Multiply by 16 for angles

# define the functions that are part of the program
first_run = True
progress = 0

def fullscreen_mode():
    global first_run
    if window.height() == 1040 or first_run:
        window.resize(1920, 1080)
        lower_button_loc = window.height() - 58
        start_button.move(842, lower_button_loc)
        play_button.move(924, lower_button_loc)
        end_button.move(1006, lower_button_loc)
        implode = QPixmap('images/fullscreen-exit-line.png')
        implode_2 = implode.scaled(24,24)
        full_button.setPixmap(implode_2)
        title_bar.resize(0, 0)
        mini_button.resize(0, 0)
        maxi_button.resize(0, 0)
        close_button.resize(0, 0)
        full_button.move(full_button_loc, 26)
        setting_button.move(56, 26)
        import_button.move(144, 26)
        info_button.move(232, 26)
    else:
        maximised_size = window.height() - 40
        window.resize(window.width(), maximised_size)
        lower_button_loc = window.height() - 58
        start_button.move(842, lower_button_loc)
        play_button.move(924, lower_button_loc)
        end_button.move(1006, lower_button_loc)
        title_bar.resize(title_bar_width, title_bar_height)
        mini_button.resize(title_button_width, title_bar_height)
        maxi_button.resize(title_button_width, title_bar_height)
        close_button.resize(title_button_width, title_bar_height)
        full_button.move(full_button_loc, 56)
        full_button.setPixmap(expand_2)
        setting_button.move(56,56)
        import_button.move(144, 56)
        info_button.move(232, 56)
    first_run = False

def maximised_mode():
    if window.height() >= 1080:
        maximised_size = window.height() - 40
        window.resize(window.width(), maximised_size)
        lower_button_loc = window.height() - 58
        start_button.move(842, lower_button_loc)
        play_button.move(924, lower_button_loc)
        end_button.move(1006, lower_button_loc)
    elif window.height() == 1040:
        pass
    else:
        print('what')

def open_info_menu():
    if upload_menu.height() == 0:
        info_menu.resize(i_m_w, i_m_h)
        info_menu_title.resize(i_m_t_w, i_m_t_h)
        info_desc_para.resize(i_p_w, i_p_h)
        info_instr_para.resize(i_p_w, i_p_h)
        info_noti_para.resize(i_p_w, i_p_h)
        info_close_button.resize(i_c_b_w, i_c_b_h)
        label_list = window.findChildren(QLabel, "bar_")
        for label in label_list:
                label.setStyleSheet("background-color: rgba(255, 117, 0, 0.1);")
    else:
        pass

def close_info_menu():
    info_menu.resize(0, 0)
    info_menu_title.resize(0, 0)
    info_desc_para.resize(0, 0)
    info_instr_para.resize(0, 0)
    info_noti_para.resize(0, 0)
    info_close_button.resize(0, 0)
    label_list = window.findChildren(QLabel, "bar_")
    for label in label_list:
            label.setStyleSheet("background-color: rgba(255, 117, 0, 1);")

def open_upload_menu():
    if info_menu.height() == 0 and upload_menu.height() <= 1:
        upload_menu.resize(u_m_w, u_m_h)
        upl_menu_title.resize(u_m_t_w, u_m_t_h)
        upl_box.resize(u_b_w, u_b_h)
        upl_img.resize(u_i_w, u_i_h)
        upl_text.resize(u_t_w, u_t_h)
        upl_close_button.resize(u_bu_w, u_bu_h)
        upl_greyed_button.resize(u_bu_w, u_bu_h)
        label_list = window.findChildren(QLabel, "bar_")
        for label in label_list:
                label.setStyleSheet("background-color: rgba(255, 117, 0, 0.1);")
    else:
        pass

def close_upload_menu():
    upload_menu.resize(0, 0)
    upl_menu_title.resize(0, 0)
    upl_box.resize(0, 0)
    upl_img.resize(0, 0)
    upl_text.resize(0, 0)
    upl_close_button.resize(0, 0)
    upl_cont_button.resize(0, 0)
    upl_greyed_button.resize(0, 0)
    upl_file_box.resize(0, 0)
    upl_music_icon.resize(0, 0)
    upl_cancel_icon.resize(0, 0)
    upl_file_title.resize(0, 0)
    upl_file_subtitle.resize(0, 0)
    label_list = window.findChildren(QLabel, "bar_")
    for label in label_list:
            label.setStyleSheet("background-color: rgba(255, 117, 0, 1);")
    file_uploaded = False

def upload_audio():
    # Open a file dialog to select an image file
    global file_name
    file_name, a = QFileDialog.getOpenFileName(window, 'Open Image', '.', 'Image Files (*.mp3 *.wav *.aac *.flac)')
    if file_name:
            file_name_pathless = os.path.basename(file_name)
            artist, song = get_song_info(file_name_pathless)
            bytes_value = os.path.getsize(file_name)
            file_size = convert_bytes_to_megabytes(bytes_value)
            audio_length = get_audio_length(file_name)
            audio_length_min_sec = convert_seconds_to_minutes_seconds(audio_length)
            display_file(artist, song)

def drag_audio(file_name):
        file_name_pathless = os.path.basename(file_name)
        artist, song = get_song_info(file_name_pathless)
        bytes_value = os.path.getsize(file_name)
        file_size = convert_bytes_to_megabytes(bytes_value)
        audio_length = get_audio_length(file_name)
        audio_length_min_sec = convert_seconds_to_minutes_seconds(audio_length)
        display_file(artist, song)

def get_song_info(file_name):
    parts = file_name.split("-")
    if len(parts) >= 2:
        artist = parts[0].strip()  # Remove leading and trailing spaces
        song = parts[1].strip().rstrip(".mp3")      # Remove leading and trailing spaces
        if len(song) > 18:
            trimmed_song = song[:15] + "..."
        else:
            trimmed_song = song
        song = trimmed_song
        return artist, song
    else:
        # If the file name does not follow the expected format, return None for both song name and artist
        return None, None
    

def convert_bytes_to_megabytes(bytes_value):
    return bytes_value / (1024 * 1024)

def get_audio_length(file_name):
    try:
        audio = None
        if file_name.lower().endswith('.mp3'):
            audio = MP3(file_name)
        elif file_name.lower().endswith('.flac'):
            audio = FLAC(file_name)
        elif file_name.lower().endswith('.wav'):
            audio = WAVE(file_name)
        elif file_name.lower().endswith('.aac'):
            audio = AAC(file_name)

        if audio is not None:
            return audio.info.length
    except Exception as e:
        print("Error:", e)

    return 0.0
def convert_seconds_to_minutes_seconds(audio_length):
    minutes = int(audio_length // 60)
    remaining_seconds = int(audio_length % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def display_file(artist, song):
    upl_box.resize(0, 0)
    upl_img.resize(0, 0)
    upl_text.resize(0, 0)
    upl_greyed_button.resize(0, 0)
    upl_cont_button.resize(u_bu_w, u_bu_h)
    upl_file_box.resize(u_f_b_w, u_f_b_h)
    upl_music_icon.resize(u_m_i_w, u_m_i_h)
    upl_cancel_icon.resize(u_c_i_w, u_c_i_h)
    upl_file_title.resize(u_f_tx_w, u_f_t_h)
    upl_file_subtitle.resize(u_f_tx_w, u_f_st_h)
    upl_file_title.setText(song)
    upl_file_subtitle.setText(artist)
    file_uploaded = True

def cancel_display_file():
    upl_box.resize(u_b_w, u_b_h)
    upl_img.resize(u_i_w, u_i_h)
    upl_text.resize(u_t_w, u_t_h)
    upl_greyed_button.resize(u_bu_w, u_bu_h)
    upl_cont_button.resize(0, 0)
    upl_file_box.resize(0, 0)
    upl_music_icon.resize(0, 0)
    upl_cancel_icon.resize(0, 0)
    upl_file_title.resize(0, 0)
    upl_file_subtitle.resize(0, 0)
    file_uploaded = False

def drag_error():
    upl_box.resize(0, 0)
    upl_img.resize(0, 0)
    upl_text.resize(0, 0)
    error_message_box.resize(e_m_b_w, e_m_b_h)
    error_title.resize(e_t_w, e_t_h)
    error_text.resize(e_te_w, e_te_h)
    details_button.resize(e_b_w, e_b_h)
    okay_button.resize(e_b_w, e_b_h)

def close_error():
    upl_box.resize(u_b_w, u_b_h)
    upl_img.resize(u_i_w, u_i_h)
    upl_text.resize(u_t_w, u_t_h)
    error_message_box.resize(0, 0)
    error_title.resize(0, 0)
    error_text.resize(0, 0)
    details_button.resize(0, 0)
    okay_button.resize(0, 0)

def display_details():
    if error_message_box.height() < 150:
        error_details.resize(e_d_w, e_d_h)
        error_message_box.resize(e_m_b_w, 200)
        details_button.setText('Hide')
    else:
        error_details.resize(0, 0)
        error_message_box.resize(e_m_b_w, e_m_b_h)
        details_button.setText('Details...')

def finalise_upload():
    global selected_audio
    selected_audio = file_name
    file_name_pathless = os.path.basename(file_name)
    artist, song = get_song_info(file_name_pathless)
    song_name.setText(song)
    artist_name.setText(artist)

def play_audio():
    media_content = QMediaContent(QUrl.fromLocalFile(selected_audio))
    audio_player.setMedia(media_content)
    audio_player.play()

def start_loading():
    '''loading_bar.setFixedSize(l_b_dim, l_b_dim)
    quarter_w.resize(q_dim, q_dim)
    move_quarter.resize(q_dim, q_dim)'''
    loading_widget.resize(l_b_dim, l_b_dim)
    upl_file_box.resize(0, 0)
    upl_music_icon.resize(0, 0)
    upl_cancel_icon.resize(0, 0)
    upl_file_title.resize(0, 0)
    upl_file_subtitle.resize(0, 0)
    timer.start(100)  # Update every 200 milliseconds

def update_loading():
    global progress
    
    # print(progress)
    loading_widget.setProgress(progress)
    if  progress >= 60:
        progress = 0
        timer.stop()
        finalise_upload()
    progress += 1  # Update this value based on your needs
    


# keep GUI running
if __name__ == '__main__':
    # set up the GUI
    app = QApplication(sys.argv)
    # define the title, dimensions, 
    window = QWidget()
    window.setObjectName('window')
    window.resize(1920, 1080)
    # remove ugly white bar
    window.setWindowFlags(Qt.FramelessWindowHint)

    # create the new title bar
    title_bar = QLabel('', window)
    title_bar.setObjectName('custom_title_bar')
    title_bar.move(0, 0)
    title_bar_width = int(window.width()) - 108
    title_bar_height = 30
    title_bar.resize(title_bar_width, title_bar_height)
    # variable for title bar buttons placement
    title_button_loc = window.width() - 108
    # variable for the width of title bar buttons
    title_button_width = 36
    # add the minimise button
    mini_button = ClickableLabel(window)
    mini_button.setObjectName('mini_button')
    mini_button.move(title_button_loc, 0)
    mini_button.resize(title_button_width, title_bar_height)
    dash = QPixmap('images/subtract-line.png')
    dash_2 = dash.scaled(16, 16)
    mini_button.setPixmap(dash_2)
    mini_button.setAlignment(Qt.AlignCenter)
    mini_button.clicked.connect(window.showMinimized)
    # adjust the button location
    title_button_loc += 36
    # add the maximise button
    maxi_button = ClickableLabel(window)
    maxi_button.setObjectName('maxi_button')
    maxi_button.move(title_button_loc, 0)
    maxi_button.resize(title_button_width, title_bar_height)
    square = QPixmap('images/checkbox-blank-line-2.png')
    square_2 = square.scaled(13, 13)
    maxi_button.setPixmap(square_2)
    maxi_button.setAlignment(Qt.AlignCenter) 
    maxi_button.clicked.connect(maximised_mode)
    # adjust the button location
    title_button_loc += 36
    # add the close button
    close_button = ClickableLabel(window)
    close_button.setObjectName('close_button')
    close_button.move(title_button_loc, 0)
    close_button.resize(title_button_width, title_bar_height)
    cross = QPixmap('images/close-line.png')
    close_button.setPixmap(cross)
    close_button.setAlignment(Qt.AlignCenter)
    close_button.clicked.connect(window.close)

    # variables for button size and location
    # n_b = normal buttons, w/h is width/height
    n_b_w = 72
    n_b_h = 40
    n_b_y = 56
    settings_x = 56
    import_x = 144
    info_x = 232

    # add the settings button
    setting_button = ClickableLabel(window)
    setting_button.setObjectName('setting_button')
    setting_button.move(settings_x, n_b_y)
    setting_button.resize(n_b_w, n_b_h)
    gear = QPixmap('images/settings-4-line.png')
    gear_2 = gear.scaled(24,24)
    setting_button.setPixmap(gear_2)
    setting_button.setAlignment(Qt.AlignCenter)
    # setting_button.clicked.connect(window.close)
    setting_button.setToolTip('Settings')

    # add the import button
    import_button = ClickableLabel(window)
    import_button.setObjectName('import_button')
    import_button.move(import_x, n_b_y)
    import_button.resize(n_b_w, n_b_h)
    upload = QPixmap('images/upload-2-line.png')
    upload_2 = upload.scaled(24,24)
    import_button.setPixmap(upload_2)
    import_button.setAlignment(Qt.AlignCenter)
    import_button.setToolTip('Import')
    import_button.clicked.connect(open_upload_menu)

    # add the info button
    info_button = ClickableLabel(window)
    info_button.setObjectName('info_button')
    info_button.move(info_x, n_b_y)
    info_button.resize(n_b_w, n_b_h)
    upload = QPixmap('images/information-line.png')
    upload_2 = upload.scaled(24,24)
    info_button.setPixmap(upload_2)
    info_button.setAlignment(Qt.AlignCenter)
    info_button.clicked.connect(open_info_menu)
    info_button.setToolTip('Info & Help')

    # add the fullscreen button
    full_button = ClickableLabel(window)
    full_button.setObjectName('import_button')
    full_button_loc = window.width() - 128
    full_button.move(full_button_loc, n_b_y)
    full_button.resize(n_b_w, n_b_h)
    expand = QPixmap('images/fullscreen-line.png')
    expand_2 = expand.scaled(24,24)
    full_button.setPixmap(expand_2)
    full_button.setAlignment(Qt.AlignCenter)
    full_button.clicked.connect(fullscreen_mode)
    full_button.setToolTip('Fullscreen')

    # media player
    audio_player = QMediaPlayer(window)

    # add the three playback buttons
    lower_button_loc = window.height() - 98
    start_x = 842
    play_x = 924
    end_x = 1006
    # start button
    start_button = ClickableLabel(window)
    start_button.setObjectName('start_button')
    start_button.move(start_x, lower_button_loc)
    start_button.resize(n_b_w, n_b_h)
    start = QPixmap('images/skip-back-line.png')
    start_2 = start.scaled(24,24)
    start_button.setPixmap(start_2)
    start_button.setAlignment(Qt.AlignCenter)
    start_button.setToolTip('Start')
    # play button
    play_button = ClickableLabel(window)
    play_button.setObjectName('play_button')
    play_button.move(play_x, lower_button_loc)
    play_button.resize(n_b_w, n_b_h)
    play = QPixmap('images/play-line.png')
    play_2 = play.scaled(24,24)
    play_button.setPixmap(play_2)
    play_button.setAlignment(Qt.AlignCenter)
    play_button.setToolTip('Play')
    play_button.clicked.connect(play_audio)
    # end button
    end_button = ClickableLabel(window)
    end_button.setObjectName('end_button')
    end_button.move(end_x, lower_button_loc)
    end_button.resize(n_b_w, n_b_h)
    end = QPixmap('images/skip-forward-line.png')
    end_2 = end.scaled(24,24)
    end_button.setPixmap(end_2)
    end_button.setAlignment(Qt.AlignCenter)
    end_button.setToolTip('End')

    # add the placeholder paused visual
    bar_x = 656
    bar_y = 534
    bar_dimension = 12
    bar_gap = 32
    for i in range(1, 21):
        bar = QLabel(window)
        bar.setObjectName('bar_')
        bar.move(bar_x, bar_y)
        bar.resize(bar_dimension, bar_dimension)
        bar_x += bar_gap

    # add text on left hand side
    # variables
    song_x = 56
    song_y = 489
    song_w = 264
    song_h = 67
    artist_x = 56
    artist_y = 564
    artist_w = 110
    artist_h = 27
    song_name = QLabel('Song name', window)
    song_name.setObjectName('song_name')
    song_name.move(song_x, song_y)
    song_name.resize(song_w, song_h)
    artist_name = QLabel('Artist name', window)
    artist_name.setObjectName('artist_name')
    artist_name.move(artist_x, artist_y)
    artist_name.resize(artist_w, artist_h)

    # the menus
    # info menu
    # variables of scaled menu
    '''
    to make names shorter these are the conventions:
    i_m = info menu
    _w = width
    _h = height
    _p_ = identifier for a specific component, such as paragraph
    '''
    i_m_w = 664
    i_m_h = 694
    i_m_t_w = 361
    i_m_t_h = 53
    i_p_w = 624
    i_p_h = 140
    i_c_b_w = 242
    i_c_b_h = 40
    i_m_x = 635
    i_m_y = 186
    i_m_t_x = 787
    i_m_t_y = 236
    i_d_p_x = 710
    i_d_p_y = 309
    i_i_p_x = 710
    i_i_p_y = 469
    i_n_p_x = 710
    i_n_p_y = 589
    i_c_b_x = 836
    i_c_b_y = 790

    # menu components
    info_menu = QLabel('', window)
    info_menu.setObjectName('info_menu')
    info_menu.move(i_m_x, i_m_y)    
    info_menu.resize(0, 0)

    info_menu_title = QLabel('Welcome to OA/SV', window)
    info_menu_title.setObjectName('info_menu_title')
    info_menu_title.move(i_m_t_x, i_m_t_y)
    info_menu_title.resize(0, 0)
    
    info_desc_para = QLabel('Odams Audio/Sound Visualiser is an app which takes'
                            '\nthe sound and music you love, and visualises it a'
                            '\nmodern and exciting way. It is complete with user'
                            '\nfriendliness in mind, so give it a go and play your'
                            '\nfavourite song today.', window)
    info_desc_para.setObjectName('info_paras')
    info_desc_para.move(i_d_p_x, i_d_p_y)
    info_desc_para.resize(0, 0)

    info_instr_para = QLabel('Instructions:'
                            '\n1. Select the import button, near settings'
                            '\n2. Drag in an audio file or upload an audio file'
                            '\n3. Allow the program to process the audio file'
                            '\n4. Once it\'s done, press play', window)
    info_instr_para.setObjectName('info_paras')
    info_instr_para.move(i_i_p_x, i_i_p_y)
    info_instr_para.resize(0, 0)

    info_noti_para = QLabel('You can access this menu again at any time by'
                            '\npressing the "i" icon in the top left corner'
                            , window)
    info_noti_para.setObjectName('info_paras')
    info_noti_para.move(i_n_p_x, i_n_p_y)
    info_noti_para.resize(0, 0)

    info_close_button = ClickableLabel(window)
    info_close_button.setText('Close')
    info_close_button.setObjectName('info_close_button')
    info_close_button.move(836, 790)
    info_close_button.resize(0, 0)
    info_close_button.setAlignment(Qt.AlignCenter)
    info_close_button.clicked.connect(close_info_menu)
    info_close_button.setToolTip('Close')

    # upload components
    # numbers
    u_m_x = 629
    u_m_y = 194
    u_m_w = 663
    u_m_h = 693
    u_m_t_x = 853
    u_m_t_y = 237
    u_m_t_w = 215
    u_m_t_h = 53
    u_b_x = 700
    u_b_y = 350
    u_b_w = 520
    u_b_h = 380
    u_i_x = 906
    u_i_y = 458
    u_i_w = 109
    u_i_h = 99
    u_t_x = 765
    u_t_y = 585
    u_t_w = 390
    u_t_h = 37
    u_cl_b_x = 679
    u_bu_y = 790
    u_bu_w = 262
    u_bu_h = 40
    u_co_b_x = 980

    upload_menu = QLabel('', window)
    upload_menu.setObjectName('upload_menu')
    upload_menu.move(u_m_x, u_m_y)    
    upload_menu.resize(0, 0)

    upl_menu_title = QLabel('Select a file', window)
    upl_menu_title.setObjectName('upl_menu_title')
    upl_menu_title.move(u_m_t_x, u_m_t_y)
    upl_menu_title.resize(0, 0)

    upl_box = UploadBox(window)
    upl_box.setObjectName('upl_box')
    upl_box.move(u_b_x, u_b_y)
    upl_box.resize(0, 0)
    upl_box.clicked.connect(upload_audio)

    upl_img = QLabel('', window)
    upload_icon = QPixmap('images/upload-line.png')
    upload_icon_2 = upload_icon.scaled(109,99)
    upl_img.setPixmap(upload_icon_2)
    upl_img.setAlignment(Qt.AlignCenter)
    upl_img.setObjectName('upl_img')
    upl_img.move(u_i_x, u_i_y)
    upl_img.resize(0, 0)
    
    upl_text = QLabel('Drag file here or click to upload', window)
    upl_text.setObjectName('upl_text')
    upl_text.move(u_t_x, u_t_y)
    upl_text.resize(0, 0)
    
    upl_close_button = ClickableLabel(window)
    upl_close_button.setObjectName('upl_close_button')
    upl_close_button.setText('Close')
    upl_close_button.move(u_cl_b_x, u_bu_y)
    upl_close_button.setAlignment(Qt.AlignCenter)
    upl_close_button.resize(0, 0)
    upl_close_button.clicked.connect(close_upload_menu)

    upl_greyed_button = QLabel('Continue', window)
    upl_greyed_button.setObjectName('upl_greyed_button')
    upl_greyed_button.setAlignment(Qt.AlignCenter)
    upl_greyed_button.move(u_co_b_x, u_bu_y)
    upl_greyed_button.resize(0, 0)

    upl_cont_button = SpecialClickableLabel(window)
    upl_cont_button.setObjectName('upl_cont_button')
    upl_cont_button.setText('Continue')
    upl_cont_button.setAlignment(Qt.AlignCenter)
    upl_cont_button.move(u_co_b_x, u_bu_y)
    upl_cont_button.resize(0, 0)
    upl_cont_button.clicked.connect(start_loading)

    u_f_b_x = 700
    u_f_b_y = 490
    u_f_b_w = 520
    u_f_b_h = 100
    u_m_i_x = 724
    u_m_i_y = 523
    u_m_i_w = 34
    u_m_i_h = 34
    u_c_i_x = 1164
    u_c_i_y = 520
    u_c_i_w = 40
    u_c_i_h = 40
    u_f_t_x = 772
    u_f_t_y = 506
    u_f_tx_w = 300
    u_f_t_h = 40
    u_f_st_x = 772
    u_f_st_y = 539
    u_f_st_h = 27


    upl_file_box = QLabel(window)
    upl_file_box.setObjectName('upl_file_box')
    upl_file_box.move(u_f_b_x, u_f_b_y)
    upl_file_box.resize(0, 0)

    upl_music_icon = QLabel('', window)
    music_icon = QPixmap('images/music-2-line.png')
    music_icon_2 = music_icon.scaled(32,32)
    upl_music_icon.setPixmap(music_icon_2)
    upl_music_icon.setAlignment(Qt.AlignCenter)
    upl_music_icon.setObjectName('upl_icon')
    upl_music_icon.move(u_m_i_x, u_m_i_y)
    upl_music_icon.resize(0, 0)

    upl_cancel_icon = ClickableLabel(window)
    cancel_icon = QPixmap('images/close-circle-line.png')
    cancel_icon_2 = cancel_icon.scaled(32,32)
    upl_cancel_icon.setPixmap(cancel_icon_2)
    upl_cancel_icon.setAlignment(Qt.AlignCenter)
    upl_cancel_icon.setObjectName('upl_cancel_icon')
    upl_cancel_icon.move(u_c_i_x, u_c_i_y)
    upl_cancel_icon.resize(0, 0)
    upl_cancel_icon.clicked.connect(cancel_display_file)

    upl_file_title = QLabel('Song Name', window)
    upl_file_title.setObjectName('upl_file_title')
    upl_file_title.move(u_f_t_x, u_f_t_y)
    upl_file_title.resize(0, 0)
    upl_file_title.setAlignment(Qt.AlignLeft)

    upl_file_subtitle = QLabel('Artist Name', window)
    upl_file_subtitle.setObjectName('upl_file_subtitle')
    upl_file_subtitle.move(u_f_st_x, u_f_st_y)
    upl_file_subtitle.resize(0, 0)
    upl_file_title.setAlignment(Qt.AlignLeft)

    detailed_text = ('The details are as follows:'
                    '\nThe file type uploaded is not'
                    '\ncompatible with the program,'
                    '\nmake sure it is a common'
                    '\naudio format and try again.')
    e_m_b_x = 860
    e_m_b_y = 484
    e_m_b_w = 200
    e_m_b_h = 111
    e_t_x = 925
    e_t_y = 486
    e_t_w = 70
    e_t_h = 40
    e_te_x = 890
    e_te_y = 528
    e_te_w = 140
    e_te_h = 27
    d_b_x = 868 
    o_b_x = 962
    e_b_w = 90
    e_b_h = 24
    e_b_y = 563
    e_d_x = 865
    e_d_y = 593
    e_d_w = 190
    e_d_h = 86
    
    error_message_box = QLabel('', window)
    error_message_box.setObjectName('error_message_box')
    error_message_box.move(e_m_b_x, e_m_b_y)
    error_message_box.resize(0, 0)

    error_title = QLabel('Error', window)
    error_title.setObjectName('error_title')
    error_title.move(e_t_x, e_t_y)
    error_title.resize(0, 0)

    error_text = QLabel('Invalid File Type', window)
    error_text.setObjectName('error_text')
    error_text.move(e_te_x, e_te_y)
    error_text.resize(0, 0)

    details_button = ClickableLabel(window)
    details_button.setObjectName('details_button')
    details_button.move(d_b_x, e_b_y)
    details_button.resize(0, 0)
    details_button.setText('Details...')
    details_button.setAlignment(Qt.AlignCenter)
    details_button.clicked.connect(display_details)

    okay_button = SpecialClickableLabel(window)
    okay_button.setObjectName('okay_button')
    okay_button.move(o_b_x, e_b_y)
    okay_button.resize(0, 0)
    okay_button.setText('Okay')
    okay_button.setAlignment(Qt.AlignCenter)
    okay_button.clicked.connect(close_error)

    error_details = QLabel(detailed_text, window)
    error_details.setObjectName('error_details')
    error_details.move(e_d_x, e_d_y)
    error_details.resize(0, 0)
    error_details.setAlignment(Qt.AlignCenter)

    l_b_dim = 350
    l_b_x = 785
    l_b_y = 365

    loading_widget = LoadingBarWidget(window)
    loading_widget.move(l_b_x, l_b_y)
    loading_widget.resize(0, 0)

    '''loading_bar = QProgressBar(window)
    loading_bar.setObjectName('loading_bar')
    loading_bar.move(0, 0)
    loading_bar.resize(0, 0)'''
    

    '''loading_bar = QLabel(window)
    loading_bar.setObjectName('loading_bar')
    loading_bar.move(l_b_x, l_b_y)
    loading_bar.resize(0, 0)
    white_ring = QPixmap('images/loading-ring.png')
    loading_bar.setPixmap(white_ring)

    test_run = 0

    q_dim = 175
    q_x_l = 785
    q_x_r = 960
    q_y_t = 365
    q_y_b = 540
    rotate_90 = 90
    rotate_180 = 180
    rotate_270 = 270
    changing_rotation = 270
    transform_90 = QTransform()
    transform_90.rotate(rotate_90, Qt.ZAxis)
    transform_180 = QTransform()
    transform_180.rotate(rotate_180, Qt.ZAxis)
    transform_270 = QTransform()
    transform_270.rotate(rotate_270, Qt.ZAxis)

    orange_ring = QPixmap('images/loading-ring-segment-orange.png')
    orange_ring_90 = orange_ring.transformed(transform_90)
    orange_ring_180 = orange_ring.transformed(transform_180)
    orange_ring_270 = orange_ring.transformed(transform_270)
    white_segment = QPixmap('images/loading-ring-segment-white.png')
    white_quarter = white_segment.transformed(transform_270)

    m_x_l = 785
    m_y_t = 365
    move_quarter = QLabel(window)
    move_quarter.move(m_x_l, m_y_t)
    move_quarter.resize(0, 0)
    
    quarter_1 = QLabel(window)
    quarter_1.move(q_x_r, q_y_t)
    quarter_1.resize(0, 0)
    quarter_1.setPixmap(orange_ring)

    quarter_2 = QLabel(window)
    quarter_2.move(q_x_r, q_y_b)
    quarter_2.resize(0, 0)
    quarter_2.setPixmap(orange_ring_90)

    quarter_3 = QLabel(window)
    quarter_3.move(q_x_l, q_y_b)
    quarter_3.resize(0, 0)
    quarter_3.setPixmap(orange_ring_180) 

    quarter_4 = QLabel(window)
    quarter_4.move(q_x_l, q_y_t)
    quarter_4.resize(0, 0)
    quarter_4.setPixmap(orange_ring_270) 

    quarter_w = QLabel(window)
    quarter_w.move(q_x_l, q_y_t)
    quarter_w.resize(0, 0)
    quarter_w.setPixmap(white_quarter)'''

    timer = QTimer()
    timer.timeout.connect(update_loading)

    # Load the external stylesheet
    with open('sheets/stylesheet.qss', 'r') as file:
        stylesheet = file.read()
    # Set the stylesheet
    app.setStyleSheet(stylesheet)
    # show all the widgets in the window
    window.show()
    # set to max size
    window.showMaximized()
    # open help/instructions
    open_info_menu()
    # run the program
    sys.exit(app.exec_())