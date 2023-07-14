import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# make labels clickable with this class
class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)

# define the functions that are part of the program
first_run = True
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
        title_bar.resize(title_bar_width, 30)
        mini_button.resize(36, 30)
        maxi_button.resize(36, 30)
        close_button.resize(36, 30)
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
    info_menu.resize(664, 694)
    info_menu_title.resize(361, 53)
    info_desc_para.resize(624, 140)
    info_instr_para.resize(624, 140)
    info_noti_para.resize(624, 140)
    info_close_button.resize(242, 40)
    label_list = window.findChildren(QLabel, "bar_")
    for label in label_list:
            label.setStyleSheet("background-color: rgba(255, 117, 0, 0.1);")

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
    title_bar.resize(title_bar_width, 30)
    # variable for title bar buttons placement
    title_button_loc = window.width() - 108
    # add the minimise button
    mini_button = ClickableLabel(window)
    mini_button.setObjectName('mini_button')
    mini_button.move(title_button_loc, 0)
    mini_button.resize(36, 30)
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
    maxi_button.resize(36, 30)
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
    close_button.resize(36, 30)
    cross = QPixmap('images/close-line.png')
    close_button.setPixmap(cross)
    close_button.setAlignment(Qt.AlignCenter)
    close_button.clicked.connect(window.close)

    # add the settings button
    setting_button = ClickableLabel(window)
    setting_button.setObjectName('setting_button')
    setting_button.move(56, 56)
    setting_button.resize(72, 40)
    gear = QPixmap('images/settings-4-line.png')
    gear_2 = gear.scaled(24,24)
    setting_button.setPixmap(gear_2)
    setting_button.setAlignment(Qt.AlignCenter)
    # setting_button.clicked.connect(window.close)

    # add the import button
    import_button = ClickableLabel(window)
    import_button.setObjectName('import_button')
    import_button.move(144, 56)
    import_button.resize(72, 40)
    upload = QPixmap('images/upload-2-line.png')
    upload_2 = upload.scaled(24,24)
    import_button.setPixmap(upload_2)
    import_button.setAlignment(Qt.AlignCenter)

    # add the info button
    info_button = ClickableLabel(window)
    info_button.setObjectName('info_button')
    info_button.move(232, 56)
    info_button.resize(72, 40)
    upload = QPixmap('images/information-line.png')
    upload_2 = upload.scaled(24,24)
    info_button.setPixmap(upload_2)
    info_button.setAlignment(Qt.AlignCenter)
    info_button.clicked.connect(open_info_menu)

    # add the fullscreen button
    full_button = ClickableLabel(window)
    full_button.setObjectName('import_button')
    full_button_loc = window.width() - 128
    full_button.move(full_button_loc, 56)
    full_button.resize(72, 40)
    expand = QPixmap('images/fullscreen-line.png')
    expand_2 = expand.scaled(24,24)
    full_button.setPixmap(expand_2)
    full_button.setAlignment(Qt.AlignCenter)
    full_button.clicked.connect(fullscreen_mode)

    # add the three playback buttons
    lower_button_loc = window.height() - 98
    # start button
    start_button = ClickableLabel(window)
    start_button.setObjectName('start_button')
    start_button.move(842, lower_button_loc)
    start_button.resize(72, 40)
    start = QPixmap('images/skip-back-line.png')
    start_2 = start.scaled(24,24)
    start_button.setPixmap(start_2)
    start_button.setAlignment(Qt.AlignCenter)
    # play button
    play_button = ClickableLabel(window)
    play_button.setObjectName('play_button')
    play_button.move(924, lower_button_loc)
    play_button.resize(72, 40)
    play = QPixmap('images/play-line.png')
    play_2 = play.scaled(24,24)
    play_button.setPixmap(play_2)
    play_button.setAlignment(Qt.AlignCenter)
    # end button
    end_button = ClickableLabel(window)
    end_button.setObjectName('end_button')
    end_button.move(1006, lower_button_loc)
    end_button.resize(72, 40)
    end = QPixmap('images/skip-forward-line.png')
    end_2 = end.scaled(24,24)
    end_button.setPixmap(end_2)
    end_button.setAlignment(Qt.AlignCenter)

    # add the placeholder paused visual
    bar_loc = 656
    for i in range(1, 21):
        bar = QLabel(window)
        bar.setObjectName('bar_')
        bar.move(bar_loc, 534)
        bar.resize(12, 12)
        bar_loc += 32

    # add text on left hand side
    song_name = QLabel('Song name', window)
    song_name.setObjectName('song_name')
    song_name.move(56, 489)
    song_name.resize(264, 67)
    artist_name = QLabel('Artist name', window)
    artist_name.setObjectName('artist_name')
    artist_name.move(56, 564)
    artist_name.resize(110, 27)

    # the menus
    # info menu
    info_menu = QLabel('', window)
    info_menu.setObjectName('info_menu')
    info_menu.move(628, 186)    
    info_menu.resize(0, 0)

    info_menu_title = QLabel('Welcome to OA/SV', window)
    info_menu_title.setObjectName('info_menu_title')
    info_menu_title.move(780, 236)
    info_menu_title.resize(0, 0)
    
    info_desc_para = QLabel('Odams Audio/Sound Visualiser is an app which takes'
                            '\nthe sound and music you love, and visualises it a'
                            '\nmodern and exciting way. It is complete with user'
                            '\nfriendliness in mind, so give it a go and play your'
                            '\nfavourite song today.', window)
    info_desc_para.setObjectName('info_paras')
    info_desc_para.move(703, 309)
    info_desc_para.resize(0, 0)

    info_instr_para = QLabel('Instructions:'
                            '\n1. Select the import button, near settings'
                            '\n2. Drag in an audio file or upload an audio file'
                            '\n3. Allow the program to process the audio file'
                            '\n4. Once it\'s done, press play', window)
    info_instr_para.setObjectName('info_paras')
    info_instr_para.move(703, 469)
    info_instr_para.resize(0, 0)

    info_noti_para = QLabel('You can access this menu again at any time by'
                            '\npressing the "i" icon in the top left corner'
                            , window)
    info_noti_para.setObjectName('info_paras')
    info_noti_para.move(703, 589)
    info_noti_para.resize(0, 0)

    info_close_button = ClickableLabel('Close', window)
    info_close_button.setObjectName('info_close_button')
    info_close_button.move(829, 790)
    info_close_button.resize(0, 0)
    info_close_button.setAlignment(Qt.AlignCenter)
    info_close_button.clicked.connect(close_info_menu)

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