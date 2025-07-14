import re
import csv

template = {
    "L" : {

        "pcb" : {
            "x" : [],
            "y" : []
        },
        "sensor" : {
            "x" : [],
            "y" : []
        }
    },
    "R" : {
        "pcb" : {
            "x" : [],
            "y" : []
        },
        "sensor" : {
            "x" : [],
            "y" : []
        }
    },
    "measured_ref" : {
        "x" : 0.,
        "y" : 0.
    },
    "measured_sup_ref" : {
        "x" : 0.,
        "y" : 0.
    }
}

def get_offsets_raw_from_textfile(filename:str) -> dict:

    module_offsets_raw = template.copy()

    with open(filename, 'r') as f:

        for line in f.readlines():

            # Catch measured reference points
            for coord in ['X', 'Y']:
                if line.find(f"TTT1.{coord}") != -1:
                    module_offsets_raw["measured_ref"][coord.lower()] = float( line.split()[3] )
                elif line.find(f"TTT2.{coord}") != -1:
                    module_offsets_raw["measured_sup_ref"][coord.lower()] = float( line.split()[3] )

            for side in ["L", "r"]:
                for material in ["sensor", "pcb"]:
                    for coord in ['X', 'Y']:
                        if re.search(f"{side}{material[0].capitalize()}[0-9].{coord}", line):
                            module_offsets_raw[side.capitalize()][material][coord.lower()].append(float(line.split()[3]))

    return module_offsets_raw

def get_flatness_raw_from_textfile(filename:str) -> tuple:

    x = []
    y = []
    z = []

    with open(filename) as f:
        for line in f.readlines():
            if line.find('Focus1') != -1:
                line_list = line.split()
                x.append(line_list[2])
                y.append(line_list[3])
                z.append(line_list[4])

    x = np.array(x, dtype='float64')
    y = np.array(y, dtype='float64')
    z = np.array(z, dtype='float64')

    return x, y, z

def write_to_csv(module_qc_dict: dict, outfile: str, which:str ='all') -> None :

    module_list = []

    fields = [
            'module',
            'sensor_center_offset_x',
            'sensor_center_offset_y',
            'pcb_center_offset_x',
            'pcb_center_offset_y',
            'sensor_angle_offset',
            'pcb_angle_offset',
        ]

    for module_name, module_qc in module_qc_dict.items():

        module_list.append({
            fields[0] : module_name,
            fields[1] : module_qc['center_offsets']['sensor'][0],
            fields[2] : module_qc['center_offsets']['sensor'][1],
            fields[3] : module_qc['center_offsets']['pcb'][0],
            fields[4] : module_qc['center_offsets']['pcb'][1],
            fields[5] : module_qc['angle_offsets']['sensor'],
            fields[6] : module_qc['angle_offsets']['pcb']
            })

    with open(outfile, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for row in module_list:
            writer.writerow(row)
