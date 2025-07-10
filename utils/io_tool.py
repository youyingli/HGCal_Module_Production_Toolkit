import re

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

            for side in ["L", "r"]:
                for material in ["sensor", "pcb"]:
                    for coord in ['X', 'Y']:
                        if re.search(f"{side}{material[0].capitalize()}[0-9].{coord}", line):
                            module_offsets_raw[side.capitalize()][material][coord.lower()].append(float(line.split()[3]))

    return module_offsets_raw


def write_to_csv(module_qc_dict: dict, outfile: str) -> None :

    module_list = []

    fields = [
            'module',
            'sensor_center_offset_x',
            'sensor_center_offset_y',
            'pcb_center_offset_x',
            'pcb_center_offset_y'
        ]

    for module_name, module_qc in module_qc_dict.items():

        module_list.append({
            fields[0] : module_name,
            fields[1] : module_qc['center_offsets']['sensor'][0],
            fields[2] : module_qc['center_offsets']['sensor'][1],
            fields[3] : module_qc['center_offsets']['pcb'][0],
            fields[4] : module_qc['center_offsets']['pcb'][1]
            })

    with open(outfile, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for row in module_list:
            writer.writerow(row)
