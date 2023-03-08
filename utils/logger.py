import logging


logger = logging.getLogger("api_logs")
logger.setLevel(logging.INFO)
filehandler = logging.FileHandler("api.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
