import cv2
import os

project_directory = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(project_directory)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')


def printing_frame_number_on_center_the_frame(video_path, out_put_path):
    video = cv2.VideoCapture(video_path)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_put_path, fourcc,
                          fps, (frame_width, frame_height))

    frame_counter = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

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
