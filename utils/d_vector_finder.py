import math

def HF_pcb_d_vector_finder( module_offsets_raw:dict, side:str ) -> dict :

    # HF pcb
    # center1 = (P1+P3)/2
    # center2 = (P2+P4)/2
    # direction vector = center1 - center2
    local_center1_x = ( module_offsets_raw[side]['pcb']['x'][0] + module_offsets_raw[side]['pcb']['x'][2] ) * 0.5
    local_center1_y = ( module_offsets_raw[side]['pcb']['y'][0] + module_offsets_raw[side]['pcb']['y'][2] ) * 0.5
    local_center2_x = ( module_offsets_raw[side]['pcb']['x'][1] + module_offsets_raw[side]['pcb']['x'][3] ) * 0.5
    local_center2_y = ( module_offsets_raw[side]['pcb']['y'][1] + module_offsets_raw[side]['pcb']['y'][3] ) * 0.5

    d_vector_x = local_center1_x - local_center2_x
    d_vector_y = local_center1_y - local_center2_y

    # Always plus for x component 
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    length = math.sqrt( d_vector_x**2 + d_vector_y**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x/length,
                'd_vector_y' : d_vector_y/length
            }

def HF_sensor_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF sensor
    # direction vector = S1 - S2
    d_vector_x = module_offsets_raw[side]['sensor']['x'][0] - module_offsets_raw[side]['sensor']['x'][1]
    d_vector_y = module_offsets_raw[side]['sensor']['y'][0] - module_offsets_raw[side]['sensor']['y'][1]

    # Always plus for x component 
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    # Angle rotation as correction
    theta = correction['theta'] * math.pi / 180.
    d_vector_x_corr = d_vector_x * math.cos(theta) + d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) - d_vector_x * math.sin(theta)

    length = math.sqrt( d_vector_x_corr**2 + d_vector_y_corr**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x_corr/length,
                'd_vector_y' : d_vector_y_corr/length
            }

def HF_baseplate_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF baseplate
    # direction vector =TTT1 - TTT2
    d_vector_x = module_offsets_raw['measured_ref']['x'] - module_offsets_raw['measured_sup_ref']['x']
    d_vector_y = module_offsets_raw['measured_ref']['y'] - module_offsets_raw['measured_sup_ref']['y']

    # Always plus for x component 
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    length = math.sqrt( d_vector_x**2 + d_vector_y**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x/length,
                'd_vector_y' : d_vector_y/length
            }
