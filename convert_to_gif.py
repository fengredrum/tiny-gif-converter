import os
import subprocess


def convert_to_gif():
    save_path = './output'
    os.makedirs(save_path, exist_ok=True)

    print('dir: \n', os.getcwd())

    subprocess.call([
                    'ffmpeg', 
                    '-ss', '00:00:00.000',
                    '-t', '00:00:5.000', 
                    '-i', 'sample/t_2.mp4', 
                    '-pix_fmt', 'yuv420p',
                    '-r', '10', 
                    '-s', '360x360', 
                    # '-t', '00:00:5.000', 
                    '-frames', '100',
                    '-y', 'output/test.gif'])


if __name__ == "__main__":
    convert_to_gif() 
