import os
import cv2
import subprocess
import random
import numpy as np
import torch
from PIL import Image

from arguments import get_args
from environment import make_vec_envs
from utils import get_vec_normalize


def evaluate(args):
    # Setup
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device('cpu')

    num_processes = 1
    torch.set_num_threads(1)
    args.eval_log_dir += args.env_id + '/' + args.run_id + '/'
    os.makedirs(args.eval_log_dir, exist_ok=True)

    eval_envs = make_vec_envs(args.env_id, args.seed, num_processes,
                              None, args.eval_log_dir, device)

    # We need to use the same statistics for normalization as used in training
    load_path = os.path.join(args.save_dir, args.env_id)
    load_path += '/' + args.run_id + '/'
    ob_rms, actor_net, _, _, _ = \
        torch.load(os.path.join(load_path, "100000.pt"), map_location='cpu')
    actor_net.eval()

    vec_norm = get_vec_normalize(eval_envs)
    if vec_norm is not None:
        vec_norm.eval()
        vec_norm.ob_rms = ob_rms

    eval_episode_rewards, eval_episode_steps = [], []
    subprocess.call(['mkdir', '-p', args.eval_log_dir + str(len(eval_episode_rewards)) + '/frames'])
    obs = eval_envs.reset()
    steps = 0

    while len(eval_episode_rewards) < 1:
        image_data = np.asarray(
            cv2.resize(eval_envs.render(mode='rgb_array'), (args.video_width, args.video_height),
                       interpolation=cv2.INTER_LINEAR), dtype=np.uint8)
        img = Image.fromarray(image_data, 'RGB')
        img.save(args.eval_log_dir + str(len(eval_episode_rewards)) + '/frames/frame-%.10d.png' % steps)

        with torch.no_grad():
            action = actor_net(obs, True)

        # Obser reward and next obs
        obs, _, done, infos = eval_envs.step(action)
        steps += 1

        for info in infos:
            if 'episode' in info.keys():
                subprocess.call([
                    'ffmpeg', '-framerate', '60', '-y', '-i',
                    args.eval_log_dir + str(len(eval_episode_rewards)) + '/frames/frame-%010d.png',
                    '-r', '30', '-pix_fmt', 'yuv420p',
                    args.eval_log_dir + str(len(eval_episode_rewards)) + '/' + 'test-video.mp4'])
                subprocess.call(['rm', '-rf', args.eval_log_dir + '_' + str(len(eval_episode_rewards)) + '/frames'])
                eval_episode_rewards.append(info['episode']['r'])
                eval_episode_steps.append(steps)
                steps = 0
                subprocess.call(['mkdir', '-p', args.eval_log_dir + str(len(eval_episode_rewards)) + '/frames'])
                print('write video')

    eval_envs.close()

    print(" Evaluation using {} episodes: mean reward {:.5f}, mean steps {:.1f}\n".format(
        len(eval_episode_rewards), np.mean(eval_episode_rewards), np.mean(eval_episode_steps)))


if __name__ == '__main__':
    args = get_args()

    evaluate(args)
