# Brady Nahkala
# Date modified: 2020 AUG 18
# Purpose: Iteratively run AnnAGNPS models of prairie potholes 
# to output nutrient data in the wetland sim file output for 
# future analysis of the 2016-2018 data by an ABE undergrad
# 
# =============================================================

import os
import platform
import sys
import shutil
import subprocess
from datetime import time
from datetime import date
from datetime import datetime
import numpy
import scipy
from scipy import stats
from statistics import stdev


# SETUP=======================================================

pothole_name = ["Bunny"]
pothole_ID = "B"        # Walnut = W; Cardinal = C; Lettuce = L; Gravy = G; Hen = H; Plume = P; Mouth = M
wetland_area_ha = 5.35   # from calibration, selected Method 4, MaxA delineation
wetland_area_m2 = wetland_area_ha * 10000
max_depth = 1000 #mm

# NUTRIENT PARAMS
scenario_numerical = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
Fr = [100, 150, 200, 250]
k = [0.1, 0.2, 0.3, 0.4, 0.5]

# REFERENCE INFILTRATION VALUE (mm/day)
inf_ref = 75

# FILE NAMES
wetlandin_filename = "C:/AGNPS_Watershed_Studies/Bunny_Nutrient_Model/4_Editor_DataSets/CSV_Input_Files/watershed/AnnAGNPS_Wetland_Data_Section.csv"
wetSIM_filename = 'C:/AGNPS_Watershed_Studies/Bunny_Nutrient_Model/5_AnnAGNPS_DataSets/AnnAGNPS_SIM_Wetland_Effects.csv'
RCN_filename = "C:/AGNPS_Watershed_Studies/Bunny_Nutrient_Model/4_Editor_DataSets/CSV_Input_Files/general/Runoff_Curve_Number_Data_Input_Editor_v5.5_Format.csv"
fert_filename = "C:/AGNPS_Watershed_Studies/Bunny_Nutrient_Model/4_Editor_DataSets/CSV_Input_Files/general/fertapp.csv"

# START AND END DATES IN GREGORIAN DAYS (Wetland sim file output)
# dates currently confirmed for Bunny only
start16 = 736104 # 05/20/2016 
end16 = 736246 # 10/9/2016

start17 = 736458 # 05/09/2017
end17 = 736593 # 09/21/2017

start18 = 736838 # 05/24/2018
end18 = 736985 # 10/18/2018

# METADATA/CONSTANTS SETUP =================================================

# WETLAND CSV INPUT FILE
headerw = "Wetland_ID,Reach_ID,Wetland_Area,Initial_Water_Depth,Min_Water_Depth,Max_Water_Depth,Water_Temperature,Potential_Daily_Infiltration,Weir_Coef,Weir_Width,Weir_Height,Soluble_N_Conc,Nitrate-N_Loss_Rate,Nitrate-N_Loss_Rate_Coef,Temperature_Coef,Weir_Exp,Input_Units_Code\n"
headerf = "Application_ID, Name_ID, Application_Rate, Depth, Mixing_Code, Input_Units_Code\n"

# OUTPUT INCREMENTATION
scenario_counter = 0

# LOOP MAIN PROGRAM =============================================
# THIS RUNS LOOP WITHIN LOOP - AT EACH FERT RATE STEP IT LOOPS MULTIPLE k20 VALUES
y=0
z=0
for y in range (0, 3):
    rate = Fr[y]

    f = open(fert_filename, "w")
    f.write(headerf)
    fert_dat = "FERT, 10-10-10," + str(rate) + ",,,1"
    f.write(fert_dat)
    f.close()

    x=0
    for x in range (0, 4):
        k20 = k[x]
        # OPEN AND EDIT WETLAND INPUT CSV
        w = open(wetlandin_filename, "w")
        w.write(headerw)
        wetland_dat = "1,2," + str(wetland_area_ha) + ",0.,0.," + str(max_depth) + ",," + str(inf_ref) + ".,2.,10.,1.,,," + str(k20) + ",1.09,1.5,1"
        w.write(wetland_dat)
        w.close()

        # BATCH FILES
        name_batchdelete = "C:/AGNPS_Watershed_Studies/" + str(pothole_name[z]) + "_Nutrient_Model/0_Batch_files/0_delete_all_output_files_BAN.bat"
        name_exannagnps = "C:/AGNPS_Watershed_Studies/" + str(pothole_name[z]) + "_Nutrient_Model/0_Batch_files/3_execute_AnnAGNPS_BAN.bat"

        # EXECUTE 0_DELETE ALL OUTPUT FILES_BAN.BAT FILE
        subprocess.run(name_batchdelete)

        # EXECUTE ANNAGNPS .BAT FILE
        subprocess.run(name_exannagnps)
        
        # EXTRACT WETLAND SIM DATA
        # copy output file
        destination_filename = "C:/AGNPS_Watershed_Studies/Bunny_Nutrient_Model/99_Nutrients/AnnAGNPS_SIM_Wetland_Effects_" + str(pothole_name[z]) + "_" + str(scenario_counter) + ".csv"
        shutil.copyfile(wetSIM_filename, destination_filename)

        # increment
        scenario_counter = scenario_counter + 1 
       
    
