# method 1
'''try:
        global k, l, bar_x
        bar_y = 534
        bar_gap = 32
        label_list = window.findChildren(QLabel, "bar_")
        amplitude_data = amplitude_values[k]
        scaled_height = 12 + (amplitude_data * 400)
        scaled_height = int(scaled_height)
        bar_y = 534 - (scaled_height/2)
        label_list[l].move(bar_x, int(bar_y))
        label_list[l].setFixedHeight(scaled_height)
        bar_x += bar_gap
        k += 1
        l += 1
        if l == 20:
            l = 0
            bar_x = 656
    except IndexError:
        audio_timer.stop()'''
# method 1.5
'''
    try:
        global k, l, bar_x, scaled_height, numer
        bar_y = 540
        bar_gap = 32
        label_list = window.findChildren(QLabel, "bar_")
        # height_from = label_list[0].height()
        numer = 0
        for label in label_list:
            print(label_list[numer].height())
            if label == label_list[0]:
                print('label_1')
            else:
                print(numer, ' ', label_list[numer].height())
                bar_x += bar_gap
                label.setFixedHeight(label_list[numer].height())
                bar_y = 540 - (label_list[numer].height()/2)
                label.move(bar_x, int(bar_y))
                numer += 1
        try:            
            if label_list[l] == label_list[0]:
                pass
            else:
                print(k)
                # print(numer)
                print(l)
                bar_x = label_list[l-1].x() + 32
                amplitude_data = amplitude_values[k-1]
                if k-numer < 0:
                    pass
                else:
                    scaled_height = 12 + (amplitude_data * 400)
                    scaled_height = int(scaled_height)
                    bar_y = 540 - (scaled_height/2)
                    label_list[l].move(bar_x, int(bar_y))
                    label_list[l].setFixedHeight(scaled_height)
        except Exception as e:
            print(e)
            print('what')
'''
# method 3
'''
    global k, l, bar_x, scaled_height, numer, tumour
    try:
        bar_y = 540
        bar_gap = 32
        label_list = window.findChildren(QLabel, "bar_")
        l = 0
        numer = 0
        bar_x = 656
        for i in range(0, tumour):
            amplitude_data = amplitude_envelopes[k-numer]
            scaled_height = 12 + (amplitude_data * 400)
            scaled_height = int(scaled_height)
            bar_y = 540 - (scaled_height/2)
            label_list[l].move(bar_x, int(bar_y))
            label_list[l].setFixedHeight(scaled_height)
            bar_x += bar_gap
            l += 1
            numer += 1

        if tumour != 20:
            tumour += 1    
        k += 1
        if l == 20:
            l = 0
            bar_x = 656
    except IndexError:
        print('what')
        audio_timer.stop()'''
# envelopes method
'''
        global selected_audio
        file_path = selected_audio
        
        global amplitude_envelopes
        interval_ms = interval
        try:
            if audio_analyzer_thread and audio_analyzer_thread.is_alive():
                    return
        except UnboundLocalError:
            pass
        # Load the audio file
        y, sr = librosa.load(file_path)

        # Calculate the number of samples in each interval
        interval_samples = int((interval_ms / 1000) * sr)

        # Calculate the number of intervals
        num_intervals = len(y) // interval_samples

        # Initialize a list to store amplitude envelope values
        amplitude_envelopes = []

        # Rectify the audio signal (convert negative values to positive)
        y_rectified = numpy.abs(y)

        # Apply a low-pass filter to smooth the envelope (optional)
        # Adjust the filter parameters as needed
        cutoff_frequency = 10.0  # Adjust this value as needed
        filter_order = 3  # Adjust this value as needed
        b, a = scipy.signal.butter(filter_order, cutoff_frequency / (0.5 * sr), 'low')
        y_smoothed = scipy.signal.filtfilt(b, a, y_rectified)

        # Iterate over intervals and calculate the amplitude envelope for each
        for i in range(num_intervals):
            start_sample = i * interval_samples
            end_sample = (i + 1) * interval_samples
            interval_amplitude = numpy.max(y_smoothed[start_sample:end_sample])
            amplitude_envelopes.append(interval_amplitude)'''