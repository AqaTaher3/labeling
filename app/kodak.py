import shutil
import ffmpeg
import os

ffprobe_path = os.popen('which ffprobe').read().strip()
ffmpeg_path = os.popen('which ffmpeg').read().strip()
target_codec = 'libx264'

app_dir = os.path.dirname(os.path.abspath(__file__))


def detect_video_codec(filename):
    try:
        probe = ffmpeg.probe(filename)
        video_stream = next(s for s in probe['streams']
                            if s['codec_type'] == 'video')
        codec_name = video_stream['codec_name']
        print("Video codec: ", codec_name)
        return codec_name
    except ffmpeg.Error as e:
        print(f"{e.stderr.decode('utf-8')}")
    except Exception as e:
        print("Error: ", str(e))


def change_video_codec(video_file, target_codec: str):
    out_put_file = app_dir+'/new_video/kodecked.mp4'
    ffmpeg.input(video_file).output(out_put_file, vcodec=target_codec).run()
    return out_put_file


def codec(input_video):
    print('checking the video codec ...')
    detected = detect_video_codec(input_video)

    if detected == 'h264':
        print('The codec of input video file is:', detected)
        print('No need to change the codec')
        shutil.copy(input_video, app_dir+'/new_video/kodeced.mp4')
        return input_video
    else:
        print('Please wait until the video file codec changes...')
        a = change_video_codec(input_video, target_codec)
        print(detect_video_codec(a))
        return a
