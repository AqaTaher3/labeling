import json
import cv2
import os
from extracking_data import extract_info, \
    destinct_extracted_model, converting_relative_size_to_absolute, \
    extracting_just_models_from_incoming_data, making_final_data
from kodak import codec
from repetitioan_count_check import frame_repetition_count_check
from labeling import labeling_frames
from voice import sedadar_kardan

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

project_directory = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(project_directory)


# current_directory = os.getcwd()
# parent_directory = os.path.dirname(current_directory)
# base = os.path.join((base_dir+'/label'))

print('<------------------ا>    In The Name Of God     <ا------------------>')


def reding_data(data):
    f = open(data)
    data = json.load(f)
    Results = data[0]["annotations"][0]["result"]
    framesCounts = Results[0]['value']['framesCount']
    duration = Results[0]['value']['duration']
    fps = framesCounts/duration
    f.close()
    return Results, fps, duration


def yeki_kardan_tamame_model_ha(kist):

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


def main(json_file, film_path, pixelation):
    directory = os.path.dirname(film_path)
    out_label = directory + '/' + pixelation + '.mp4'
    final_out_put = directory + '/' + 'voice_dar' + '.mp4'
    res, fps, duration = reding_data(json_file)
    # delete_directory_contents(os.path.join(project_directory + '/new_video'))
    only_models = extracting_just_models_from_incoming_data(res)
    destincted_models = destinct_extracted_model(only_models)
    extracted_data = extract_info(destincted_models, res)
    last_made_list = making_final_data(extracted_data)
    reformed_vide = codec(film_path)
    understood_video = frame_repetition_count_check(reformed_vide, res)
    last_changed_frames = converting_relative_size_to_absolute(
        understood_video, last_made_list)
    print(last_made_list)
    with open('last_last.json', 'w') as f:
        json.dump(last_made_list, f)
    yeki_shode = yeki_kardan_tamame_model_ha(last_changed_frames)

    print('laa****************************************')

    adress = labeling_frames(understood_video, yeki_shode, fps,
                             out_label, pixelation, (0, 0, 0))

    bb = sedadar_kardan(reformed_vide, adress, duration, final_out_put)

    print('here are you output adress --->>', adress, bb)
    # delete_directory_contents(project_directory + '/new_video')


# tozihatttttttttttttttttt
print('input_json', 'input_video', 'pixeling' '\n'
      'pixeling :label OR blur OR checkered')
# tozihatttttttttttttttttt

# Json_file = (base_dir + '/inputs/' + input('Json  ?  '))
# Video_file = (base_dir + '/inputs/' + input('File  ?  '))
# pixelation = input('pixelation  ?  ')

# main(Json_file, Video_file, pixelation)
Json_file = (base_dir + '/inputs/' + 'aqua.json')
Video_file = (base_dir + '/inputs/' + 'tom.mp4')


main(Json_file, Video_file, 'label')
