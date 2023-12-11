import cv2
import json

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

f = open('Results.json')
Results = json.load(f)
f.close()

framesCounts = Results[0]['value']['framesCount']
duration = Results[0]['value']['duration']
fps = framesCounts/duration


def is_out_put(input, out_put):
    cap = cv2.VideoCapture(input)
    if out_put:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_put_video = cv2.VideoWriter(out_put, fourcc, fps,
                                        (frame_width, frame_height))
    return (cap, out_put_video)


def labeling_frames(video_file, frame_info, default_label_name="",
                    label_out_put=None, label_color=(0, 0, 0)):

    frame_number = 0
    cap = cv2.VideoCapture(video_file)
    if label_out_put:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out_put_video = cv2.VideoWriter(label_out_put, fourcc, fps,
                                        (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for info in frame_info:
            if info['frame'] == frame_number:
                x, y = info["x"], info["y"]
                width, height = info["width"], info["height"]
                cv2.rectangle(frame, (int(x), int(y)), (int(x + width),
                              int(y + height)), label_color, thickness=4)
                cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)

        if label_out_put:
            out_put_video.write(frame)
        else:
            print('unredab out_put')
            break
        frame_number += 1
        if frame_number % 500 == 0:
            print("labeling next", frame_number, 'frames',
                  'for model:', default_label_name)

    cap.release()
    if label_out_put:
        out_put_video.release()
    return label_out_put


ff = open('Resultsss.json')
dataa = json.load(ff)
g = dataa
ff.close()

b = []
for i in range(len(g)):
    key = list(g[i].keys())[0]
    dicts = g[i][key]
    b.extend(dicts)

sorted_frames = sorted(b, key=lambda x: x['frame'])
frames_list = sorted_frames


with open("bb.json", "w") as file:
    json.dump(frames_list, file)

labeling_frames('/home/user/Desktop/counted_video.mp4', b, "Tom",
                '/home/user/Desktop/com.mp4', (0, 0, 0))

# ...................................................................


def bluring_frames(video_file, frame_info, default_label_name="",
                   label_out_put=None, label_color=(0, 0, 0)):

    frame_number = 0
    (cap, out_put_video) = is_out_put(video_file, label_out_put)

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

            if label_out_put:
                out_put_video.write(frame)

            frame_number += 1
            if frame_number % 500 == 0:
                print("bluring next ", frame_number, 'frames',
                      'for model:', default_label_name)


# ...................................................................


def checkering_frames(video_file, frame_info, default_label_name="",
                      label_out_put=None, label_color=(0, 0, 0)):

    cap = cv2.VideoCapture(video_file)
    frame_number = 0

    frame_number = 0
    (cap, out_put_video) = is_out_put(video_file, label_out_put)

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

        if label_out_put:
            out_put_video.write(frame)

        frame_number += 1
        if frame_number % 500 == 0:
            print("chckerding next ",
                  frame_number, 'frames')

    cap.release()

    if label_out_put:
        out_put_video.release()
