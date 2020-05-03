import PySimpleGUI as sg

from convert_to_gif import gif_converter

sg.theme('DarkTeal2')

split_line_size = 68
start_time_size = (3, 1)

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
    [sg.Text('_' * split_line_size)],

    # ---------------------- Conver or Cancel ---------------------- #
    [
        sg.Text(size=(46, 1), auto_size_text=False,
                justification='right', key='-Output-'),
        sg.Button('Convert'),
        sg.Button('Cancel'),
    ],
]

# ---------------------- Create Window ---------------------- #
window = sg.Window('Tiny GIF Converter', layout,
                   default_element_size=(40, 1), grab_anywhere=False)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event in ('-FPS-Slider-', '-Duration-Slider-'):
        fps = int(values['-FPS-Slider-'] * values['-Duration-Slider-'])
        window['-Frames-'].update('Frames: ' + str(fps))
    elif event == 'Convert':
        window['-Output-'].update('Processing...')
        # print(values)

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
