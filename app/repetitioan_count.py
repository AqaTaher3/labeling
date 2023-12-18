import cv2
import shutil
import os
from moviepy.editor import VideoFileClip

ffprobe_path = os.popen('which ffprobe').read().strip()
ffmpeg_path = os.popen('which ffmpeg').read().strip()

app_dir = os.path.dirname(os.path.abspath(__file__))
codecc = 'h264'
# app/new_video_path = shutil.which('app/new_video')
# change_settings({"app/new_video_BINARY": app/new_video_path})


def count_frames(input_video):
    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count


def frame_repetition_count_check(input_video, Results):
    output_video = app_dir + '/new_video/counted_video.mp4'
    clip = VideoFileClip(input_video)
    frames_of_label_studio = int(Results[0]['value']['framesCount'])
    framesCounts = Results[0]['value']['framesCount']
    duration = Results[0]['value']['duration']
    fps = framesCounts/duration
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

        cap.release()
        out.release()
    else:
        shutil.copy(input_video, output_video)
    return output_video
