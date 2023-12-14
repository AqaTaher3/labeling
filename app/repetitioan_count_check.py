import cv2
import shutil
import os
from moviepy.config import change_settings
from moviepy.editor import VideoFileClip

ffmpeg_path = shutil.which('ffmpeg')

change_settings({"FFMPEG_BINARY": ffmpeg_path})

project_directory = os.path.dirname(os.path.abspath(__file__))


def count_frames(input_video):
    print(123, 'count_frames')
    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count


def extract_audio(input_video):
    print(123, 'extract_audio')
    clip = VideoFileClip(input_video)
    audio = clip.audio
    return audio


def write_video_with_audio(output_video, video_clip, audio_clip):
    print(123, 'write_video_with_audio')
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_video, codec="libx264")


def frame_repetition_count_check(input_video, Results):
    frames_of_label_studio = int(Results[0]['value']['framesCount'])
    output_video = project_directory + '/new_video/counted_video.mp4'

    frame_count = count_frames(input_video)
    print('counts of your video frames:', frame_count)
    if frames_of_label_studio > frame_count:
        print('count of your json file frames:', frames_of_label_studio)
        print('repetition_frames_count ...')

        different_frames = frames_of_label_studio - frame_count
        loop_frame = int(frame_count / different_frames)
        total_frames = frame_count + different_frames

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        cap = cv2.VideoCapture(input_video)
        out = cv2.VideoWriter(output_video, fourcc, cap.get(cv2.CAP_PROP_FPS),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        frame_number = 0
        while frame_number < total_frames:
            print(total_frames, 'totalll')
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % (loop_frame + 1) == 0:
                out.write(frame)
                frame_number += 1

            out.write(frame)
            frame_number += 1
            print(frame_number)

        cap.release()
        out.release()
        audio = extract_audio(input_video)
        write_video_with_audio(output_video, VideoFileClip(output_video),
                               audio)
    else:
        shutil.copy(input_video, output_video)

    return output_video
