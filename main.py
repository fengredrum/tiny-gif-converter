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
            sg.FileBrowse(),
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
                    sg.Text('Res:', justification='left'),
                    sg.InputOptionMenu(
                        ('320x240', '640x480', '800x600'), key='-Resolution-'),
                    sg.Text('Frames: 50', size=(10, 1),
                            justification='left', key='-Frames-')
                ],
                [sg.Slider(range=(5, 60), default_value=10, orientation='h', size=(25, 20),
                           enable_events=True, key='-FPS-Slider-')],
                [
                    sg.Text('Output dir:'),
                    sg.InputText(default_text='Output Path',
                                 size=(12, 1), key='-Out-Path-'),
                    sg.FolderBrowse(key='-Out-Browse-'),
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
            sg.Button('Convert'),
            sg.Button('Cancel'),
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

first_pass_1 = first_pass_2 = win_activ_0 = True
win_activ_1 = win_activ_2 = not win_activ_0
# Event Loop to process "events" and get the "values" of the inputs
while True:
    if win_activ_0:
        event, values = windows[0].read()
    elif win_activ_1:
        event, values = windows[1].read()
    elif win_activ_2:
        event, values = windows[2].read()

    if event == '-Theme-0-':  # Theme 0 is selected
        # Active selected window
        windows[0].UnHide()
        win_activ_0 = True
        windows[0]['-Theme-0-'].update(win_activ_0)
        # Hide other windows
        if win_activ_1:
            windows[1].Hide()
            win_activ_1 = False
        elif win_activ_2:
            windows[2].Hide()
            win_activ_2 = False

    elif event == '-Theme-1-':  # Theme 1 is selected
        # Active selected window
        win_activ_1 = True
        if first_pass_1:
            first_pass_1 = False
        else:
            windows[1].UnHide()
            windows[1]['-Theme-1-'].update(win_activ_1)
        # Hide other windows
        if win_activ_0:
            windows[0].Hide()
            win_activ_0 = False
        elif win_activ_2:
            windows[2].Hide()
            win_activ_2 = False

    elif event == '-Theme-2-':  # Theme 2 is selected
        # Active selected window
        win_activ_2 = True
        if first_pass_2:
            first_pass_2 = False
        else:
            windows[2].UnHide()
            windows[2]['-Theme-2-'].update(win_activ_2)
        # Hide other windows
        if win_activ_0:
            windows[0].Hide()
            win_activ_0 = False
        elif win_activ_1:
            windows[1].Hide()
            win_activ_1 = False

    elif event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

    elif event in ('-FPS-Slider-', '-Duration-Slider-'):
        fps = int(values['-FPS-Slider-'] * values['-Duration-Slider-'])
        window['-Frames-'].update('Frames: ' + str(fps))

    elif event == 'Convert':  # Start converting
        window['-Output-'].update('Processing...')

        # Setting
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

        # Converting
        if gif_converter(
                load_path=load_path,
                save_path=save_path,
                start_time=start_time,
                duration=str(values['-Duration-Slider-']),
                fps=str(fps),
                frame_size=frame_size,
        ) == 'Done':
            break


window.close()

if save_path is None:
    save_path = 'default path'

sg.popup(
    'Finish',
    'The converted file is saved at {}.'.format(save_path),
)
