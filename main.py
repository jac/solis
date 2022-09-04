import environ
import logging
import src

@environ.config(prefix="SOLIS")
class SolisConfig:
    @environ.config(prefix="PROM")
    class Prom:
        port = environ.var(18000, converter=int)
        scrape_interval = environ.var(30, converter=int)
        modified = environ.bool_var(True)

    @environ.config(prefix="INVERTER")
    class Inverter:
        serial_num = environ.var(converter=int)
        ip = environ.var()
        port = environ.var(8899, converter=int)

    prom = environ.group(Prom)
    inverter = environ.group(Inverter)

    debug = environ.bool_var(False)

if __name__ == '__main__':
    cfg = environ.to_config(SolisConfig)

    if cfg.debug:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG,
                            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('Starting')
    src.collector.run(cfg)