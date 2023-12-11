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
# fourcc(*'mp4v')


def reding_data(data):
    f = open(data)
    data = json.load(f)
    Results = data[0]["annotations"][0]["result"]
    f.close()
    with open("Results.json", "w") as file:
        json.dump(Results, file)
    return Results


def labeling_all_models(input_vide0, last_changed_frames,
                        color=(255, 255, 255)):
    single_use = input_vide0
    for i in range(len(last_changed_frames)):
        model_name = list(last_changed_frames[i].keys())[0]
        print('model_name', model_name)
        frame_info = last_changed_frames[i][model_name]
        output_i = '/final_works/' + str(i) + "labeled" + '.mp4'
        labeling_frames(single_use, frame_info, model_name, output_i, color)
        single_use = output_i
    return single_use


def bluring_all_models(input_vide0, last_changed_frames,
                       color=(255, 255, 255)):
    single_use = input_vide0
    for i in range(len(last_changed_frames)):
        model_name = list(last_changed_frames[i].keys())[0]
        print('model_name', model_name)
        frame_info = last_changed_frames[i][model_name]
        output_i = '/final_works/' + str(i) + "labeled" + '.mp4'
        bluring_frames(single_use, frame_info, model_name, output_i, color)
        single_use = output_i
    return single_use


def checkering_all_models(input_vide0, last_changed_frames,
                          color=(255, 255, 255)):
    single_use = input_vide0
    for i in range(len(last_changed_frames)):
        model_name = list(last_changed_frames[i].keys())[0]
        print('model_name', model_name)
        frame_info = last_changed_frames[i][model_name]
        output_i = '/final_works/' + str(i) + "labeled" + '.mp4'
        checkering_frames(single_use, frame_info, model_name, output_i, color)
        single_use = output_i
    return single_use


def delete_directory_contents(directory):
    contents = os.listdir(directory)
    # بررسی و حذف هر فایل یا پوشه درون پوشه
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory_contents(item_path)
            os.rmdir(item_path)


def pixeling(job, input_video, last_changed_frames, directory):
    if job == 'label':
        label_output = labeling_all_models(input_video, last_changed_frames,
                                           (0, 0, 150))
        shutil.move(label_output, directory)
        delete_directory_contents('./final_works')

    elif job == 'blur':
        label_output = bluring_all_models(input_video, last_changed_frames,
                                          (0, 0, 150))
        shutil.move(label_output, directory)
        delete_directory_contents('./final_works')

    elif job == 'checkered':
        label_output = checkering_all_models(input_video, last_changed_frames,
                                             (0, 0, 150))
        shutil.move(label_output, directory)
        delete_directory_contents('./final_works')


def main(json_file, film_path, pixelation):
    directory = os.path.dirname(film_path)

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
    # delete_directory_contents('./new_video')
    return (last_made_list)


print('input_json', 'input_video', 'pixeling' '\n'
      'pixeling :label OR blur OR checkered')

main('/home/user/Desktop/aqua.json', '/home/user/Desktop/print.mp4',
     'label')
