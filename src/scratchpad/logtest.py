import logging
import logging.config
#import yaml
import json

def main():
#    logging.config.dictConfig(yaml.load(open("logging.yml", "r")))
    logging.config.dictConfig(json.load(open("logging.json", "r")))
#    logging.basicConfig(filename="logs/main.log",level=logging.DEBUG,format='%(asctime)s: %(message)s')
#    logging.basicConfig(filename="logs/main.log",level=logging.DEBUjsonrmat='%(asctime)s: %(message)s')
 
    logger = logging.getLogger("gary")
    logger.info(f"setting up Match")

if __name__ == '__main__':
    main()
