from moviepy.editor import VideoFileClip
import os

project_directory = os.path.dirname(os.path.abspath(__file__))


def add_audio_to_output_video(input_video, muted_video, output_path):
    clip = VideoFileClip(muted_video)
    clip = clip.set_fps(25)
    video_0 = VideoFileClip(input_video)

    taked_audio = video_0.audio
    Duration = video_0.duration
    if Duration is not None:
        last_audio = taked_audio.set_duration(Duration)
    else:
        last_audio = taked_audio

    video_with_audio = clip.set_audio(last_audio)
    video_with_audio.write_videofile(output_path, codec='libx264')

    clip.close()
    video_0.close()
    return output_path


# in_1 = project_directory+'/new_video/tom.mp4'
# in_2 = project_directory+'/new_video/counted_video.mp4'
# out = project_directory+'/new_video/voice_dar.mp4'

# sedadar_kardan(in_1, in_2, out)
