from HGCal_Module_Production_Toolkit.utils.center_finder import *
from HGCal_Module_Production_Toolkit.utils.d_vector_finder import *
from HGCal_Module_Production_Toolkit.utils.io_tool import get_offsets_raw_from_textfile, write_to_csv

import yaml

def ragular_all_numbers(obj, factor=1):
    if isinstance(obj, dict):
        return {k: ragular_all_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ragular_all_numbers(v) for v in obj]
    elif isinstance(obj, (int, float)):
        return round(obj*factor, 4)
    else:
        return obj

def get_angle_from_two_vectors(v1:dict, v2:dict) -> float:

    length_1 = math.sqrt( v1['d_vector_x'] ** 2 + v1['d_vector_y'] ** 2 )
    length_2 = math.sqrt( v2['d_vector_x'] ** 2 + v2['d_vector_y'] ** 2 )

    dot = v1['d_vector_x']*v2['d_vector_x'] + v1['d_vector_y']*v2['d_vector_y']

    cos_theta = dot / (length_1*length_2)

    return abs( math.acos(cos_theta) ) * 180. / math.pi

def calculate_centor_offsets(modules:dict, offsets_raw:dict) -> dict:

    with open("data/sensor.yaml", 'r') as sensor_correction_file:
        sensor_correction = yaml.safe_load(sensor_correction_file)

    with open("data/tray.yaml", 'r') as baseplate_correction_file:
        baseplate_correction = yaml.safe_load(baseplate_correction_file)

    offsets = {}

    for module in modules:

        module_list = module.split("-")

        module      = module_list[0]
        module_type = module_list[0][4:6]
        tray_index  = module_list[1]
        tray_side   = module_list[2]

        pcb_centers       = globals()[f"{module_type}_pcb_center_finder"](offsets_raw, tray_side)
        sensor_centers    = globals()[f"{module_type}_sensor_center_finder"](offsets_raw, tray_side, sensor_correction[module_type])
        baseplate_centers = globals()[f"{module_type}_baseplate_center_finder"](offsets_raw, tray_side, baseplate_correction[tray_index])


        offsets[module] = {}
        offsets[module]["center_offsets"] = {
                "pcb"    : [ pcb_centers   ["x"] - baseplate_centers["x"], pcb_centers   ["y"] - baseplate_centers["y"] ],
                "sensor" : [ sensor_centers["x"] - baseplate_centers["x"], sensor_centers["y"] - baseplate_centers["y"] ],
                }

    return offsets

def calculate_angle_offsets(modules:dict, offsets_raw:dict) -> dict:

    with open("data/sensor.yaml", 'r') as sensor_correction_file:
        sensor_correction = yaml.safe_load(sensor_correction_file)

    offsets = {}
    for module in modules:

        module_list = module.split("-")

        module      = module_list[0]
        module_type = module_list[0][4:6]
        tray_index  = module_list[1]
        tray_side   = module_list[2]

        pcb_d_vector       = globals()[f"{module_type}_pcb_d_vector_finder"](offsets_raw, tray_side)
        sensor_d_vector    = globals()[f"{module_type}_sensor_d_vector_finder"](offsets_raw, tray_side, sensor_correction[module_type])
        baseplate_d_vector = globals()[f"{module_type}_baseplate_d_vector_finder"](offsets_raw, tray_side)

        sensor_angle_offsets = get_angle_from_two_vectors(sensor_d_vector, baseplate_d_vector)
        pcb_angle_offsets    = get_angle_from_two_vectors(pcb_d_vector, baseplate_d_vector)

        if pcb_d_vector['d_vector_y'] < baseplate_d_vector['d_vector_y']:
            pcb_angle_offsets = -pcb_angle_offsets
        if sensor_d_vector['d_vector_y'] < baseplate_d_vector['d_vector_y']:
            sensor_angle_offsets = -sensor_angle_offsets

        offsets[module] = {}
        offsets[module]["angle_offsets"] = {
                "pcb"    : pcb_angle_offsets,
                "sensor" : sensor_angle_offsets
                }

    return offsets

def offsets_calculator(modules:list, textfile:str) -> dict:

    module_offsets_raw = get_offsets_raw_from_textfile(textfile)

    offsets = calculate_centor_offsets(modules, module_offsets_raw)
    offsets = ragular_all_numbers(offsets, factor=1000)

    angle_offsets = calculate_angle_offsets (modules, module_offsets_raw)
    angle_offsets = ragular_all_numbers(angle_offsets)

    for k, v in angle_offsets.items():
        offsets[k].update(v)

    return offsets

if __name__ == '__main__':

    modules = [
        "320MHF2WCNT0098-AT07-R",
        "320MHF2WCNT0099-AT07-L"
        ]


    txtfile = 'M165M166.txt'

    offsets = offsets_calculator(modules, txtfile)

    print(offsets)

    write_to_csv(offsets, 'vvvv.csv' )
