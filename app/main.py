import json
import shutil
import cv2
import os

from extracking_data import extract_info, \
    destinct_extracted_model, converting_relative_size_to_absolute, \
    extracting_just_models_from_incoming_data, making_final_data
from kodak import codec
from repetitioan_count_check import frame_repetitioan_count_check
from labeling import labeling_frames, bluring_frames, checkering_frames

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

print('<------------------ا>    In The Name Of God     <ا------------------>')


def reding_data(data):
    f = open(data)
    data = json.load(f)
    Results = data[0]["annotations"][0]["result"]
    f.close()
    with open("Results.json", "w") as file:
        json.dump(Results, file)
    return Results


def apply_changes(input_video, last_changed_frames,
                  job, color=(255, 255, 255)):
    single_use = input_video
    for i, frame_info_dict in enumerate(last_changed_frames):
        model_name = list(frame_info_dict.keys())[0]
        frame_info = frame_info_dict[model_name]
        out_put = f'/new_video/{i}_{job}.mp4'

        if job == 'label':
            a = labeling_frames(single_use, frame_info,
                                model_name, out_put, color)
            single_use = a
            print('sssssss', single_use)
        elif job == 'blur':
            bluring_frames(single_use, frame_info,
                           model_name, out_put, color)
        elif job == 'checkered':
            checkering_frames(single_use, frame_info,
                              model_name, out_put, color)

            single_use = a

    return single_use


def delete_directory_contents(directory: any):
    contents = os.listdir(directory)
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            # delete_directory_contents(item_path)
            os.rmdir(item_path)


def pixeling(job, input_video, last_changed_frames, directory):
    final_out_put = apply_changes(input_video, last_changed_frames,
                                  job, (0, 0, 150))
    shutil.move(final_out_put, directory)
    # delete_directory_contents('./new_video')


def main(json_file, film_path, pixelation):
    directory = os.path.dirname(film_path)
    delete_directory_contents('./new_video')
    with open('/home/user/Desktop/00.mp4', 'wb'):
        pass
    results = reding_data(json_file)

    only_models = extracting_just_models_from_incoming_data(results)
    destincted_models = destinct_extracted_model(only_models)
    extracted_data = extract_info(destincted_models, results)
    last_made_list = making_final_data(extracted_data)
    reformed_vide = codec(film_path)
    understood_video = frame_repetitioan_count_check(reformed_vide, results)
    last_changed_frames = converting_relative_size_to_absolute(
        understood_video, last_made_list)
    pixeling(pixelation, understood_video, last_changed_frames, directory)
    return (last_made_list)


print('input_json', 'input_video', 'pixeling' '\n'
      'pixeling :label OR blur OR checkered')

main('/home/user/Desktop/aqua.json', '/home/user/Desktop/kodecked.mp4',
     'label')
