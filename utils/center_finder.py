def list_average(coord_list:list) -> float:
    return sum(coord_list) / len(coord_list)

def HF_pcb_center_finder( module_offsets_raw:dict, side:str ) -> dict :
    return {
                'x' : list_average(module_offsets_raw[side]['pcb']['x']),
                'y' : list_average(module_offsets_raw[side]['pcb']['y'])
            }

def HF_sensor_center_finder( module_offsets_raw:dict, side:str, correction:dict ) -> dict :
    return {
                'x' : list_average(module_offsets_raw[side]['sensor']['x']) + correction['x']*(1 if side == 'R' else -1.),
                'y' : list_average(module_offsets_raw[side]['sensor']['y']) - correction['y']*(1 if side == 'R' else -1.)
            }

def HF_baseplate_center_finder( module_offsets_raw:dict, side:str, correction:dict ) -> dict :
    return {
                'x' : module_offsets_raw['measured_ref']["x"] - (correction['Reference']["x"] - correction[side]["x"]),
                'y' : module_offsets_raw['measured_ref']["y"] - (correction['Reference']["y"] - correction[side]["y"])
            }
