import base64
from IPython import display
import imageio

def embed_mp4(filename):
  video = open(filename,'rb').read()
  b64 = base64.b64encode(video)
  tag = '''
  '''.format(b64.decode())
  return display.HTML(tag)

def update_episode_recap(episode_number, frames):
    filename = f'episodes_recaps/episode_{episode_number}.mp4'
    with imageio.get_writer(filename, fps=30) as video:
        for frame in frames:
            video.append_data(frame)
    embed_mp4(filename)