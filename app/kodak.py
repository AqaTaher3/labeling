import shutil
import ffmpeg

target_codec = 'libx264'


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
    # with open('app/new_video/kodecked.mp4', 'wb'):
    #     pass
    out_put_file = 'app/new_video/kodecked.mp4'
    ffmpeg.input(video_file).output(out_put_file, vcodec=target_codec).run()
    return out_put_file


def codec(input_video):
    print('barresi_codec')
    detected = detect_video_codec(input_video)

    if detected == 'h264':
        print('The codec of input video file is:', detected)
        print('No need to change the codec')
        shutil.copy(input_video, 'app/new_video/')
        return input_video
    else:
        print('Please wait until the video file codec changes...')
        a = change_video_codec(input_video, target_codec)
        print(detect_video_codec(a))
        return a
# a = '/home/user/Desktop/counted_video.mp4'
# b = codec(a)