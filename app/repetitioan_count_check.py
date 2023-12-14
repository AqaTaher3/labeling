import cv2
import shutil
import os
from moviepy.config import change_settings
from moviepy.editor import VideoFileClip


codecc = 'h264'

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


def frame_repetition_count_check(input_video, Results):
    output_video = project_directory + '/new_video/counted_video.mp4'
    clip = VideoFileClip(input_video)
    frames_of_label_studio = int(Results[0]['value']['framesCount'])

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
        fps = clip.fps
        width, height = clip.size
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        frame_number = 0
        while frame_number < total_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % (loop_frame + 1) == 0:
                out.write(frame)
                frame_number += 1

            out.write(frame)
            frame_number += 1

            un_round = (frame_number/total_frames)*100
            rounded = round(un_round, 2)
            formatted_number = "{:.1%}".format(rounded / 100)
            print(formatted_number)

        cap.release()
        out.release()
        exit()
    else:
        shutil.copy(input_video, output_video)
    print(output_video)
    return output_video
