# AUTHOR: Brady Nahkala
# TITLE: Graduate Research Assistant - ISU
# LAST REVISED: 09 MAR 2020
# PURPOSE: Using a database of alternative management files, cycle through 
# pothole management scenarios (ref 1) for multiple potholes. 
#
# Personal Reference: C:\AGNPS_Watershed_Studies\Model Development Manager.xlsx
#
# LAST CLEANED: 11 NOV 2020
# Commenting code. 
#
# =======================================================================
#
#
# LIBRARY =============================
import os
import platform
import sys
import shutil
import subprocess
import numpy
import scipy


# METADATA ===========================
pothole_names = ["Bunny"] # unique identifier
scenario_numerical = [0, 1, 2] # any number of scenarios you've built and want to run, listed here
scenario_name = ["NA"] # can give each scenario a name, for reference, as shown in examples below
#"Base", "Retired-All", "Conservation Tillage", "Retired-Pothole", "Improved Drainage 01","Improved Drainage 02", "Improved Drainage 03", 
# "Planting Date 01", "Planting Date 02", "Planting Date 03", "Planting Date 04", 
# "No-Till", "ConTillRetired", "NTillRetired", "ConTillDrain1", "ConTillDrain2", "ConTillDrain3", "Cover Crop"
# "BaseRetired", Improved Drainage 01 Retired","Improved Drainage 02 Retired", "Improved Drainage 03 Retired"

wetland_area_ha = 5.35   # from calibration, in hectares
wetland_area_m2 = wetland_area_ha * 10000 # square meters

# UNUSED ===
# d-A-V is linear below 0.1 m and second-order above 0.1 m
regression_transition_m = 0.1
regression_transition_m3 = 266.7
 # =========

# DATES and data array
# gregorian day for start and end of simulation (1994-2018, excluding 2-year spinup)
start = 727929
end = 737059
duration = end - start + 2

volume_data = numpy.empty([duration, 45]) # y value needs to be big enough to hold number of scenarios
depth_data = numpy.empty([duration, 45])

z = 0 # pothole id
for x in pothole_names:
    # POTHOLE FILE NAMES
    
    # controls simulation and aggregates inputs for AnnAGNPS
    master = "C:/AGNPS_Watershed_Studies/" + str(pothole_names[z]) + "_Alternatives/4_Editor_Datasets/CSV_Input_Files/annagnps_master.csv"
    
    # Output file for copying volumetric time series from each simulation run
    output_file = "C:/AGNPS_Watershed_Studies/Output_Database/"+ str(pothole_names[z]) + "/" + str(pothole_names[z]) + "_Output.csv"
    
    # AnnAGNPS generated output file after each run
    wetSIM_filename = "C:/AGNPS_Watershed_Studies/" + str(pothole_names[z]) + "_Alternatives/5_AnnAGNPS_DataSets/AnnAGNPS_SIM_Wetland_Effects.csv"
    
    for y in scenario_numerical: # run each scenario listed above
        # SCENARIO FILE NAMES
        header = "Data Section ID, File Name"
        annID = 'AnnAGNPS ID,.\simulation\\annaid.csv'
        cell = 'Cell Data,.\watershed\AnnAGNPS_Cell_Data_Section_' + str(y) + '.csv' # increment which cell file is used, land management data changed
        crop = "Crop Data,.\general\cropdata_RUSLE1.csv"
        cropg = "Crop Growth Data,.\general\crop_growth_RUSLE1.csv"
        glob = "Global IDs Factors and Flags Data,.\simulation\globfac.csv"
        mngf = "Management Field Data,.\general\AnnAGNPS_Management_Field_Data_" + str(y) + ".csv" # incrememnt management field data, becuase it changed (could have a single file with all possible schedules for your simulations)
        mngo = "Management Operation Data,.\general\AnnAGNPS_Management_Operation_Data_Template.csv"
        mngs = "Management Schedule Data,.\general\AnnAGNPS_Management_Schedule_Data_" + str(y) + ".csv" # same as management field data
        ncdat = "Non-Crop Data,.\general\AnnAGNPS_Non_Crop_Data_Section_2.csv"
        rch = "Reach Data,.\watershed\AnnAGNPS_Reach_Data_Section.csv"
        rcn = "Runoff Curve Number Data,.\general\Runoff_Curve_Number_Data_Input_Editor_v5.5_Format.csv"
        sim = "Simulation Period Data,.\simulation\sim_period.csv"
        soil = "Soil Data,.\general\soildat.csv"
        soill = "Soil Layer Data,.\general\soil_layers.csv"
        shed = "Watershed Data,.\watershed\watershed_data.csv"
        oog = "Output Options - Global,.\simulation\outopts_global.csv"
        ooaa = "Output Options - AA,.\simulation\outopts_aa.csv"
        oocsv = "Output Options - CSV,.\simulation\outopts_csv.csv"
        oodpp = "Output Options - DPP,.\simulation\outopts_dpp.csv"
        ooev = "Output Options - EV,.\simulation\outopts_ev.csv"
        oonpt = "Output Options - NPT,.\simulation\outopts_npt.csv"
        oosim = "Output Options - SIM,.\simulation\outopts_sim.csv"
        ootbl = "Output Options - TBL,.\simulation\outopts_tbl.csv"
        oomm = "Output Options - MN/MX,.\simulation\outopts_limits.csv"
        climst = "CLIMATE DATA - STATION,.\climate\climate_station.csv" 
        climd = "CLIMATE DATA - DAILY,.\climate\climate_daily.csv"
        wetland = "Wetland Data,.\watershed\AnnAGNPS_Wetland_Data_Section_" + str(y) + ".csv" # change wetland file for changes in drainage

        # write file references to master
        names = [header, annID, cell, crop, cropg, glob, mngf, mngo, mngs, ncdat, rch, rcn, sim, soil, soill, shed, oog, ooaa, oocsv, oodpp, ooev, oonpt, oosim, ootbl, oomm, climst, climd, wetland]
        w = open(master, "w").close()
        w = open(master, "w")
        # inputs
        n = 0
        for k in names:
            w.write(names[n] + "\n")
            n = n + 1
        w.close()

        # BATCH FILES - name them and specify directory
        name_batchdelete = "C:/AGNPS_Watershed_Studies/" + str(pothole_names[z]) + "_Alternatives/0_Batch_files/0_delete_all_output_files_BAN.bat"
        name_exannagnps = "C:/AGNPS_Watershed_Studies/" + str(pothole_names[z]) + "_Alternatives/0_Batch_files/3_execute_AnnAGNPS_BAN.bat"

        # EXECUTE 0_DELETE ALL OUTPUT FILES_BAN.BAT FILE
        subprocess.run(name_batchdelete)

        # EXECUTE ANNAGNPS .BAT FILE
        subprocess.run(name_exannagnps)
        
        # EXTRACT WETLAND SIM DATA
        # copy entire output file
        destination_filename = "C:/AGNPS_Watershed_Studies/Output_Database/" + str(pothole_names[z]) + "/AnnAGNPS_SIM_Wetland_Effects_" + str(pothole_names[z]) + "_" + str(y) + ".csv"
        shutil.copyfile(wetSIM_filename, destination_filename)
        
        #read output file
        wetread = numpy.genfromtxt(fname = wetSIM_filename, delimiter=',', usecols=numpy.arange(0,32), invalid_raise=False)
        
        # APPEND ALL SIM DATA to output_file location, for comparing simulations
        i = 4
        j = 0
        for m in range(11, 9865): # change based on date range
            if (wetread[m, 0] >= start and wetread[m, 0] <= end):
                volume_data[j, 0] = wetread[m, 0] 
                volume_data[j, 1] = wetread[m, 3]
                volume_data[j, 2] = wetread[m, 1]
                volume_data[j, 3] = wetread[m, 2]
                volume_data[j, i + int(y)] = wetread[m, 14] / 1000 * wetland_area_m2

                depth_data[j, 0] = wetread[m, 0] 
                depth_data[j, 1] = wetread[m, 3]
                depth_data[j, 2] = wetread[m, 1]
                depth_data[j, 3] = wetread[m, 2]

                #optional, automatic conversion from volume to depth using Martin, 2018 thesis
                # currently BROKEN
                #if volume_data[j, i + int(y)] >= regression_transition_m3:
                    #depth_data[j, i + int(y)] = 35202*(volume_data[j, i + int(y)])^2-7364.1*volume_data[j, i + int(y)]+651.08
                #else:
                    #depth_data[j, i + int(y)] = 2667*volume_data[j, i + int(y)]

                m = m + 1
                j= j + 1 
        numpy.savetxt(output_file, volume_data, delimiter=",") # save csv of time series from all model runs
    z = z + 1

