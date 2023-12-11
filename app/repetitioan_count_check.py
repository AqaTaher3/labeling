import cv2
import shutil
import json


def printing_frames(video_path, output_path):
    video = cv2.VideoCapture(video_path)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc,
                          fps, (frame_width, frame_height))

    frame_counter = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        # نوشتن شماره فریم وسط هر فریم ویدیو
        text = f'Frame: {frame_counter}'
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_x = int((frame_width - text_size[0]) / 2)
        text_y = int((frame_height + text_size[1]) / 2)
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2, cv2.LINE_AA)

        out.write(frame)

        frame_counter += 1
        print('printing', frame_counter)

    video.release()
    out.release()
    cv2.destroyAllWindows()


f = open('Results.json')
Results = json.load(f)

# frame_repetitioan_count_check('/home/user/Desktop/tom_va_jery.mp4', Results)
# printing_frames('/home/user/Desktop/3.mp4', '/home/user/Desktop/04.mp4')


def frame_repetitioan_count_check(input_video, Results):
    frames_of_label_studio = int(Results[0]['value']['framesCount'])
    with open('new_video/counted_video.mp4', 'wb'):
        pass
    output_video = 'new_video/counted_video.mp4'

    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('counts of your vide frames :', frame_count)
    if frames_of_label_studio > frame_count:
        print('count of your json file frames', frames_of_label_studio)
        print('repetitioan_frames_count ...  ')
        diffrent_frames = frames_of_label_studio - frame_count

        loop_frame = int(frame_count / diffrent_frames)

        total_frames = frame_count + diffrent_frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, cap.get(cv2.CAP_PROP_FPS),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # اضافه کردن فریم‌های تکراری
        frame_number = 0
        for _ in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_number += 1
            # اضافه کردن فریم‌های تکراری
            if frame_number % (loop_frame + 1) == 0:
                out.write(frame)
                frame_number += 1

        # اضافه کردن فریم‌های باقی‌مانده
        while frame_number < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_number += 1
        cap.release()
        out.release()
    else:
        shutil.copy(input_video, output_video)
    return (output_video)


# frame_repetitioan_count_check('/home/user/Desktop/tom_va_jery.mp4', Results)
v = '/home/user/Desktop/counted_video.mp4'

# printing_frames(v, 'print.mp4')
