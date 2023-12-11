import cv2

fourcc = cv2.VideoWriter_fourcc(*'mp4v')


def counting_video_data(result):
    framesCounts = result[0]['value']['framesCount']
    duration = result[0]['value']['duration']
    fps = framesCounts/duration
    return (duration, fps)


def is_out_put(video_file, label_out_put):
    cap = cv2.VideoCapture(video_file)
    if label_out_put:
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        out_put_video = cv2.VideoWriter(label_out_put, codec, 30.0,
                                        (int(cap.get(3)), int(cap.get(4))))
        frame_number = 0
        return cap, out_put_video, frame_number
    else:
        return cap, None, None


def draw_label_for_label(frame, label_info, default_label_name, label_color):
    x, y = label_info["x"], label_info["y"]
    width, height = label_info["width"], label_info["height"]
    cv2.rectangle(frame, (int(x), int(y)), (int(x + width),
                  int(y + height)), label_color, thickness=4)
    cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)


def draw_label_for_blur(frame, label_info, default_label_name, label_color):
    x, y = label_info["x"], label_info["y"]
    width, height = label_info["width"], label_info["height"]
    roi = frame[int(y):int(y+height), int(x):int(x+width)]
    blurred_roi = cv2.GaussianBlur(roi, (25, 25), 0)
    frame[int(y):int(y+height), int(x):int(x+width)] = blurred_roi
    label_box_coords = (int(x), int(y) - 10, int(x + width), int(y))
    cv2.rectangle(frame, (label_box_coords[0], label_box_coords[1]),
                  (label_box_coords[2], label_box_coords[3]),
                  label_color, cv2.FILLED)
    cv2.putText(frame, default_label_name, (int(x), int(y) - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, label_color, 2)


def draw_label_for_chess(frame, label_info, default_label_name, label_color):
    x, y = label_info["x"], label_info["y"]
    width, height = label_info["width"], label_info["height"]
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


def labeling_frames(video_file, frame_info, default_label_name="",
                    label_out_put=None, L="label", label_color=(0, 0, 0)):
    cap, out_put_video, frame_number = is_out_put(video_file, label_out_put)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for info in frame_info:
            if info['frame'] == frame_number:
                if L == 'label':
                    draw_label_for_label(frame, info, default_label_name,
                                         label_color)
                elif L == 'blur':
                    draw_label_for_blur(frame, info, default_label_name,
                                        label_color)
                elif L == 'checkered':
                    draw_label_for_chess(frame, info, default_label_name,
                                         label_color)
        if label_out_put:
            out_put_video.write(frame)
        else:
            print('unredab out_put')
            break
        frame_number += 1
        if frame_number % 500 == 0:
            print("labeling next", frame_number, 'frames',)

    cap.release()
    if label_out_put:
        out_put_video.release()
    return label_out_put
