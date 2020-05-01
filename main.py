import PySimpleGUI as sg

sg.theme('DarkTeal2')

split_line_size = 68
start_time_size = (3, 1)

# ------ Column Definition ------ #
column1 = [[sg.Text('Start Time (H:M:S)', justification='left', size=(15, 1))],
           [sg.Spin(values=list(range(100)), initial_value=0, size=start_time_size), sg.Text('Hour')],
           [sg.Spin(values=list(range(100)), initial_value=0, size=start_time_size), sg.Text('Minute')],
           [sg.Spin(values=list(range(100)), initial_value=0, size=start_time_size), sg.Text('Second')],
           ]

column2 = [[sg.Text('Duration (s)', justification='left', size=(9, 1))],
           [sg.Slider(range=(1, 10), orientation='v', size=(3, 20), default_value=5,
           enable_events=True, key='-Slider-1')],
           ]

layout = [
    # File Bowser
    [sg.Text('Please Choose A File (Video or Gif)', size=(35, 1))],
    [sg.Text('Your File', size=(13, 1), auto_size_text=False, justification='right'),
        sg.InputText('Default File'), sg.FileBrowse()],
    [sg.Text('_' * split_line_size)],

    # Setup
    [sg.Text('Setup Arguments', size=(35, 1))],
    [   # Input setting
        sg.Frame('Set Start Time and Duration', [[
            sg.Column(column1),
            sg.Column(column2),
        ]]),
        # Output setting
        sg.Frame('Resolution FPS and FileName', [[
            sg.Text('Res:', justification='left',),
            sg.InputOptionMenu(('320x240', '640x480', '800x600')), 
            sg.Text('FPS: 10', size=(10, 1), justification='left', key='-FPS-')],
            [sg.Slider(range=(50, 300), default_value=100, orientation='h', size=(25, 20),
            enable_events=True, key='-Slider-2')],
            [sg.Text('Output file name:'), sg.InputText(default_text='out.gif', size=(12, 1))]
        ]),
    ],
    [sg.Text('_' * split_line_size)],

    # Conver and Cancel
    [sg.Text(size=(46, 1), key='-OUTPUT-', auto_size_text=False, justification='right'),
     sg.Button('Convert'), sg.Button('Cancel')],


]


window = sg.Window('Tiny GIF Converter', layout,
                   default_element_size=(40, 1), grab_anywhere=False)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event == 'Convert':
        window['-OUTPUT-'].update('Processing...')
    elif event in ('-Slider-1', '-Slider-2'):
        fps = int(values['-Slider-2'] / values['-Slider-1'])
        window['-FPS-'].update('FPS: ' + str(fps))


window.close()

# sg.popup('Title',
#             'The results of the window.',
#             'The button clicked was "{}"'.format(event),
#             'The values are', values)
