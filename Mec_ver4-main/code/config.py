# import os
# from pathlib import Path

# LINK_PROJECT = Path(os.path.abspath(__file__))
# LINK_PROJECT = LINK_PROJECT.parent.parent
# #print(LINK_PROJECT)
# DATA_DIR = os.path.join(LINK_PROJECT, "data")
# RESULT_DIR = os.path.join(LINK_PROJECT, "result/result1/")
# DATA_TASK = os.path.join(LINK_PROJECT, "data_task/data1000")


# NUM_TASKS_PER_TIME_SLOT = 2600
# NUM_VEHICLE = 5

# COMPUTATIONAL_CAPACITY_900 = 2  # Ghz
# COMPUTATIONAL_CAPACITY_901 = 2  # Ghz
# COMPUTATIONAL_CAPACITY_902 = 2  # Ghz
# COMPUTATIONAL_CAPACITY_903 = 2
# COMPUTATIONAL_CAPACITY_904 = 2
# COMPUTATIONAL_CAPACITY_905 = 2
# COMPUTATIONAL_CAPACITY_906 = 2
# COMPUTATIONAL_CAPACITY_907 = 2
# COMPUTATIONAL_CAPACITY_LOCAL = 4  # Ghz
# COMPUTATIONAL_CAPACITY_CLOUD = 4  # Ghz
# TRANS_RATE_EDGE_TO_CLOUD = 1  # Mbps
# CHANNEL_BANDWIDTH = 20  # MHz
# # List_COMPUTATION = [COMPUTATIONAL_CAPACITY_900, COMPUTATIONAL_CAPACITY_901, COMPUTATIONAL_CAPACITY_902,
# #                     COMPUTATIONAL_CAPACITY_903, COMPUTATIONAL_CAPACITY_904, COMPUTATIONAL_CAPACITY_905,
# #                     COMPUTATIONAL_CAPACITY_906, COMPUTATIONAL_CAPACITY_907, COMPUTATIONAL_CAPACITY_LOCAL]
# # Pr = 46 # dBm
# Pr = 46
# P = 39.810  # mW
# SIGMASquare = 100  # dBm   background noise power
# PATH_LOSS_EXPONENT = 4  # alpha
# NUM_EDGE_SERVER = NUM_VEHICLE + 1  # a server + vehicles
# List_COMPUTATION = [COMPUTATIONAL_CAPACITY_900] * \
#     NUM_VEHICLE + [COMPUTATIONAL_CAPACITY_LOCAL]
# NUM_STATE = NUM_EDGE_SERVER * 2 + 2
# NUM_ACTION = NUM_EDGE_SERVER + 1  # including cloud, must + 1
# # NUM_ACTION = NUM_EDGE_SERVER # no BS or no cloud
# # NUM_ACTION = NUM_EDGE_SERVER
# SCAILING_CO_EFFICIENT = 1
# FILE_NAME = "Not change"
# NB_STEPS = NUM_TASKS_PER_TIME_SLOT * 121
# # NB_STEPS = 405000




# # NUM_EDGE_SERVER = 6
# # NUM_VEHICLE =  5
# # CHANNEL_BANDWIDTH = 20  # MHz
# # TRANS_RATE_EDGE_TO_CLOUD = 1  # Mbps
# # SIGMASquare = 100  # dBm   background noise power
# # PATH_LOSS_EXPONENT = 4  # alpha
# # Pr = 46 
# # P = 39.810 #mW
# # NUM_ACTION = 7

# class Config:
#     Pr = 46
#     Pr2 = 24
#     Wm = 20
#     #n_unit_in_layer=[16, 32, 32, 8]
#     n_unit_in_layer=[32, 32, 16]
#     length_hidden_layer = len(n_unit_in_layer)
 
 
#-------------------------------------------------   
import os
from pathlib import Path

LINK_PROJECT = Path(os.path.abspath(__file__))
LINK_PROJECT = LINK_PROJECT.parent.parent
#print(LINK_PROJECT)
DATA_DIR = os.path.join(LINK_PROJECT, "data")
RESULT_DIR = os.path.join(LINK_PROJECT, "result/result1/")
DATA_TASK = os.path.join(LINK_PROJECT, "data_task/data1000")

NUM_VEHICLE = 5
# NUM_ACTIONS = 4
NUM_ACTIONS = 6
COMPUTATIONAL_CAPACITY_900 = 2  # Ghz
COMPUTATIONAL_CAPACITY_901 = 2  # Ghz
COMPUTATIONAL_CAPACITY_902 = 2  # Ghz
COMPUTATIONAL_CAPACITY_903 = 2
COMPUTATIONAL_CAPACITY_904 = 2
COMPUTATIONAL_CAPACITY_905 = 2
COMPUTATIONAL_CAPACITY_906 = 2
COMPUTATIONAL_CAPACITY_907 = 2
COMPUTATIONAL_CAPACITY_LOCAL = 4
CHANNEL_BANDWIDTH = 20

List_COMPUTATION = [COMPUTATIONAL_CAPACITY_900] * \
    NUM_VEHICLE + [COMPUTATIONAL_CAPACITY_LOCAL]
Pr = 46 
P = 39.810
SIGMASquare = 100
PATH_LOSS_EXPONENT = 4 
NUM_EDGE_SERVER = NUM_VEHICLE + 1
NUM_STATE = NUM_EDGE_SERVER*2+1
NUM_ACTION = NUM_EDGE_SERVER 
SCAILING_CO_EFFICIENT = 1 
FILE_NAME = "Not change"


class Config:
    Pr = 46
    Pr2 = 24
    Wm = 10
    #n_unit_in_layer=[16, 32, 32, 8]
    n_unit_in_layer=[32, 32, 16]
    length_hidden_layer = len(n_unit_in_layer)
    
    
    
# import os
# from pathlib import Path

# LINK_PROJECT = Path(os.path.abspath(__file__))
# LINK_PROJECT = LINK_PROJECT.parent.parent
# #print(LINK_PROJECT)
# DATA_DIR = os.path.join(LINK_PROJECT, "data")
# RESULT_DIR = os.path.join(LINK_PROJECT, "result/result1/")
# DATA_TASK = os.path.join(LINK_PROJECT, "data_task/data1000")

# NUM_ACTIONS = 4
# class Config:
#     Pr = 46
#     Pr2 = 24
#     Wm = 10
#     #n_unit_in_layer=[16, 32, 32, 8]
#     n_unit_in_layer=[32, 32, 16]
#     length_hidden_layer = len(n_unit_in_layer)
    