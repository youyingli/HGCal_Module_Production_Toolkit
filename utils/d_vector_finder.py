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
    d_vector_x_corr = d_vector_x * math.cos(theta) - d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) + d_vector_x * math.sin(theta)

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

def HL_pcb_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF pcb
    # direction vector = M1 - M4
    d_vector_x = module_offsets_raw[side]['pcb']['x']['M1'] - module_offsets_raw[side]['pcb']['x']['M4']
    d_vector_y = module_offsets_raw[side]['pcb']['y']['M1'] - module_offsets_raw[side]['pcb']['y']['M4']

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

def HL_sensor_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF sensor
    # direction vector = M26 - M3
    d_vector_x = module_offsets_raw[side]['sensor']['x']['M26'] - module_offsets_raw[side]['sensor']['x']['M3']
    d_vector_y = module_offsets_raw[side]['sensor']['y']['M26'] - module_offsets_raw[side]['sensor']['y']['M3']

    # Always plus for x component
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    # Angle rotation as correction
    theta = correction['theta'] * math.pi / 180.
    d_vector_x_corr = d_vector_x * math.cos(theta) - d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) + d_vector_x * math.sin(theta)

    length = math.sqrt( d_vector_x_corr**2 + d_vector_y_corr**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x_corr/length,
                'd_vector_y' : d_vector_y_corr/length
            }

def HL_baseplate_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

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

def HR_pcb_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF pcb
    # direction vector = M3 - M4
    d_vector_x = module_offsets_raw[side]['pcb']['x']['M3'] - module_offsets_raw[side]['pcb']['x']['M4']
    d_vector_y = module_offsets_raw[side]['pcb']['y']['M3'] - module_offsets_raw[side]['pcb']['y']['M4']

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

def HR_sensor_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF sensor
    # direction vector = M13 - M6
    d_vector_x = module_offsets_raw[side]['sensor']['x']['M13'] - module_offsets_raw[side]['sensor']['x']['M6']
    d_vector_y = module_offsets_raw[side]['sensor']['y']['M13'] - module_offsets_raw[side]['sensor']['y']['M6']

    # Always plus for x component
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    # Angle rotation as correction
    theta = correction['theta'] * math.pi / 180.
    d_vector_x_corr = d_vector_x * math.cos(theta) - d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) + d_vector_x * math.sin(theta)

    length = math.sqrt( d_vector_x_corr**2 + d_vector_y_corr**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x_corr/length,
                'd_vector_y' : d_vector_y_corr/length
            }

def HR_baseplate_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

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

########################################################
# HD Bottom
########################################################
def HB_pcb_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF pcb
    # direction vector = M1 - M4
    d_vector_x = module_offsets_raw[side]['pcb']['x']['FD3'] - module_offsets_raw[side]['pcb']['x']['FD1']
    d_vector_y = module_offsets_raw[side]['pcb']['y']['FD3'] - module_offsets_raw[side]['pcb']['y']['FD1']

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

def HB_sensor_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF sensor
    # direction vector = M26 - M3
    d_vector_x = module_offsets_raw[side]['sensor']['x']['M14'] - module_offsets_raw[side]['sensor']['x']['M25']
    d_vector_y = module_offsets_raw[side]['sensor']['y']['M14'] - module_offsets_raw[side]['sensor']['y']['M25']

    # Always plus for x component
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    # Angle rotation as correction
    theta = correction['theta'] * math.pi / 180.
    d_vector_x_corr = d_vector_x * math.cos(theta) - d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) + d_vector_x * math.sin(theta)

    length = math.sqrt( d_vector_x_corr**2 + d_vector_y_corr**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x_corr/length,
                'd_vector_y' : d_vector_y_corr/length
            }

def HB_baseplate_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

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



########################################################
# LD Right
########################################################
def LR_pcb_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF pcb
    # direction vector = M1 - M4
    d_vector_x = module_offsets_raw[side]['pcb']['x']['FD2'] - module_offsets_raw[side]['pcb']['x']['FD4']
    d_vector_y = module_offsets_raw[side]['pcb']['y']['FD2'] - module_offsets_raw[side]['pcb']['y']['FD4']

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

def LR_sensor_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

    # HF sensor
    # direction vector = M26 - M3
    d_vector_x = module_offsets_raw[side]['sensor']['x']['M7'] - module_offsets_raw[side]['sensor']['x']['M6']
    d_vector_y = module_offsets_raw[side]['sensor']['y']['M7'] - module_offsets_raw[side]['sensor']['y']['M6']

    # Always plus for x component
    if d_vector_x < 0.:
        d_vector_x = - d_vector_x
        d_vector_y = - d_vector_y

    # Angle rotation as correction
    theta = correction['theta'] * math.pi / 180.
    d_vector_x_corr = d_vector_x * math.cos(theta) - d_vector_y * math.sin(theta)
    d_vector_y_corr = d_vector_y * math.cos(theta) + d_vector_x * math.sin(theta)

    length = math.sqrt( d_vector_x_corr**2 + d_vector_y_corr**2 )

    # Return unit vector
    return {
                'd_vector_x' : d_vector_x_corr/length,
                'd_vector_y' : d_vector_y_corr/length
            }

def LR_baseplate_d_vector_finder( module_offsets_raw:dict, side:str, correction = None ) -> dict :

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
