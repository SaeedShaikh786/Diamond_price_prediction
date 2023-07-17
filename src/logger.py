import logging 
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"    ## log file is of current date and time 
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)    # we join path for current work dir and our log file

# here up ^  "logs" is for making folder is not exists then log_path is to join all the dir and log folder 
# and file name

os.makedirs(logs_path,exist_ok=True)   # we make dir as mention above 

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)  # we creat a files under same folder 

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



