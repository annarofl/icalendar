import logging
import logging.config
import yaml

def main():
    logging.config.dictConfig(yaml.load(open("logging.yml", "r")))
#    logging.basicConfig(filename="logs/main.log",level=logging.DEBUG,format='%(asctime)s: %(message)s')
 
    logger = logging.getLogger("gary")
    logger.info(f"setting up Match")

if __name__ == '__main__':
    main()
