# Python automation for running mutliple scenario variations of the same watershed in AnnAGNPS
Scripts for running many AnnAGNPS models using separate input files. These scripts assume:
1. You have built and calibration an AnnAGNPS model. 
2. You have copied and modified any input files with changes in input parameters and they are stored as numbered files within the same input folder. 
3. You can are only interested in saving results from the Wetland_Sim output file. 

Scripts used to run 42 different land management scenarios for multiple prairie pothole models to assess their flood patterns over a 25-year simulation. All scenarios were built separately in csv format, and those csv files are looped via reference numbers. 

A script for running AnnAGNPS 11 year simulation while modifying fertilizer and k20 wetland nitrate decay rates in the model. This is the preliminary check to evaluate AnnAGNPS ability to model nutrient data, of which we have monitored samples from 2016-2018. 

Used in the following. 

Nahkala, B.A. (2020). Watershed modeling and random forest flood risk classification of farmed prairie potholes. Master's thesis. ISU Digital Repository. 19114. 

Nahkala, B.A., Kaleita, A.L., and Soupir, M.L. Characterization of prairie pothole inundation using AnnAGNPS under varying management and drainage scenarios. Agricultural Water Management. *In Review.* 
