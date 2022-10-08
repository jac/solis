import logging
from . import metrics
from sys import exit
from time import sleep
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from pysolarmanv5.pysolarmanv5 import PySolarmanV5

metrics_dict = {}
def run(cfg):
    logging.info(f'Starting Web Server for Prometheus on port: {cfg.prom.port}')
    start_http_server(cfg.prom.port)

    REGISTRY.register(SolisCollector(cfg))
    while True:
        sleep(cfg.prom.scrape_interval)

class SolisCollector(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def collect(self):
        yield from scrape_solis(self.cfg)

def add_modified_metrics(custom_metrics_dict):
    met_pwr = custom_metrics_dict['meter_active_power_1'] - custom_metrics_dict['meter_active_power_2']
    total_load = custom_metrics_dict['house_load_power'] + custom_metrics_dict['bypass_load_power']

    # Present battery modified metrics
    if custom_metrics_dict['battery_current_direction'] == 0:
        metrics_dict['battery_power_modified'] = 'Battery Power(modified)', custom_metrics_dict['battery_power_2']
        metrics_dict['battery_power_in_modified'] = 'Battery Power In(modified)', custom_metrics_dict['battery_power_2']
        metrics_dict['battery_power_out_modified'] = 'Battery Power Out(modified)', 0
        metrics_dict['grid_to_battery_power_in_modified'] = 'Grid to Battery Power In(modified)', 0
    else:
        metrics_dict['battery_power_modified'] = 'Battery Power(modified)', custom_metrics_dict['battery_power_2'] * -1 # negative
        metrics_dict['battery_power_out_modified'] = 'Battery Power Out(modified)', custom_metrics_dict['battery_power_2']
        metrics_dict['battery_power_in_modified'] = 'Battery Power In(modified)', 0
        metrics_dict['grid_to_battery_power_in_modified'] = 'Grid to Battery Power In(modified)', 0

    if total_load < met_pwr and custom_metrics_dict['battery_power_2'] > 0:
        metrics_dict['grid_to_battery_power_in_modified'] = 'Grid to Battery Power In(modified)', custom_metrics_dict['battery_power_2']

    # Present meter modified metrics
    if met_pwr > 0:
        metrics_dict['meter_power_in_modified'] = 'Meter Power In(modified)', met_pwr
        metrics_dict['meter_power_modified'] = 'Meter Power(modified)', met_pwr
        metrics_dict['meter_power_out_modified'] = 'Meter Power Out(modified)', 0
    else:
        metrics_dict['meter_power_out_modified'] = 'Meter Power Out(modified)', met_pwr * - 1  # negative
        metrics_dict['meter_power_in_modified'] = 'Meter Power In(modified)', 0
        metrics_dict['meter_power_modified'] = 'Meter Power(modified)', met_pwr

    # Present load modified metrics
    metrics_dict['total_load_power_modified'] = 'Total Load Power(modified)', total_load

    if 0 < custom_metrics_dict['total_dc_input_power_2'] <= total_load:
        metrics_dict['solar_to_house_power_modified'] = 'Solar To House Power(modified)', custom_metrics_dict['total_dc_input_power_2']
    elif custom_metrics_dict['total_dc_input_power_2'] == 0:
        metrics_dict['solar_to_house_power_modified'] = 'Solar To House Power(modified)', 0
    elif custom_metrics_dict['total_dc_input_power_2'] > total_load:
        metrics_dict['solar_to_house_power_modified'] = 'Solar To House Power(modified)', total_load

    logging.info('Added modified metrics')


def scrape_solis(cfg):
    try:
        logging.info(f"Connecting to Solis Modbus @ {cfg.inverter.ip}:{cfg.inverter.port}")
        modbus = PySolarmanV5(cfg.inverter.ip, cfg.inverter.serial_num, port=cfg.inverter.port, mb_slave_id=1, verbose=cfg.debug)
    except Exception as e:
        logging.error(f"{repr(e)}. Exiting")
        exit(1)

    logging.info('Scraping...')

    for reg, reg_class in metrics.METRICS.items():
        for attempt in range(3):
            try:
                logging.debug(f"Scraping registers {reg} - length {reg_class.REGISTER_LENGTH}")
                regs = modbus.read_input_registers(register_addr=reg, quantity=reg_class.REGISTER_LENGTH)
                logging.debug(regs)
            except Exception as e:
                logging.error(f"Attempt {attempt} - Failed to read registers {reg}; Length: {reg_class.REGISTER_LENGTH}; Error {repr(e)}")
                if attempt == 3:
                    exit(1)
                sleep(3)
            break

        rc = reg_class()
        yield from rc.collect(regs)
        del rc

    

    # for r in registers.all_regs:
    #     # Convert time to epoch
    #     if reg == 33022:
    #         inv_year = '20' + str(regs[0]) + '-'
    #         if regs[1] < 10:
    #             inv_month = '0' + str(regs[1]) + '-'
    #         else:
    #             inv_month = str(regs[1]) + '-'
    #         if regs[2] < 10:
    #             inv_day = '0' + str(regs[2]) + ' '
    #         else:
    #             inv_day = str(regs[2]) + ' '
    #         if regs[3] < 10:
    #             inv_hour = '0' + str(regs[3]) + ':'
    #         else:
    #             inv_hour = str(regs[3]) + ':'
    #         if regs[4] < 10:
    #             inv_min = '0' + str(regs[4]) + ':'
    #         else:
    #             inv_min = str(regs[4]) + ':'
    #         if regs[5] < 10:
    #             inv_sec = '0' + str(regs[5])
    #         else:
    #             inv_sec = str(regs[5])
    #         inv_time = inv_year + inv_month + inv_day + inv_hour + inv_min + inv_sec
    #         logging.info(f'Solis Inverter time: {inv_time}')
    #         time_tuple = strptime(inv_time, '%Y-%m-%d %H:%M:%S')
    #         time_epoch = mktime(time_tuple)
    #         metrics_dict['system_epoch'] = 'System Epoch Time', time_epoch

    # Create modified metrics
    # if cfg.prom.modified:
    #     add_modified_metrics(custom_metrics_dict)
    logging.info('Scraped')