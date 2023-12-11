import cv2
import json

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

f = open('Results.json')
Results = json.load(f)
f.close()

framesCounts = Results[0]['value']['framesCount']
duration = Results[0]['value']['duration']
fps = framesCounts/duration


def is_output(input, output):
    cap = cv2.VideoCapture(input)
    if output:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_video = cv2.VideoWriter(output, fourcc, fps,
                                       (frame_width, frame_height))
    return (cap, output_video)


def labeling_frames(video_file, frame_info, default_label_name="",
                    label_output=None, label_color=(0, 0, 0)):

    frame_number = 0
    (cap, output_video) = is_output(video_file, label_output)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_info and len(frame_info) > 0 and frame_info[0]['frame'] \
                <= frame_number:
            info = frame_info.pop(0)
            x, y = info["x"], info["y"]
            width, height = info["width"], info["height"]
            cv2.rectangle(frame, (int(x), int(y)), (int(x + width),
                          int(y + height)), label_color, thickness=4)
            cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)

        if label_output:
            output_video.write(frame)

        frame_number += 1
        if frame_number % 500 == 0:
            print("labeeeling next ", frame_number, 'frames',
                  'for model:', default_label_name)

    cap.release()
    if label_output:
        output_video.release()

# ...................................................................


def bluring_frames(video_file, frame_info, default_label_name="",
                   label_output=None, label_color=(0, 0, 0)):

    frame_number = 0
    (cap, output_video) = is_output(video_file, label_output)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_info and len(frame_info) > 0 and frame_info[0]['frame'] \
                <= frame_number:
            info = frame_info.pop(0)
            x, y = info["x"], info["y"]
            width, height = info["width"], info["height"]
            frame_roi = frame[int(y):int(y + height), int(x):int(x + width)]
            blurred_roi = cv2.GaussianBlur(frame_roi, (25, 25), 5)
            frame[int(y):int(y + height), int(x):int(x + width)] = blurred_roi

            label_box_coords = (int(x), int(y) - 10, int(x + width), int(y))
            cv2.rectangle(frame, (label_box_coords[0], label_box_coords[1]),
                          (label_box_coords[2], label_box_coords[3]),
                          label_color, cv2.FILLED)
            cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, label_color,
                        2, cv2.LINE_AA)

            if label_output:
                output_video.write(frame)

            frame_number += 1
            if frame_number % 500 == 0:
                print("bluring next ", frame_number, 'frames',
                      'for model:', default_label_name)


# ...................................................................


def checkering_frames(video_file, frame_info, default_label_name="",
                      label_output=None, label_color=(0, 0, 0)):

    cap = cv2.VideoCapture(video_file)
    frame_number = 0

    frame_number = 0
    (cap, output_video) = is_output(video_file, label_output)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if len(frame_info) > 0 and frame_info[0]["frame"] <= frame_number:
            info = frame_info.pop(0)
            x, y = info["x"], info["y"]
            width, height = info["width"], info["height"]
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
            cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, label_color, 2,
                        cv2.LINE_AA)

        if label_output:
            output_video.write(frame)

        frame_number += 1
        if frame_number % 500 == 0:
            print("chckerding next ",
                  frame_number, 'frames')

    cap.release()

    if label_output:
        output_video.release()
