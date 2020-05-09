import os
import subprocess


def gif_converter(
    load_path=None,
    save_path=None,
    start_time='00:00:00',
    duration='5.',
    fps='10',
    frame_width='320',
):

    # Setup path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if load_path is None:
        load_path = os.path.join(dir_path, 'sample/sample_2.mp4')
    if save_path is None:
        save_path = os.path.join(dir_path, 'output/')
        os.makedirs(save_path, exist_ok=True)

    subprocess.call(['mkdir', 'tmp/'])

    # Extract frames
    subprocess.call([
                    'ffmpeg',
                    '-ss', start_time,  # start time
                    '-t', duration,  # duration
                    '-i', load_path,  # original file dir
                    '-vf', "fps=" + fps + ", scale=" + frame_width + ":-1",
                    '-pix_fmt', 'rgb24',  # pixel formats
                    # output file dir
                    '-y', 'tmp/frame%04d.png',
                    ])

    # Create GIF
    out_file_name = os.path.basename(load_path) + '_converted.gif'
    ex = subprocess.Popen("gifski --fps " + fps + " -o " +
                          os.path.join(save_path, out_file_name) +
                          " tmp/frame*.png", 
                          stdout=subprocess.PIPE,
                          universal_newlines=True,
                          shell=True)

    while ex.poll() == None:
        yield ex.stdout.readline()
        # print(ex.stdout.readline())
    status = ex.wait()
    subprocess.call(['rm', '-rf', 'tmp/'])

    return True


if __name__ == "__main__":
    gif_converter()
