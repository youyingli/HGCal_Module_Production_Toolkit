from HGCal_Module_Production_Toolkit.scripts.offsets_calculator import offsets_calculator
from HGCal_Module_Production_Toolkit.utils.make_accuracy_plot import make_accuracy_plot
{
    "320MHF2WCNT0096" : {

        "center_offsets" : {
            "pcb" : [8, 9],
            "sensor" : [7, 8]
            },

        "angle_offsets" : {
            "pcb" : 2,
            "sensor" : 3
            },

        "flatness" : 33,
        "thickness" : 22,
        "Max_height" : 3,
        "Min_height" : 3

    }


}


inputs = [

    (["320MHF2WCNT0096-AT07-R", "320MHF2WCNT0097-AT07-L"], "M163M164.txt"),
    (["320MHF2WCNT0098-AT07-R", "320MHF2WCNT0099-AT07-L"], "M165M166.txt"),

]

qc_data={}

for modules, txtfile in inputs:
    qc_data.update( offsets_calculator(modules, txtfile) )
print(qc_data)


offsets_list = []
for module, qc in qc_data.items():

    offsets = [
            module,
            qc['center_offsets']['sensor'][0],
            qc['center_offsets']['sensor'][1],
            qc['center_offsets']['pcb'][0],
            qc['center_offsets']['pcb'][1],
            0.03,
            0.03
            ]

    make_accuracy_plot([offsets], 'out' )
    offsets_list += offsets

make_accuracy_plot([offsets_list], 'out')

