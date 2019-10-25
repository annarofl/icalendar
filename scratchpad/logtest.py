import logging
import logging.config
import os
import yaml
# import json


def setup_logging(
    default_path='logging.yml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
#    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
#    logging.config.dictConfig(json.load(open("logging.json", "r")))
#    logging.basicConfig(filename="logs/main.log",level=logging.DEBUG,format='%(asctime)s: %(message)s')
#    logging.basicConfig(filename="logs/main.log",level=logging.DEBUjsonrmat='%(asctime)s: %(message)s')

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info(f"setting up Match")


if __name__ == '__main__':
    main()
