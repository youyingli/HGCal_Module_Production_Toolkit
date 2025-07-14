import os
os.environ['FRAMEWORK_PATH'] = './'
os.environ['PYTHONPATH'] = ''

from HGCal_Module_Production_Toolkit.scripts.offsets_calculator import offsets_calculator
from HGCal_Module_Production_Toolkit.scripts.make_accuracy_plot import make_accuracy_plot
from HGCal_Module_Production_Toolkit.scripts.make_flatness import flat_and_thick_ness_finder
from HGCal_Module_Production_Toolkit.utils.io_tool import write_to_csv
#{
#    "320MHF2WCNT0096" : {
#
#        "center_offsets" : {
#            "pcb" : [8, 9],
#            "sensor" : [7, 8]
#            },
#
#        "angle_offsets" : {
#            "pcb" : 2,
#            "sensor" : 3
#            },
#
#        "flatness" : 33,
#        "thickness" : 22,
#        "Max_height" : 3,
#        "Min_height" : 3
#
#    }
#
#
#}

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
        offsets_list += offsets

    make_accuracy_plot([offsets_list], os.getenv('FRAMEWORK_PATH') + '/out')

    # Flatness and thickness
    # ----------------------------------------------------------

    for module, inputs in flatness_inputs:
        qc_data[module].update( flat_and_thick_ness_finder(modules, txtfile)[module] )
        qc_data[module].update( flat_and_thick_ness_finder(modules, txtfile, isVacuum=True)[module] )

    write_to_csv(qc_data, os.getenv('FRAMEWORK_PATH') + f'/out/output_{tag}.csv')

if __name__ == '__main__':


    offsets_inputs = [

        (["320MHF2WCNT0096-AT07-R", "320MHF2WCNT0097-AT07-L"], "M163M164.txt"),
        (["320MHF2WCNT0098-AT07-R", "320MHF2WCNT0099-AT07-L"], "M165M166.txt"),

    ]


    flatness_inputs = [

        ("320MHF2WCNT0096-AT07-R", ["M163M164.txt",""]),
        ("320MHF2WCNT0096-AT07-R", ["M163M164.txt",""]),
        ("320MHF2WCNT0096-AT07-R", ["M163M164.txt",""]),
        ("320MHF2WCNT0096-AT07-R", ["M163M164.txt",""]),

    ]

    main(offsets_inputs, flatness_inputs, tag = 'test')
