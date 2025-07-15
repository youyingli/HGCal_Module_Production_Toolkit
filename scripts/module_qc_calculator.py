import os
os.environ['FRAMEWORK_PATH'] = './'
os.environ['PYTHONPATH'] = ''
print(os.getenv('PYTHONPATH') )
from HGCal_Module_Production_Toolkit.scripts.offsets_calculator import offsets_calculator
from HGCal_Module_Production_Toolkit.scripts.make_accuracy_plot import make_accuracy_plot
from HGCal_Module_Production_Toolkit.scripts.flatness_calculator import flatness_calculator
from HGCal_Module_Production_Toolkit.utils.io_tool import write_to_csv


def main(offsets_inputs:list, flatness_inputs:list, tag:str = 'NoTag') -> None:

    os.system('mkdir -p ' + os.getenv('FRAMEWORK_PATH') + '/out')

    qc_data = {}

    # Offset
    # ----------------------------------------------------------
    for modules, txtfile in offsets_inputs:
        qc_data.update( offsets_calculator(modules, txtfile) )

    offsets_list = []
    for module, qc in qc_data.items():

        offsets = [
                module,
                qc['center_offsets']['sensor'][0],
                qc['center_offsets']['sensor'][1],
                qc['center_offsets']['pcb'][0],
                qc['center_offsets']['pcb'][1],
                qc['angle_offsets']['sensor'],
                qc['angle_offsets']['pcb']
                ]

        make_accuracy_plot([offsets], os.getenv('FRAMEWORK_PATH') + '/out' )
        offsets_list.append(offsets)

    make_accuracy_plot(offsets_list, os.getenv('FRAMEWORK_PATH') + '/out')

    # Flatness and thickness
    # ----------------------------------------------------------
    for module, txtfiles in flatness_inputs:
        m = module.split("-")[0]
        qc_data[m].update( flatness_calculator(module, txtfiles[0], isVacuum=True)[m] )
        qc_data[m].update( flatness_calculator(module, txtfiles[1])[m] )

    write_to_csv(qc_data, os.getenv('FRAMEWORK_PATH') + f'/out/output_{tag}.csv')

if __name__ == '__main__':


    offsets_inputs = [

        (["320MHF2WCNT0076-AT07-R", "320MHF2WCNT0077-AT07-L"], "M143M144.txt"),
        (["320MHF2WCNT0078-AT08-L", "320MHF2WCNT0079-AT08-R"], "M145M146.txt"),

    ]


    flatness_inputs = [

        ("320MHF2WCNT0076-AT07-R", ["M143M144-1.txt","M143M144-2.txt"]),
        ("320MHF2WCNT0077-AT07-L", ["M143M144-1.txt","M143M144-2.txt"]),
        ("320MHF2WCNT0078-AT08-L", ["M145M146-1.txt","M145M146-2.txt"]),
        ("320MHF2WCNT0079-AT08-R", ["M145M146-1.txt","M145M146-2.txt"]),

    ]

    main(offsets_inputs, flatness_inputs, tag = 'test')
