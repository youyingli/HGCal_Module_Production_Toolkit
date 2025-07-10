from HGCal_Module_Production_Toolkit.utils.center_finder import *
from HGCal_Module_Production_Toolkit.utils.io_tool import get_offsets_raw_from_textfile, write_to_csv

import yaml

def ragular_all_numbers(obj):
    if isinstance(obj, dict):
        return {k: ragular_all_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ragular_all_numbers(v) for v in obj]
    elif isinstance(obj, (int, float)):
        return round(obj*1000., 4)
    else:
        return obj

def calculate_centor_offsets(modules:dict, textfile:str) -> dict:

    module_offsets_raw = get_offsets_raw_from_textfile(textfile)

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

        pcb_centers       = globals()[f"{module_type}_pcb_center_finder"](module_offsets_raw, tray_side)
        sensor_centers    = globals()[f"{module_type}_sensor_center_finder"](module_offsets_raw, tray_side, sensor_correction[module_type])
        baseplate_centers = globals()[f"{module_type}_baseplate_center_finder"](module_offsets_raw, tray_side, baseplate_correction[tray_index])


        offsets[module] = {}
        offsets[module]["center_offsets"] = {
                "pcb"    : [ pcb_centers   ["x"] - baseplate_centers["x"], pcb_centers   ["y"] - baseplate_centers["y"] ],
                "sensor" : [ sensor_centers["x"] - baseplate_centers["x"], sensor_centers["y"] - baseplate_centers["y"] ],
                }

    return offsets

def calculate_angle_offsets(modules:dict, textfile:str) -> dict:
    pass

def offsets_calculator(modules:list, txtfile:str) -> dict:

    offsets = calculate_centor_offsets(modules, txtfile)
    offsets = ragular_all_numbers(offsets)

#    calculate_angle_offsets()

    return offsets

if __name__ == '__main__':

    modules = [
        "320MHF2WCNT0098-AT07-R",
        "320MHF2WCNT0099-AT07-L"
        ]


    txtfile = 'M165M166.txt'

    offsets = offsets_calculator(modules, txtfile)
    write_to_csv(offsets, 'vvvv.csv' )
