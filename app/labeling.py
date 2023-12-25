import cv2
import os
from enum import Enum

codec = cv2.VideoWriter_fourcc(*'mp4v')

ffprobe_path = os.popen('which ffprobe').read().strip()
ffmpeg_path = os.popen('which ffmpeg').read().strip()

app_dir = os.path.dirname(os.path.abspath(__file__))
work_dir = os.path.dirname(app_dir)

output_path = app_dir+'/new_video/label.mp4'


class Pixelation(str, Enum):
    blur = "blur"
    label = "label"
    checkered = "checkered"


def check_output_existanse(video_file, label_out_put, fps):
    cap = cv2.VideoCapture(video_file)
    if label_out_put:
        output_video = cv2.VideoWriter(
            filename=label_out_put,
            fourcc=codec,
            fps=fps,
            frameSize=(int(cap.get(3)), int(cap.get(4)))
        )
        frame_number = 0
        return cap, output_video, frame_number
    else:
        return cap, None, None


def put_text(frame, label_info, label_name, label_color):
    x, y = label_info["x"], label_info["y"]
    width, height = label_info["width"], label_info["height"]
    cv2.putText(frame, label_name, (int(x), int(y) - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)
    return (x, y, width, height)


def draw_label(frame, label_info, label_name, label_color):
    (x, y, width, height) = put_text(frame, label_info, label_name,
                                     label_color)
    cv2.rectangle(frame, (int(x), int(y)), (int(x + width),
                  int(y + height)), label_color, thickness=4)


def draw_blur(frame, label_info, default_label_name, label_color):
    (x, y, width, height) = put_text(frame, label_info, default_label_name,
                                     label_color)
    roi = frame[int(y):int(y+height), int(x):int(x+width)]
    blurred_roi = cv2.GaussianBlur(roi, (25, 25), 0)
    frame[int(y):int(y+height), int(x):int(x+width)] = blurred_roi
    label_box_coords = (int(x), int(y) - 10, int(x + width), int(y))
    cv2.rectangle(frame, (label_box_coords[0], label_box_coords[1]),
                  (label_box_coords[2], label_box_coords[3]),
                  label_color, cv2.FILLED)


def draw_check(frame, label_info, default_label_name, label_color):
    (x, y, width, height) = put_text(frame, label_info, default_label_name,
                                     label_color)
    try:
        for i in range(int(x), int(x + width), int(width / 8)):
            for j in range(int(y), int(y + height), int(height / 8)):
                row = (j - int(y)) // (int(height / 8))
                col = (i - int(x)) // (int(width / 8))
                if (row + col) % 2 == 0:
                    cv2.rectangle(frame, (i, j), (i + int(width / 8),
                                  j + int(height / 8)),
                                  (0, 0, 0), cv2.FILLED)
                else:
                    cv2.rectangle(frame, (i, j), (i + int(width / 8),
                                  j + int(height / 8)),
                                  (255, 255, 255), cv2.FILLED)
    except ZeroDivisionError:
        pass
    except ValueError:
        pass

    label_box_coords = (int(x), int(y) - 10, int(x + width), int(y))

    cv2.rectangle(frame, (label_box_coords[0], label_box_coords[1]),
                  (label_box_coords[2], label_box_coords[3]),
                  label_color, cv2.FILLED)


def label_frames(
    video_file,
    frames_info_list,
    fps,
    pixelation,
    label_color=(0, 0, 0)
):
    cap, out_put_video, frame_number = check_output_existanse(video_file, output_path, fps)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for frames_info in frames_info_list:
            if frames_info['frame'] == frame_number:
                model_name = frames_info['model']

                if pixelation == Pixelation.label:
                    draw_label(frame, frames_info, model_name, label_color)
                elif pixelation == Pixelation.blur:
                    draw_blur(frame, frames_info, model_name, label_color)
                elif pixelation == Pixelation.checkered:
                    draw_check(frame, frames_info, model_name, label_color)

        if output_path:
            out_put_video.write(frame)
        else:
            print('unredab out_put')
            break
        frame_number += 1
        if frame_number % 500 == 0:
            print("labeling next", frame_number, 'frames')

    cap.release()
    if output_path:
        out_put_video.release()
    return output_path
