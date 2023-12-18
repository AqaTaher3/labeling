import json
import cv2
import os
from extracking_data import extract_info, \
    destinct_extracted_model, converting_relative_size_to_absolute, \
    extracting_just_models_from_incoming_data, making_final_data
from kodak import codec
from repetitioan_count import frame_repetition_count_check
from labeling import labeling_frames
from voice import add_audio_to_output_video

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

app_dir = os.path.dirname(os.path.abspath(__file__))
work_dir = os.path.dirname(app_dir)
inputs_text_file_path = work_dir+'/input/input.txt'

print('<------------------ا>    In The Name Of God     <ا------------------>')


def reding_data_from_json(data):
    f = open(data)
    data = json.load(f)
    Results = data[0]["annotations"][0]["result"]
    framesCounts = Results[0]['value']['framesCount']
    duration = Results[0]['value']['duration']
    fps = framesCounts/duration
    f.close()
    return Results, fps


def unite_all_models(kist):
    b = []
    for i in range(len(kist)):
        key = list(kist[i].keys())[0]
        dicts = kist[i][key]
        b.extend(dicts)

    sorted_frames = sorted(b, key=lambda x: x['frame'])
    frames_list = sorted_frames
    return frames_list


def delete_directory_contents(directory: any):
    contents = os.listdir(directory)
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            os.rmdir(item_path)


def output_path(pixelation):
    if pixelation == 'label':
        return (work_dir + '/input/'+pixelation+'ed.mp4')

    if pixelation == 'blur':
        return (work_dir + '/input/'+pixelation+'ed.mp4')

    elif pixelation == 'checkered':
        return (work_dir + '/input/'+pixelation+'.mp4')


def input_checker(json, video, label, color=None):
    if label not in ['label', 'blur', 'checkered']:
        print('invalid_pixalation')
        exit()


def main(json_file, film_path, pixelation, label_color=(0, 0, 0)):
    final_output_path = output_path(pixelation)
    res, fps, = reding_data_from_json(json_file)
    delete_directory_contents(app_dir+'/new_video')
    only_models = extracting_just_models_from_incoming_data(res)
    destincted_models = destinct_extracted_model(only_models)
    extracted_data = extract_info(destincted_models, res)
    last_made_list = making_final_data(extracted_data)
    reformed_vide = codec(film_path)
    understood_video = frame_repetition_count_check(reformed_vide, res)
    last_changed_frames = converting_relative_size_to_absolute(
        understood_video, last_made_list)
    united_models = unite_all_models(last_changed_frames)
    lebeled_video_path = labeling_frames(understood_video, united_models,
                                         fps, pixelation, label_color)
    voiced_video = add_audio_to_output_video(reformed_vide, lebeled_video_path,
                                             final_output_path)

    print('here are you output adress --->>', voiced_video)
    delete_directory_contents(app_dir+'/new_video')


def make_color_format(input_color):
    nospaces = input_color.replace("(", "")
    nospaces = nospaces.replace(")", "")
    RGB = nospaces.split(",")
    return ((int(RGB[0]), int(RGB[1]), int(RGB[2])))


def reding_input(input_file):
    if input_file:
        print('input_file')
        with open(input_file, 'r') as input_info:
            content = input_info.readlines()
            input = []
            for con in content:
                b = con.replace("\n", "")
                input.append(b)
            Json_file = (work_dir+'/input/' + input[0])
            Video_file = (work_dir+'/input/' + input[1])
            pixalation = input[2]

        input_checker(Json_file, Video_file, pixalation)
        main(Json_file, Video_file, pixalation, make_color_format(input[3]))
    else:
        print('input_file_doesnt found')


reding_input(inputs_text_file_path)
