import cv2
import shutil


def frame_repetitioan_count_check(input_video, Results):
    frames_of_label_studio = int(Results[0]['value']['framesCount'])
    with open('new_video/counted_video.mp4', 'wb'):
        pass
    out_put_video = 'new_video/counted_video.mp4'

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
        out = cv2.VideoWriter(out_put_video, fourcc, cap.get(cv2.CAP_PROP_FPS),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        frame_number = 0
        for _ in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_number += 1

            if frame_number % (loop_frame + 1) == 0:
                out.write(frame)
                frame_number += 1

        while frame_number < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_number += 1
        cap.release()
        out.release()
    else:
        shutil.copy(input_video, out_put_video)
    return (out_put_video)


# printing_frames(v, 'print.mp4')
# frame_repetitioan_count_check('/home/user/Desktop/tom_va_jery.mp4', Results)
