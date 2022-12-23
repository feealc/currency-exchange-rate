import logging
import sys
import os
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s :: %(levelname)-8s :: %(module)-15s :: %(message)s')

# stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# file
file_handler = logging.FileHandler(filename=os.path.join(Path(__file__).parent.parent, 'log', 'main_file.log'),
                                   encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
