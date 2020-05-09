import re
import PySimpleGUI as sg

from convert_to_gif import gif_converter

split_line_size = 72
start_time_size = (3, 1)
num_themes = 3

# Create Different Layout Themes
layouts = []
for i in range(num_themes):
    if i == 0:
        sg.theme('DarkTeal2')
    elif i == 1:
        sg.theme('DarkPurple')
    elif i == 2:
        sg.theme('LightBrown3')
    # ---------------------- Start Time Colum ---------------------- #
    column_st = [
        [sg.Text('Start Time (H:M:S)', justification='left', size=(15, 1))],
        [sg.Spin(values=list(range(100)), initial_value=0,
                 size=start_time_size, key='-HH-'),
         sg.Text('Hour')],
        [sg.Spin(values=list(range(100)), initial_value=0,
                 size=start_time_size, key='-MM-'),
         sg.Text('Minute')],
        [sg.Spin(values=list(range(100)), initial_value=0,
                 size=start_time_size, key='-SS-'),
         sg.Text('Second')],
    ]
    # ---------------------- Duration Colum ---------------------- #
    column_dur = [
        [sg.Text('Duration (s)', justification='left', size=(9, 1))],
        [sg.Slider(range=(1, 10), orientation='v', size=(3, 20), default_value=5,
                   enable_events=True, key='-Duration-Slider-')],
    ]

    # ---------------------- Window Layout ---------------------- #
    layout = [
        # ---------------------- File Bowser ---------------------- #
        [sg.Text('Please Choose A File (Video or Gif)', size=(35, 1))],
        [
            sg.Text('Your File', size=(13, 1),
                    auto_size_text=False, justification='right'),
            sg.InputText('File Path', key='-File-Path-'),
            sg.FileBrowse(key='-Browser-' + str(i)),
        ],
        [sg.Text('_' * split_line_size)],

        # ---------------------- Setup ---------------------- #
        [sg.Text('Setup Arguments', size=(35, 1))],
        [   # Input setting
            sg.Frame('Set Start Time and Duration', [[
                sg.Column(column_st),
                sg.Column(column_dur),
            ]]),
            # Output setting
            sg.Frame('Resolution FPS and FileName', [
                [
                    sg.Text('Width:', justification='left'),
                    sg.InputOptionMenu(
                        ('240', '320', '480', '640', '800'), default_value='320', key='-Resolution-'),
                    sg.Text('Frames: 50', size=(10, 1),
                            justification='left', key='-Frames-')
                ],
                [sg.Slider(range=(5, 60), default_value=10, orientation='h', size=(25, 20),
                           enable_events=True, key='-FPS-Slider-')],
                [
                    sg.Text('Output dir:'),
                    sg.InputText(default_text='Output Path',
                                 size=(12, 1), key='-Out-Path-'),
                    sg.FolderBrowse(key='-Out-Browse-' + str(i)),
                ]
            ]),
        ],

        # ---------------------- Theme ---------------------- #
        [sg.Text('Change Theme')],
        [
            sg.Radio('DarkTeal2', "THEME-RADIO",
                     default=(i == 0), enable_events=True, key='-Theme-0-'),
            sg.Radio('DarkPurple', "THEME-RADIO",
                     default=(i == 1), enable_events=True, key='-Theme-1-'),
            sg.Radio('LightBrown3', "THEME-RADIO",
                     default=(i == 2), enable_events=True, key='-Theme-2-'),
        ],
        [sg.Text('_' * split_line_size)],

        # ---------------------- Conver or Cancel ---------------------- #
        [
            sg.Text(size=(50, 1), auto_size_text=False,
                    justification='right', key='-Output-'),
            sg.Button('Convert', key='-Convert-' + str(i)),
            sg.Button('Cancel', key='-Cancel-' + str(i)),
        ],
    ]
    layouts.append(layout)

# Create Different Window Themes
windows = []
for i in range(num_themes):
    if i == 0:
        sg.theme('DarkTeal2')
    elif i == 1:
        sg.theme('DarkPurple')
    elif i == 2:
        sg.theme('LightBrown3')

    window = sg.Window('Tiny GIF Converter', layouts[i],
                       default_element_size=(40, 1), grab_anywhere=False)
    windows.append(window)

start_convert = False
first_pass = [True, True]
win_activ = [True, False, False]
# Event Loop to process "events" and get the "values" of the inputs
while True:
    if win_activ[0]:
        event, values = windows[0].read()
    elif win_activ[1]:
        event, values = windows[1].read()
    elif win_activ[2]:
        event, values = windows[2].read()

    # print(event)
    if event == '-Theme-0-':  # Theme 0 is selected
        # Active selected window
        windows[0].UnHide()
        win_activ[0] = True
        windows[0]['-Theme-0-'].update(win_activ[0])
        # Hide other windows
        if win_activ[1]:
            windows[1].Hide()
            win_activ[1] = False
        elif win_activ[2]:
            windows[2].Hide()
            win_activ[2] = False

    elif event == '-Theme-1-':  # Theme 1 is selected
        # Active selected window
        win_activ[1] = True
        if first_pass[0]:
            first_pass[0] = False
        else:
            windows[1].UnHide()
            windows[1]['-Theme-1-'].update(win_activ[1])
        # Hide other windows
        if win_activ[0]:
            windows[0].Hide()
            win_activ[0] = False
        elif win_activ[2]:
            windows[2].Hide()
            win_activ[2] = False

    elif event == '-Theme-2-':  # Theme 2 is selected
        # Active selected window
        win_activ[2] = True
        if first_pass[1]:
            first_pass[1] = False
        else:
            windows[2].UnHide()
            windows[2]['-Theme-2-'].update(win_activ[2])
        # Hide other windows
        if win_activ[0]:
            windows[0].Hide()
            win_activ[0] = False
        elif win_activ[1]:
            windows[1].Hide()
            win_activ[1] = False

    # If user closes window or clicks cancel
    elif event in (None, '-Cancel-0', '-Cancel-1', '-Cancel-2'):
        break

    elif event in ('-FPS-Slider-', '-Duration-Slider-'):
        num_frames = int(values['-FPS-Slider-'] * values['-Duration-Slider-'])
        act_window_idx = win_activ.index(True)
        windows[act_window_idx]['-Frames-'].update(
            'Frames: ' + str(num_frames))

    elif event in ('-Convert-0', '-Convert-1', '-Convert-2'):  # Setup for converting

        if values['-File-Path-'] == 'File Path':
            load_path = None
        else:
            load_path = values['-File-Path-']

        if values['-Out-Path-'] == 'Output Path':
            save_path = None
        else:
            save_path = values['-Out-Path-']

        start_time = str(values['-HH-']) + ':' + \
            str(values['-MM-']) + ':' + str(values['-SS-'])
        fps = int(values['-FPS-Slider-'])
        frame_size = values['-Resolution-']

        start_convert = True
        break

for window in windows:
    window.close()


if start_convert:
    act_window_idx = win_activ.index(True)
    if act_window_idx == 0:
        sg.theme('DarkTeal2')
    elif act_window_idx == 1:
        sg.theme('DarkPurple')
    elif act_window_idx == 2:
        sg.theme('LightBrown3')

    # Layout the processing window
    num_frames = values['-Duration-Slider-'] * values['-FPS-Slider-']
    num_frames = int(num_frames)
    layout = [[sg.Text('ETA: ', size=(10, 1), justification='left', key='-ETA-')],
              [sg.ProgressBar(num_frames, orientation='h',
                              size=(20, 20), key='-PROGBAR-'),
               sg.Text('0%', size=(5, 1), key='-PERCENT-')],
              [sg.Cancel()]]

    # Create the processing window
    window = sg.Window('Processing...', layout)

    # Converting
    cancelled = False
    for msg in gif_converter(
        load_path=load_path,
        save_path=save_path,
        start_time=start_time,
        duration=str(values['-Duration-Slider-']),
        fps=str(fps),
        frame_width=frame_size,
    ):
        event, values = window.read(timeout=0)

        if event == 'Cancel' or event is None:
            cancelled = True
            break

        print(msg)
        data = re.findall(r"\d+\d*", msg)
        if len(data) == 3:
            window['-PROGBAR-'].update_bar(int(data[0]))
            window['-ETA-'].update('ETA: ' + data[-1] + ' s')
            window['-PERCENT-'].update(str(100 *
                                           int(data[0]) / num_frames) + '%')
    window.close()

    # Popup finish message
    if not cancelled:
        if save_path is None:
            save_path = 'default path'
        sg.popup(
            'Finish!',
            'The converted file is saved at {}.'.format(save_path),
        )
