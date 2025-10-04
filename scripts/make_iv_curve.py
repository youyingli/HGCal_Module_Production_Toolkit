import psycopg
import yaml
import matplotlib.pyplot as plt
import numpy as np

def iv_data_query(cursor, module_name:str, is_lower_temp:bool = False) -> tuple:

    compare_symbol = '<' if is_lower_temp else '>'

    query = f"""
        SELECT program_v, meas_i, temp_c, rel_hum FROM public.module_iv_test
        WHERE module_name = %s AND (temp_c::REAL) {compare_symbol} 0.
    """
    cursor.execute(query, (module_name,))
    results = cursor.fetchall()

    if len(results) != 0:
        return results[-1]
    else:
        print(f'IV data for {module_name} does not exist at room temperature !')
        return None

def makeplot(module_name:str, modules_data_normal_temp:list, modules_data_lower_temp:list, islegend:bool = True) -> tuple:

    fig, ax = plt.subplots(figsize=(8.5, 5), layout='constrained')
    ax.grid()

    for voltage, current, temperature, humidity in modules_data_normal_temp:
        ax.plot(np.array(voltage), np.array(current)*(1e6), label = f'temperature = {temperature}, humidity = {humidity}', linestyle='-')

    for voltage, current, temperature, humidity in modules_data_lower_temp:
        ax.plot(np.array(voltage), np.array(current)*(1e6), label = f'temperature = {temperature}, humidity = {humidity}', linestyle=':')

    ax.set_title(f'{module_name} IV', fontdict={'fontsize':20})
    ax.set_xlabel('Voltage [V]',  fontsize=18)
    ax.set_ylabel('Current [$\mu$A]', fontsize=18)
    ax.set_yscale('log')
#    ax.xaxis.set_minor_locator(MultipleLocator(50))
    ax.set_ylim(0.0004, 100)
    #ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower right', ncol=2, borderaxespad=0.)
    #ax.legend(bbox_to_anchor=(1., 0., 1.1, .5), loc='lower right', borderaxespad=0.)
    if islegend:
        ax.legend(bbox_to_anchor=(1.01, 0., 0.25, .5), loc='lower left', borderaxespad=0.)
    plt.tick_params(axis='both', which='minor', direction='in', labelsize=0, length=5, width=1, right=True)
    plt.tick_params(axis='both', which='major', direction='in', labelsize=18, length=7, width=1.5, right=True)
    plt.savefig(f'{module_name}_IV.png')
    plt.savefig(f'{module_name}_IV.pdf')
    plt.close()

def make_iv_curve(modules: list, config) -> None:

    modules_data_normal_temp = []
    modules_data_lower_temp  = []

    for module_name in modules:

        with psycopg.connect(
            dbname   = config['database_name'],
            user     = config['user'],
            password = config['password'],
            host     = config['host'],
            port     = 5432
        ) as connection:
            with connection.cursor() as cursor:

                if data := iv_data_query(cursor, module_name, is_lower_temp=False):
                    modules_data_normal_temp.append( data )

                if data := iv_data_query(cursor, module_name, is_lower_temp=True):
                    modules_data_lower_temp.append( data )

        makeplot(module_name, modules_data_normal_temp[-1:], modules_data_lower_temp[-1:])

    makeplot('summary', modules_data_normal_temp, modules_data_lower_temp, islegend=False)


if __name__ == '__main__':

    modules = [
    "320MHF1W4NT0035",
    "320MHF1W4NT0036",
    "320MHF1W4NT0037",
    "320MHF1W4NT0038",
    "320MHF1W4NT0039",
    "320MHF1W4NT0040"
    ]
    make_iv_curve(modules, config)
