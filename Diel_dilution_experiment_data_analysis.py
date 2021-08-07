# Diel dilution experiment data analysis
# Use this notebook to analyze diel dilution experiment data 
# Author: Darcy Taniguchi, Alyssia Gonzalez, Sandra Morcos



# Other information

# Model 2 regression from https://github.com/OceanOptics/pylr2
# T-test info found at https://towardsdatascience.com/inferential-statistics-series-t-test-using-numpy-2718f8f9bf2f
# Here's a website showing how to do a paired t-test and also mentions the non-parametric Wilcoxon signed rank test https://pythonfordatascienceorg.wordpress.com/paired-samples-t-test-python/
# Can also look at what Anderson and Harvey (2019) Frontiers in Marine Science did--paired t-test
# Here is lots of info on p-values for linear regressions https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression

######### IMPORTANTLY: wherever it says "slope," it means slope (= -grazing rate).########## 

#######################################################
### Importing things ###
import numpy as np
import pandas as pd
from scipy import stats
from pylr2_master.pylr2 import regress2
import math
import statistics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt 
import statsmodels.api as sm

#######################################################
#### Functions to process data ###

# Putting data from a data frame into a dictionary
def data_in_dict(df, col_names):
    # This function puts the data from a data frame into a dictionary
    # df = dataframe (read from Excel typically)
    # col_names = names of columns want to include in dictionary
    
    # Output--dictionary of data from data frame specified in col_names
    data_dict = {} #dictionary with bottles as keys, values are list of dictionary of nutrient val, replicates, etc
        # Order of list is time point (init or final)
        # For example {1C: [data_timept0, data_timept1], 2C: [data_time0, data_time2], 3C:[data_time0, data,time1]}
    sample_num = df.Sample_No #samples numbers

    sample_num = sample_num.values.tolist()

    for b in sample_num: #going through each sample number, not each row because there are some rows that are notes
    # for b in [1,2,7,8,37,38,59,60]:
        if math.isnan(b): # if the sample number is nan, break out of the loop
            break
        data_temp = df[df.Sample_No.eq(b)] # Get all data for that sample number
        dict_temp = {}


        for c in col_names: #Go through columns of interest and put into dictionary
            temp = data_temp[c]
            temp2 = temp.values.tolist()
            dict_temp[c] = temp2[0]


        #dict_temp['Expt_num'] = expt_num# Adding in experiment number to dictionary

        bot_num_temp = data_temp.Bottle_number
        bot_num = bot_num_temp.to_string(index=False)
        bot_num = bot_num.strip()

        ###### The code below organizes dictionary by bottle numbers, which works if each experiment is read in separately
        if bot_num in data_dict.keys(): #If bottle already exist in outer dictionary
            list_temp = data_dict.get(bot_num) # Get values from outer dict with key as bottle number
            list_temp.append(dict_temp) #add new value to end of list
            data_dict[bot_num] = list_temp #make longer list value in outer dict

        else: #bottle not in dictionary, must make list of dict and put in outer dict
            list_temp = [dict_temp]
            data_dict[bot_num] = list_temp
        
        ###### The code below organizes dictionary so each key is an experiment, which works better if all experiments are in one worksheet
#        expt_num_temp = data_temp.Expt_num
#        expt_num = expt_num_temp.to_string(index=False)
#        expt_num = expt_num.strip()
#        if expt_num in data_dict.keys(): #If experiment number already exists in outer dictionary
#            list_temp = data_dict.get(expt_num)# get values from outer dictionary with key as experiment number
#            list_temp.append(dict_temp) # add new value to end of list
#            data_dict[expt_num] = list_temp # make longer list value in outer dictionary
#        else: #experiment not in dictionary, must make list of dict and put in outer dict
#            list_temp = [dict_temp]
#            data_dict[expt_num] = list_temp
            
    return data_dict


## Finding dilution fraction and putting in dictionary with keys as bottles, values as dilution fraction

def dil_frac_calc(df):
    #Uses the average of the initial, undiluted samples as the denominator to find the dilution fraction
    #Initial samples
    init_undil = df[df.Time_point.eq(0) & df.Fraction_whole_seawater.eq(1)] #initial undiluted samples, for dil frac
    init = df[df.Time_point.eq(0)] #all initial data

    init_undil_all = init_undil['pro_per_mL'] + init_undil['syn_per_mL'] + init_undil['peuk_per_mL'] + init_undil['hbact_per_mL']# Summing all cell types
    ave_undil = np.mean(init_undil_all)

    dil_dict = {}
    bot_init = init.Bottle_number

    for jjj in bot_init:
        dtemp = init[init.Bottle_number.eq(jjj)]
        temp_val = dtemp.Fraction_whole_seawater
        temp_val = temp_val.tolist()
        # Use the following lines if want to just make the undiluted ones exaclty 1
        if temp_val[0] == 1.0:
            dil_dict[jjj] = 1.0
        else:
            init_count = dtemp['pro_per_mL'] + dtemp['syn_per_mL'] + dtemp['peuk_per_mL'] + dtemp['hbact_per_mL']
            dil_frac_temp = init_count/ave_undil
            df_temp = dil_frac_temp.tolist()
            dil_dict[jjj] = df_temp[0]


         # Use the lines down below if want to make undiluted fractions the fraction of the average
    #     init_count = dtemp['pro_per_mL'] + dtemp['syn_per_mL'] + dtemp['peuk_per_mL'] + dtemp['hbact_per_mL']
    #     dil_frac_temp = init_count/ave_undil
    #     df_temp = dil_frac_temp.tolist()
    #     dil_dict[jjj] = df_temp[0]
    return dil_dict

###use this function to find growth rate (3 rates, day, night, 24hr) use time in days
def k_calc (time, init_cell, fin_cell): #Calculates apparent growth rate k in units of time
    # time is amount of time incubation was run, typically in units of days
    #init_cell is initial cell concentration, units of cells per volume
    # fin_call is final cell concentration, units of cells per volume
    k = (1/time) * (np.log(fin_cell/init_cell))
    return k

###this is dealing with replicate experiments (below)
def k_calc_from_rep(x,r1,r2,t1,t2,inc_time):
    # This function calculates the apparent growth rate for Prochlorococcus, Synechococcus, 
        #pico-eukaryotes, heterotrophic bacteria, all photosynthetic cells (i.e., everything except het. bac)
        # and all cells combined
    # let d be the dict, r1 be first replicate number, r2 be second replicate number, 
    # t1 be a time point that goes with rep 1, t2 be another time point that goes with rep 2, 
    # inc_time be incubation time, typically units in days
    
    # Make sure t1 < t2
    if t1 > t2:
        ttemp = t1
        t1 = t2
        t2 = ttemp
        
        rtemp = r1
        r1 = r2
        r2 = rtemp
    
    dict_out = {}
    output_list = []
    for key, l in x.items(): # going through list in outer dictionary
        for d1 in l:
            if d1['Replicate'] == r1 and d1['Time_point'] == t1:
                # found first dict d with replicate number r1 and time point t1
                # now find the first dict with replicate number r2 and time point t2
                for key2, l2 in x.items():
                    for d2 in l2:
                        if d2['Replicate'] == r2 and d2['Time_point'] == t2: # found second dict d2
                            
                            # Finding particular samples in each dictionary with same dil frac and nutrient amendment
                            if d1['Fraction_whole_seawater'] == d2['Fraction_whole_seawater'] and d1['Nutrients_1'] == d2['Nutrients_1']:
                                    # Get cell values from each dictionary d
                                    pro1 = d1['pro_per_mL']
                                    syn1 = d1['syn_per_mL']
                                    peuk1 = d1['peuk_per_mL']
                                    hbact1 = d1['hbact_per_mL']
                                    all_photo1 = pro1 + syn1 + peuk1
                                    all1 = all_photo1 + hbact1
                                    
                                    # Get cell values from each dictionary d2
                                    pro2 = d2['pro_per_mL']
                                    syn2 = d2['syn_per_mL']
                                    peuk2 = d2['peuk_per_mL']
                                    hbact2 = d2['hbact_per_mL']
                                    all_photo2 = pro2 + syn2 + peuk2 
                                    all2 = all_photo2 + hbact2
                                    
                                    
                                    # call k_calc (time, init_cell, fin_cell)
                                    dict_out['k_pro'] = k_calc(inc_time, pro1, pro2)                                  
                                    dict_out['k_syn'] = k_calc(inc_time, syn1, syn2)
                                    dict_out['k_peuk'] = k_calc(inc_time, peuk1, peuk2)
                                    dict_out['k_hbact'] = k_calc(inc_time, hbact1, hbact2)
                                    dict_out['k_photo'] = k_calc(inc_time, all_photo1, all_photo2)
                                    dict_out['k_all'] = k_calc(inc_time, all1, all2)
                                    
                                    dict_out['Replicate1'] = d1.get('Replicate')
                                    dict_out['Replicate2'] = d2.get('Replicate')
                                    dict_out['Time_point1'] = d1.get('Time_point')
                                    dict_out['Time_point2'] = d2.get('Time_point')
                                    dict_out['Bottle_number1'] = key
                                    dict_out['Bottle_number2'] = key2
                                    dict_out['Nutrients_1'] = d2.get('Nutrients_1')#should be same for both dict
                                    dict_out['Fraction_whole_seawater'] = d2.get('Fraction_whole_seawater')#should be same for both dict
                                    output_list.append(dict_out.copy())
                    
    return  output_list             
    

    #### Below are functions that keep replicate sets separate  
### (i.e, there will be 1 slope and 1 intercept per set of replicates, 
##so if did 2 replicate experiments, get 2 slope, 2 intercepts)

def model_2_reg_rep_sep(data, dil_dict, expt_num, k_names, intercept_names, slope_names):
    # This function takes:
        #data = output from k_calc_from_rep, a list of lists of dictionaries
        # dil_dict = dictionary of dilution fractions for each bottle
        # expt_num = the experiment number
        # k_names = names of apparent growth rates for different cell types, which are also keys in data
        # intercept_names = names of what want intercept values to be called for different cell types
        # slope_name = names of what want slope values to be called for different cell types
        
    # Output of this function is, for each cell type (pro, syn, peuk, hbact, photosynthesizers, all cells):
        # slope, intercept, std of slope, std of intercept, prediction array, r value FOR EACH REPLICATE PAIR
    # Output is in the form of a list of dictionaries, where for each replicate experiment, have dictionary of
        #regression value for each cell type and expt. number and no nutrient growth (= k_no_nut + grazing rate)
        

    # list for regression and apparent rates
    rate_list = []

    for l in k_data: # going through each item in list
        dict_temp = {} # for regression info and metadata


        k_new_list=[] # for names of k_no_nut values for all cell types
        # Lists for all k values
        k_pro = []
        k_syn = []
        k_peuk = []
        k_hbact = []
        k_photo = []
        k_all = []

        # lists for dilution fractions
        dil_temp = []

        for d in l: # going through each dictionary in inner list 
            if d.get('Nutrients_1') == 1: # only want nutrient amended samples for regression

                k_pro.append(d.get('k_pro'))
                k_syn.append(d.get('k_syn'))
                k_peuk.append(d.get('k_peuk'))
                k_hbact.append(d.get('k_hbact'))
                k_photo.append(d.get('k_photo'))
                k_all.append(d.get('k_all'))

                bot = d.get('Bottle_number1') # bottle 1 associated with k values
                dil_temp.append(dil_dict.get(bot))# the real dilution fraction associated with bottle 1

            else: # non-nutrient amended sample
                for kn in k_names:
                    k_new = kn+'_no_nut'
                    k_new_list.append(k_new)
                    dict_temp[k_new] = d.get(kn) # put values in dictionary


        ### Regression code
        dil = np.array(dil_temp) #change to numpy array for regression function

        all_k_type = [k_all, k_pro, k_syn, k_peuk, k_hbact, k_photo]
        suffix = ['_all','_pro','_syn','_peuk','_hbact','_photo']
        reg_final = {} # Final regression values for all cell types


        for kk,sf,kno in zip(all_k_type, suffix,k_new_list): # going through k types and suffixes
                reg = regress2(dil, np.array(kk)) # model 2 regressions
                reg2 = reg.copy()
                for dd in reg.keys():
                    reg2[dd+sf] = reg2.pop(dd)
                reg_final.update(reg2)

                reg_final['growth_no_nut'+sf] = dict_temp.get(kno) - reg.get('slope') #remebering grazing = -slope


        ### Combining dictionaries of regression and no-nutrient samples
        reg_final['expt_num']=expt_num # adding to dictionary the experiment number
        reg_final.update(dict_temp) # Combine dictionary from regression with dictionay of non-nutrient k values

        rate_list.append(reg_final)
    
    return rate_list
    

### paired t-test info
def paired_t_rep_sep(rate_list, intercept_names, k_no_nut_names, k_names, expt_num):
    # This function performs a paired t test of regression intercept (= nutrient-amended growth rate)
        # and non-nutrient-amended apparent growth rate (k0)
    # The comparison are within a complete replicate, meaning for every intercept there is one k0 value
    # Thus, there are as many k0 and intercepts as there are replicate experimetns
    
    # rate_list = data of apparent growth rates, output from model_2_reg_reps_sep
    # intercept names = list of string of names of intercepts for all cell types (which are also names of 
        # keys in rate_list)
    # k_no_nut_names = list of string of names of apparent growth rates without nutrient addition (also names
        # of keys in rate_list)
    # k_names = list of strings of k values to be used to name keys in output
    # expt_num = experiment number
    
    # Output -- list of dictionary of p values and associated statistics
    
    paired_t_dict_pval = {}
    paired_t_dict_stat = {}

    for i,k,jj in zip(intercept_names, k_no_nut_names, k_names):
        int_list = []
        k_no_nut_list = []
        for r in rate_list:
            int_list.append(r.get(i))
            k_no_nut_list.append(r.get(k))

        paired_t = stats.ttest_rel(int_list,k_no_nut_list)
        paired_t_dict_pval[jj+'_pval'] = paired_t.pvalue
        paired_t_dict_pval['expt_num'] = expt_num
        paired_t_dict_stat[jj+'_stat'] = paired_t.statistic
        paired_t_dict_stat['expt_num'] = expt_num

    return [paired_t_dict_pval, paired_t_dict_stat]
    

### Taking average of rates and finding standard error (se = stdev/sqrt(n) for n the number of samples)


def rate_ave(rate_list, intercept_names, k_no_nut_names, slope_names, expt_num):
    # This function takes average of growth, grazing, and nutrient-amended growth and also finds standard error
    
    # Input
    # rate_list = data of apparent growth rates, output from model_2_reg_reps_sep
    # intercept names = list of string of names of intercepts for all cell types (which are also names of 
        # keys in rate_list)
    # k_no_nut_names = list of string of names of apparent growth rates without nutrient addition (also names
        # of keys in rate_list)
    # slope_names = list of strings of slope values to be used to name keys in output
    # expt_num = experiment number
    
    # Output
    # dictionary of average of slope values (NEED TO TAKE NEGATIVE TO GET GRAZING RATE), slope standard error, 
        # intercept average, intercept standard error, no-nutrient growth average, and no-nutrient growth se

    rate_ave_dict = {}

    for i,k,s in zip(intercept_names, k_no_nut_names, slope_names):
        int_list = []
        k_no_nut_list = []
        slope_list = []
        for r in rate_list:
            int_list.append(r.get(i))
            k_no_nut_list.append(r.get(k))
            slope_list.append(r.get(s))

        int_ave = statistics.mean(int_list)
        int_se = (statistics.stdev(int_list, xbar = int_ave))/math.sqrt(len(int_list))
        rate_ave_dict[i] = int_ave
        rate_ave_dict[i+'_se'] = int_se

        slope_ave = statistics.mean(slope_list) 
        slope_se = (statistics.stdev(slope_list, xbar = slope_ave))/math.sqrt(len(slope_list))
        rate_ave_dict[s] = slope_ave
        rate_ave_dict[s+'_se'] = slope_se

        k_no_nut_ave = statistics.mean(k_no_nut_list)
        k_no_nut_se = (statistics.stdev(k_no_nut_list, xbar = k_no_nut_ave))/math.sqrt(len(k_no_nut_list))
        rate_ave_dict[k] = k_no_nut_ave
        rate_ave_dict[k+'_se'] = k_no_nut_se

        rate_ave_dict['expt_num'] = expt_num
        
    return rate_ave_dict

    ## Puting values for comparison of nutrient and no nutrient amended apparent growth rates in dif. lists,in order

def nut_no_nut (data):
    # data is list of lists of dictionary of apparent growth rate with metadata output from k_calc_from_rep
    # Output of function is dictionary of different cell types with values of dictionaries of lists
        # of nutrient and non-nutrient amended apparent growth rates, with lists in order of comparison
    data_nut_no_nut = {}

    nut_pro_temp = []
    no_nut_pro_temp = []
    nut_syn_temp = []
    no_nut_syn_temp = []
    nut_peuk_temp = []
    no_nut_peuk_temp =[]
    nut_hbact_temp = []
    no_nut_hbact_temp = []
    nut_photo_temp = []
    no_nut_photo_temp = []
    nut_all_temp = []
    no_nut_all_temp = []

    for l in data:
        for d in l:
            if d['Nutrients_1'] == 0 and d['Fraction_whole_seawater'] == 1:# if no nut and undiluted
                rep1 = d.get('Replicate1')
                rep2 = d.get('Replicate2')
                t1 = d.get('Time_point1')
                t2 = d.get('Time_point2')            

                for d2 in l:
                    if d2['Nutrients_1'] ==1 and d2['Fraction_whole_seawater'] == 1: #nutrients and undiluted

                        #Make sure replicates and time points match for nutrient and non-nutrient samples
                        if rep1 == d2.get('Replicate1') and rep2 == d2.get('Replicate2') and \
                        t1 == d2.get('Time_point1') and t2 == d2.get('Time_point2'):

                            # Now we know are dealing with same replicates and time points, add values to list
                            # Append to nutrient list for pro
                            nut_pro_temp.append(d2.get('k_pro'))
                            # Append to no nutrient list for Pro
                            no_nut_pro_temp.append(d.get('k_pro'))

                            #Do same for all other cell types
                            nut_syn_temp.append(d2.get('k_syn'))
                            no_nut_syn_temp.append(d.get('k_syn'))

                            nut_peuk_temp.append(d2.get('k_peuk'))
                            no_nut_peuk_temp.append(d.get('k_peuk'))

                            nut_hbact_temp.append(d2.get('k_hbact'))
                            no_nut_hbact_temp.append(d.get('k_hbact'))

                            nut_photo_temp.append(d2.get('k_photo'))
                            no_nut_photo_temp.append(d.get('k_photo'))

                            nut_all_temp.append(d2.get('k_all'))
                            no_nut_all_temp.append(d.get('k_all'))

                            if len(nut_pro_temp) != len(no_nut_pro_temp) or \
                            len(nut_syn_temp) != len(no_nut_syn_temp) or\
                            len(nut_peuk_temp) != len(no_nut_peuk_temp) or \
                            len(nut_hbact_temp) != len(no_nut_hbact_temp) or \
                            len(nut_photo_temp) != len(no_nut_photo_temp) or \
                            len(nut_all_temp) != len(no_nut_all_temp):
                                print('Lists of nutrient and non-nutrient not same length')
                                break # Get out of loop because not same length, so won't be in order

        # Add values to dictionary
        data_nut_no_nut['pro'] = {'nut':nut_pro_temp, 'no_nut':no_nut_pro_temp}
        data_nut_no_nut['syn'] = {'nut':nut_syn_temp, 'no_nut':no_nut_syn_temp}
        data_nut_no_nut['peuk'] = {'nut': nut_peuk_temp, 'no_nut':no_nut_peuk_temp}
        data_nut_no_nut['hbact'] = {'nut':nut_hbact_temp, 'no_nut': no_nut_hbact_temp}
        data_nut_no_nut['photo'] = {'nut': nut_photo_temp, 'no_nut':no_nut_hbact_temp }
        data_nut_no_nut['all'] = {'nut':nut_all_temp , 'no_nut': no_nut_all_temp}

    return data_nut_no_nut
            

# Paired t-test to compare nutrient amended and non-nutrient amended APPARENT growth rates

def paired_t_with_key(data, key):
    # This function does a paired t test with input data
    # data is dictionary with keys as cell types and values as dictionaries of nutrient or no nut k values
        # The data is output from the function nut_no_nut
    # key is the cell type want to compare (i.e., pro, syn, peuk, hbact, photo, or all)
    k = data.get(key)
    no_nut = k.get('no_nut')
    nut = k.get('nut')
    test_result = stats.ttest_rel(no_nut, nut)
    return test_result

######################################################################################
########Code for finding the grazing and growth rates using Chlorophyll data##########
######################################################################################

########Dilution Fraction Calculation##########

# # where the data is located
# directory_to_use = r'C:\Users\alyssia\Desktop\Research_Material_Dr_T\Python_practice' #for PC put r'C:your\path'
# excel_file_to_use = 'Chl_SIO_pier_forcode.xlsx'
# sheet_to_use_dil = 'Dilution_Fraction'


# file_to_read = directory_to_use + '/' + excel_file_to_use

# # read in the data 
# dil_frac_data = pd.read_excel(file_to_read, sheet_name = sheet_to_use_dil)

# # read the data in a dataframe
# dil_frac_df = pd.DataFrame(dil_frac_data)

# # locate the values in columns Chlorophyll_ug/L with disired dilutions 
# hundred_percent = dil_frac_df.query('Dilution==1')['Chlorophyll_ug/L']
# eighty_percent =dil_frac_df.query('Dilution==0.8')['Chlorophyll_ug/L']
# sixity_percent = dil_frac_df.query('Dilution==0.6')['Chlorophyll_ug/L']
# fortyfive_percent = dil_frac_df.query('Dilution==0.45')['Chlorophyll_ug/L']
# twenty_percent = dil_frac_df.query('Dilution==0.2')['Chlorophyll_ug/L']

# # average chlorophyll per dilution 
# ave_hundred_percent = statistics.mean(hundred_percent)
# ave_eighty_percent = statistics.mean(eighty_percent)
# ave_sixity_percent = statistics.mean(sixity_percent)
# ave_fortyfive_percent =statistics.mean(fortyfive_percent)
# ave_twenty_percent = statistics.mean(twenty_percent)

# # find the dilution fraction 
# nominal_hundred = ave_hundred_percent/ave_hundred_percent 
# nominal_eighty = ave_eighty_percent/ave_hundred_percent 
# nominal_sixity = ave_sixity_percent/ave_hundred_percent
# nominal_fortyfive = ave_fortyfive_percent/ave_hundred_percent 
# nominal_twenty = ave_twenty_percent/ave_hundred_percent

# # put dilution fractions into a list 
# # dilution_fractions = [nominal_hundred, nominal_eighty, nominal_fortyfive, nominal_sixity, nominal_twenty]
# # print(dilution_fractions)
# dilution_fractions= [1, 0.8136, 0.6213, 0.4197, 0.2291] # dilution fractions from another experiment using the same squishy bottle, these values will be used for Expt 1,2, and 3 summer 2021


######################################################################
########## Experiment-specific data ##############

# Reading in data and putting in dictionary of lists of dictionaries
# Dictionary with bottles as keys, values are list of dictionary of nutrient val, replicates, etc.
# Order of list is time point (init or final)
# For example {1C: [data_timept0, data_timept1], 2C: [data_timept0, data_timept2], 3C:[data_timept0, data,timept1]}
# data_timept0 is something like {'pro_per_mL':20000, 'syn_per_mL':40000, 'Nutrients_1'=0,'Time_point'=0}

######### Expt. 1 #############

directory_to_use = r'C:\Users\alyssia\Desktop\Research_Material_Dr_T\Python_practice' #'/Users/dtaniguchi/Research/Python_practice' 
# /Users/dtaniguchi/Research/Python_practice
excel_file_to_use = 'Chl_SIO_pier_forcode.xlsx' 
sheet_to_use = 'working_data_exp1_anissa'

file_to_read = directory_to_use + '/' + excel_file_to_use 
###Beginning of Alyssia's work###


data = pd.read_excel(file_to_read, sheet_name = sheet_to_use)
print(data)

col_names = ['Bottle_number','Fraction_Whole_SW','Nut_0_No_Nut_1','Replicate','Time_point','Expt_num',\
                                'Sample_No','Depth_m',\
                                'Vol_Filtered','First_Blank','F0_RFU','F0_Second_Run_RFU',\
                               'Fa_RFU','Fa_Second_Run_RFU','End_Blank','Volume_Acetone_ml',\
                               'Chlorophyll_ug/L','Phaeopigments_ug/L']# add 'Chl_averages'

df = pd.DataFrame(data)
print(df)
# Putting data into dictionary
data_dict = data_in_dict(df, col_names) 
print(data_dict)
###for loop to obtain all the avg chlorophyll values

#With in df
#Unique list of experimennts
expt = list(set(df.Expt_num))#[1,2]
#Unique list of time points
time_pt = list(set(df.Time_point))#[0,1]#, 1, 2]
#Unique list of bottle numbers

# bottle_num =list(set(df.Bottle_number))# ['NaN', '1A', '1B', '2A', '2B', '3A', '3B', '1D', '3D', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '8A', '9A', '10A', '11A', '12A', '7B', '8B', '9B', '4D', '10B', '11B', '12B', '2D']
bottle_num = ['carboy', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34'] # for anissa data 
print(bottle_num)
data = data_dict.copy() # Getting new dictionary into which will put average values
#Going through dictionary to find average values
list_ave_chl = [] #empty list for average chlorophyll
for key, v in data_dict.items(): # going through list in outer dictionary

        for e in expt:
#            print('expt = ',e)
            for t in time_pt:
#                print('time point=',t)
                for b in bottle_num:
#                    print('bottle number=',b)
                    temp_chl = []
                    temp_phaeo = []
                    for d in v:

                        if d['Expt_num'] == e and d['Time_point'] == t and d['Bottle_number'] == b:
                            temp_chl.append(d['Chlorophyll_ug/L'])
                            temp_phaeo.append(d['Phaeopigments_ug/L'])
                    
                            
                            
                    # Finding average of chlorophyll, is possible
                    if not temp_chl:# if chl list is empty
                        chl_ave = float("NAN") # chl average is nan
                    if len(temp_chl) ==1:#if the list is just one value
                        chl_ave = temp_chl[0] # chl average is equal to that one value
                    if len(temp_chl) > 1: # if tehre is more then one value in the list
                        chl_ave= statistics.mean(temp_chl) # chl average is the average of chl values
                        list_ave_chl.append(chl_ave) # append each chl average to this list
                        
                    if temp_chl:
                        print('temp_chl = ',temp_chl)
                        print('average=', chl_ave)
                        print('list of ave chl =', list_ave_chl) 
                    
                    # Same as for chl above, but for phaeopigments
                    if not temp_phaeo: 
                        phaeo_ave = float("Nan")
                    if len(temp_phaeo) == 1:
                        phaeo_ave = temp_phaeo[0]
                    if len(temp_phaeo) > 1:
                        phaeo_ave= statistics.mean(temp_phaeo)
                        
# put ave_chl in dictionary where bottle is the key... couldnt use bottle_num because it printed bottles out of order (order is important)
# bottle = ['carboy', '1A', '2A', '3A', '4A', '5A', '6A', '1B', '2B', '3B', '4B', '5B', '6B', '2D', '7A', '8A', '9A', '10A', '11A', '12A', '7B', '8B', '9B', '10B', '11B', '12B', '4D'] # 1D and 3D we didnt take chl samples from 
bottle = ['carboy', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34'] # for anissas data 
ave_chl_dict = dict(zip(bottle, list_ave_chl))
print(ave_chl_dict)
                        
###########Calulate the apparent growth rate##############

### below seperating the ave chl  by time point  

# ave_chl for t0
# therefore dilution = 1
ave_tzero = ave_chl_dict.get('carboy','None')

# ave_chl for t1 

# bottles number for t1 and dil = 1  
keys_t1_one = ['5A', '6A', '5B', '6B'] # 1D has no chl samples 
# puts values (average chl) in a list, ends in 'none' when there is no more keys
ave_t1_one = [ave_chl_dict.get(key) for key in keys_t1_one] 
print(ave_t1_one)

# bottle number for t1 and dil = 0.8
keys_t1_eighty = ['4A', '4B']
# puts values (average chl) in a list
ave_t1_eighty = [ave_chl_dict.get(key) for key in keys_t1_eighty]

# bottle number for t1 and dil = 0.6 
keys_t1_sixity = ['3A', '3B']
# puts values (average chl) in a list
ave_t1_sixity = [ave_chl_dict.get(key) for key in keys_t1_sixity]

# bottle number for t1 and dil = 0.4 
keys_t1_forty = ['2A', '2B']
# puts values (average chl) in a list
ave_t1_forty = [ave_chl_dict.get(key) for key in keys_t1_forty]

# bottle number for t1 and dil = 0.2 
keys_t1_twenty = ['1A', '1B', '2D']
# puts values (average chl) in a list
ave_t1_twenty = [ave_chl_dict.get(key) for key in keys_t1_twenty]

# # ave_chl for t2 

# bottles number for t2 and dil = 1 
keys_t2_one = ['11A', '12A', '11B', '12B'] # 3D has no chl samples 
# puts values (average chl) in a list 
ave_t2_one = [ave_chl_dict.get(key) for key in keys_t2_one]
# print(ave_t2_one)

# bottles number t2 and dil = 0.8 ####Just copy pasted down below 
keys_t2_eighty = ['10A', '10B']
# puts values (average chl) in a list 
ave_t2_eighty = [ave_chl_dict.get(key) for key in keys_t2_eighty]

# bottle number t2 and dil = 0.6 
keys_t2_sixity = ['9A', '9B']
# puts values (average chl) in a list 
ave_t2_sixity = [ave_chl_dict.get(key) for key in keys_t2_sixity]

# bottle number t2 and dil = 0.4 
keys_t2_forty = ['8A', '8B']
# puts values (average chl) in a list 
ave_t2_forty = [ave_chl_dict.get(key) for key in keys_t2_forty]

# bottles number t2 and dil = 0.2
keys_t2_twenty = ['7A', '7B', '4D']
# puts values (average chl) in a list 
ave_t2_twenty = [ave_chl_dict.get(key) for key in keys_t2_twenty]

# Calculate the apparent growth 

###Day time rates###
print('Day rates below', )

# App. growth rate for dil = 1 
for a in ave_t1_one:
    day_growth_one = (1/0.5)*np.log((a)/(ave_tzero))
    print('hundred', day_growth_one)
    
# App. growth rate for dil = 0.8 
for a in ave_t1_eighty:
    day_growth_eighty = (1/0.5)*np.log((a)/(ave_tzero* 0.8136))
    print('eighty', day_growth_eighty)

# App. growth rate for dil = 0.6
for a in ave_t1_sixity:
    day_growth_sixity = (1/0.5)*np.log((a)/(ave_tzero*0.6213))
    print('sixity', day_growth_sixity)
# App. growth rate for dil = 0.4 
for a in ave_t1_forty:
    day_growth_forty = (1/0.5)*np.log((a)/(ave_tzero*0.4197))
    print('forty', day_growth_forty)
# App. growth rate for dil = 0.2
for a in ave_t1_twenty:
    day_growth_twenty = (1/0.5)*np.log((a)/(ave_tzero*0.2291))
    print('twenty', day_growth_twenty)

### Night time rates ### 
print('')
print('Night rates below')
# App. growth rate for dil = 1
for (a, b) in zip(ave_t2_one, ave_t1_one):
    night_growth_one = (1/0.5)*np.log((a)/(b))
    print('hundred', night_growth_one)
        
# App. growth rate for dil = 0.8 
for (a, b) in zip(ave_t2_eighty, ave_t1_eighty):
    night_growth_eighty = (1/0.5)*np.log((a)/(b))
    print('eighty', night_growth_eighty)
        
# App. growth rate for dil = 0.6 
for (a, b) in zip(ave_t2_sixity, ave_t1_sixity):
    night_growth_sixity = (1/0.5)*np.log((a)/(b))
    print('sixity', night_growth_sixity)
    
# App. growth rate for dil = 0.4 
for (a, b) in zip(ave_t2_forty, ave_t1_forty):
    night_growth_forty = (1/0.5)*np.log((a)/(b))
    print('forty', night_growth_forty)
    
# App. growth rate for dil = 0.2 
for (a, b) in zip(ave_t2_twenty, ave_t1_twenty):
    night_growth_twenty = (1/0.5)*np.log((a)/(b))
    print('twenty', night_growth_twenty)
    
###24 hour rates###
print('')
print('24 hour rates below')

# App. growth rate for dil = 1
for a in ave_t2_one:
    twentyfourhour_growth_one = (1/1)*np.log((a)/(ave_tzero))
    print('hundred', twentyfourhour_growth_one)
    
# App. growth rate for dil = 0.8 
for a in ave_t2_eighty:
    twentyfourhour_growth_eighty = (1/1)*np.log((a)/(ave_tzero*0.8136))
    print('eighty', twentyfourhour_growth_eighty)

# App. growth rate for dil = 0.6
for a in ave_t2_sixity:
    twentyfourhour_growth_sixity = (1/1)*np.log((a)/(ave_tzero*0.6213))
    print('sixity', twentyfourhour_growth_sixity)
    
    
# App. growth rate for dil = 0.4 
for a in ave_t2_forty:
    twentyfourhour_growth_forty = (1/1)*np.log((a)/(ave_tzero*0.4197))
    print('forty', twentyfourhour_growth_forty)

# App. growth rate for dil = 0.2
for a in ave_t2_twenty:
    twentyfourhour_growth_twenty = (1/1)*np.log((a)/(ave_tzero*0.2291))
    print('twenty', twentyfourhour_growth_twenty)
    
####End of calculating the apparent growth rates#####
# reminder the nut and no nut are not sig diff. 

# Next steps are regression, plots 
# import matplotlib.pyplot as plt





expt_Num = 1 #experiment number corresponding to data read in



# Replicates to compare for 24 hour, 12-day, and 12-hour night rates
# 24-hour rates
# dataset, replicate 1, replicate 2, time point 1, time point 2, incubation time
hour_24_r_t = [{'data':data_dict, 'rep1':3,'rep2':3,'time_pt1':0,'time_pt2':2,'inc_time':1.0},
              {'data':data_dict,'rep1':4,'rep2':4,'time_pt1':0,'time_pt2':2,'inc_time':1.0}] 


# Nighttime rates
night_r_t = [{'data':data_dict, 'rep1':1,'rep2':1,'time_pt1':0,'time_pt2':1,'inc_time':0.5},
              {'data':data_dict,'rep1':2,'rep2':2,'time_pt1':0,'time_pt2':1,'inc_time':0.5}] 


# Daytime rates
day_r_t = [{'data':data_dict, 'rep1':1,'rep2':3,'time_pt1':1,'time_pt2':2,'inc_time':0.5},
              {'data':data_dict,'rep1':2,'rep2':4,'time_pt1':1,'time_pt2':2,'inc_time':0.5}] 



### Calculate values for replicate experiments from same time point are kept separate
### Calculating dilution fraction and apparent growth rate

# Calculating dilution fraction 
# Use the average of the initial, undiluted samples as the 
    #denominator to find the dilution fraction
dil_dict = dil_frac_calc(df)

## Calculating apparent growth rate    

full_24_hr_rate = []# list of apparent growth rate (k values) and meta data for 24-hour incubations
daytime_rate = [] # list of apparent growth rates and metadata for daytime incubations
nighttime_rate = [] # list of apparent growth rates and metadata for nighttime incubations


for i in hour_24_r_t:
    temp = k_calc_from_rep(x=i.get('data'),r1 = i.get('rep1'), r2 = i.get('rep2'), t1 = i.get('time_pt1'),\
                          t2 = i.get('time_pt2'), inc_time = i.get('inc_time'))
    full_24_hr_rate.append(temp)


for i in day_r_t:
    temp = k_calc_from_rep(x=i.get('data'),r1 = i.get('rep1'), r2 = i.get('rep2'), t1 = i.get('time_pt1'),\
                          t2 = i.get('time_pt2'), inc_time = i.get('inc_time'))
    daytime_rate.append(temp)
    
for i in night_r_t:
    temp = k_calc_from_rep(x=i.get('data'),r1 = i.get('rep1'), r2 = i.get('rep2'), t1 = i.get('time_pt1'),\
                          t2 = i.get('time_pt2'), inc_time = i.get('inc_time'))
    nighttime_rate.append(temp)

### Model 2 linear regression, paired t-test, average rate values with errors
k_data =  full_24_hr_rate
k_names = ['k_all','k_pro','k_syn','k_peuk','k_hbact','k_photo']
intercept_names = ['intercept_all', 'intercept_pro','intercept_syn','intercept_peuk','intercept_hbact','intercept_photo']
slope_names = ['slope_all', 'slope_pro','slope_syn','slope_peuk','slope_hbact','slope_photo']
k_no_nut_names = ['k_all_no_nut', 'k_pro_no_nut', 'k_syn_no_nut', 'k_peuk_no_nut', 'k_hbact_no_nut', 'k_photo_no_nut',]

# calculate regressions by keeping replicate experiments separate to get 1 intercept, 1 slope for each replicate
rate_rep_sep = model_2_reg_rep_sep(k_data, dil_dict, expt_num, k_names, intercept_names, slope_names)

paired_t_rep_separate = paired_t_rep_sep(rate_rep_sep, intercept_names, k_no_nut_names, k_names, expt_num)

rate_average = rate_ave(rate_rep_sep, intercept_names, k_no_nut_names, slope_names, expt_num)
