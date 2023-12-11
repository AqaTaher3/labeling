import cv2

def  extracting_just_models_from_incoming_data(incoming_result):
    modele_avalie = []
    for a in range(len(incoming_result)):
        try :
            b = incoming_result[a]["value"]['labels'][0]
            modele_avalie.append({b: []})
        except KeyError:
            a += 1    
    return modele_avalie


def destinct_extracted_model(modele_avalie):
    model_ha = []
    for i in range(len(modele_avalie)):
        if modele_avalie[i] not in model_ha:
            model_ha.append(modele_avalie[i])
    return model_ha


def extract_info(incoming_blank_models, incoming_result):
    blanks = incoming_blank_models
    results = incoming_result
    for result in results:
            for blank in range(len(blanks)):
                if result["value"]['labels'][0] == list(blanks[blank])[0]:
                    blank_key = result['value']['labels'][0]
                    blanks[blank][blank_key] += result['value']['sequence']
    return blanks


def create_intermediate_frames(frames_list: list):
    sorted_frames = sorted(frames_list, key=lambda x: x['frame'])
    frames_list = sorted_frames
    new_frames = []
    for i in range(len(frames_list) - 1):
        if frames_list[i]['enabled'] == True :
            frame1 = frames_list[i]
            frame2 = frames_list[i+1]
            frame1_value = frame1['frame']
            frame2_value = frame2['frame']
            for j in range(frame1_value, frame2_value):
                frame_ratio = (j-frame1_value) / (frame2_value - frame1_value)
                new_frame = {
                'frame': j,
                "enabled": frames_list[i]['enabled'],
                'x': round((frame2['x'] - frame1['x']) * frame_ratio + frame1['x'], 2),
                'y': round((frame2['y'] - frame1['y']) * frame_ratio + frame1['y'], 2),
                'width': round((frame2['width'] - frame1['width']) * frame_ratio + frame1['width'], 2),
                'height': round((frame2['height'] - frame1['height']) * frame_ratio + frame1['height'], 2)
                            }
                new_frames.append(new_frame)
        else :
            new_frames.append(frames_list[i])
            i + 1
            
            
    new_frames.append(frames_list[-1])
    return new_frames

def making_final_data(list_0):
    final_data = list_0
    for final in final_data:
        key = list(final.keys())[0]
        final[key] = create_intermediate_frames(final[key])
    return final_data


def calculate_relevant_dimensions(video_for_converting):
    cap = cv2.VideoCapture(video_for_converting)
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))/100
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))/100
    print('your video size',original_width, original_height)
    return (original_width, original_height)

def converting_relative_size_to_absolute(video_for_converting, relative_list:list):
    (original_width, original_height) = calculate_relevant_dimensions(video_for_converting)
    list = relative_list
    for rel in list:
        for item in rel.values():    
            for i in range(len(item)):
                item[i]['x'] *= original_width
                item[i]['width'] *= original_width
                item[i]['y'] *= original_height
                item[i]['height'] *= original_height
    return list



