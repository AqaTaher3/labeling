import json
import cv2
import os

from extracking_data import extract_info, \
    destinct_extracted_model, converting_relative_size_to_absolute, \
    extracting_just_models_from_incoming_data, making_final_data
from kodak import codec
from repetitioan_count_check import frame_repetitioan_count_check
from labeling import labeling_frames

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

print('<------------------ا>    In The Name Of God     <ا------------------>')


def reding_data(data):
    f = open(data)
    data = json.load(f)
    Results = data[0]["annotations"][0]["result"]
    framesCounts = Results[0]['value']['framesCount']
    duration = Results[0]['value']['duration']
    fps = framesCounts/duration
    f.close()
    return Results, fps


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
    out_put_video_name = directory + '/' + pixelation + str('.mp4')
    print(out_put_video_name)
    results, fps = reding_data(json_file)
    delete_directory_contents('./app/new_video')
    only_models = extracting_just_models_from_incoming_data(results)
    destincted_models = destinct_extracted_model(only_models)
    extracted_data = extract_info(destincted_models, results)
    last_made_list = making_final_data(extracted_data)
    reformed_vide = codec(film_path)
    understood_video = frame_repetitioan_count_check(reformed_vide, results)
    last_changed_frames = converting_relative_size_to_absolute(
        understood_video, last_made_list)
    a = yeki_kardan_tamame_model_ha(last_changed_frames)

    adress = labeling_frames(understood_video, a, "",
                             out_put_video_name, pixelation, fps)
    print('here are you output adress --->>', adress)
    delete_directory_contents('./app/new_video')


# tozihatttttttttttttttttt
print('input_json', 'input_video', 'pixeling' '\n'
      'pixeling :label OR blur OR checkered')
# tozihatttttttttttttttttt

input = input(('input_json', 'input_video', 'pixeling',
              'pixeling :label OR blur OR checkered'))

input = input.split(" ")

# json_file = os.path.join(os.pardir) + '/input/' + input[0]

json_file = 'input/'+input[0]
video_file = 'input/'+input[1]
main((json_file), video_file, 'label')
