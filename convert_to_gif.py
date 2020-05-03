import os
import subprocess


def gif_converter(
    load_path=None,
    save_path=None,
    start_time='00:00:00',
    duration='2.',
    fps='10',
    frame_size='640x480',
):

    # Setup path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if load_path is None:
        load_path = os.path.join(dir_path, 'sample/sample_1.gif')
    if save_path is None:
        save_path = os.path.join(dir_path, 'output/')
        os.makedirs(save_path, exist_ok=True)

    out_file_name = os.path.basename(load_path) + '_converted.gif'

    # Convert file
    subprocess.call([
                    'ffmpeg',
                    '-ss', start_time,  # start time
                    '-t', duration,  # duration
                    '-i', load_path,  # original file dir
                    '-pix_fmt', 'yuv420p',  # pixel formats
                    '-r', fps,  # fps
                    '-s', frame_size,  # resolution
                    # output file dir
                    '-y', os.path.join(save_path, out_file_name),
                    ])

    return 'Done'


if __name__ == "__main__":
    gif_converter()
