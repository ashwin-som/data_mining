#read in csv_file 

#do modifications 
#llalas
#write to a new file 

import pandas as pd
import numpy as np
#read in csv_file 
#do modifications 
#write to a new file 

#import csv
'''with open('Affordable_Housing_Production_by_Building_20240402.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       count = 0 
       for lines in csvFile:
            count += 1 
            if count > 50:
                  break
            print(lines)'''
'''
questionable of which to include:
Building Completion Date
Reporting Construction Type	
Extended Affordability Only	
revailing Wage Status

'''
print("starting")
#ignoring -> Project Start Date,	Project Completion Date,	Building ID	Number	Street	Borough	Postcode	BBL	BIN	Community Board	Council District	Census Tract	NTA - Neighborhood Tabulation Area	Latitude	Longitude	Latitude (Internal)	Longitude (Internal)	Building Completion Date	Reporting Construction Type	Extended Affordability Only	Prevailing Wage Status	Extremely Low Income Units	Very Low Income Units	Low Income Units	Moderate Income Units	Middle Income Units	Other Income Units	Studio Units	1-BR Units	2-BR Units	3-BR Units	4-BR Units	5-BR Units	6-BR+ Units	Unknown-BR Units	Counted Rental Units	Counted Homeownership Units	All Counted Units	Total Units
#Neighborhood tabulation areas (NTAs) were created by the NYC Department of City Planning to project populations at a small area level.
'''df = pd.read_csv("Affordable_Housing_Production_by_Building_20240402.csv", usecols=['Project ID','Project Name', 'Borough',	'Postcode', 'BBL', 
                                                                                    'BIN', 'NTA - Neighborhood Tabulation Area',
                                                                                    'Extremely Low Income Units',	'Very Low Income Units','Low Income Units',
                                                                                    'Moderate Income Units',	'Middle Income Units',	'Other Income Units',	
                                                                                    'Counted Rental Units', 'Counted Homeownership Units', 'All Counted Units',	
                                                                                    'Total Units'
])'''


'''
merge:
Extremely Low Income Units	
Very Low Income Units	
Low Income Units	
Moderate Income Units	
Middle Income Units	
Other Income Units(can probably ignore this one )

'''


#file name: https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data


#def merge_income_vals(extremely_low, very_low, low, moderate, middle):
def merge_income_vals(count_list):
    #total = extremely_low + very_low + low + moderate + middle
    #count_list = 
    weight_vector = np.array([1,2,3,4,5]) #skipping zero, so that there is less "exceptions"
    #lue_vector = np.array([extremely_low, very_low, low, moderate, middle])
    value_vector = np.array(count_list)
    total = np.sum(value_vector)
    #multiply each by the percentage of score 
    #a lot fall between 2.95 and 3 
    score = np.dot(weight_vector,value_vector)/total
    if score < 1.85:
        return "very_low"
    elif score >=1.85 and score <= 3:
        return "low"
    else: #greater than 3
        return "moderately_low"
    #these currently give is a dist of 756 for very low, 3937 for low, and 2560 for moderately low 
    
def rental_rate(input):
    rented = input[0]
    owned = input[1]
    total = input[2]
    if rented/total > .5:
        return "mostly_rented"
    elif owned/total > .5:
        return "mostly_owned"
    else:
        return "unclear" 
def afford_reg(input2):
    affordable = input2[0]
    total = input2[1]
    ratio = affordable/total
    if ratio > .7:
        return "mostly_affordable"
    if ratio < .3:
        return "mostly_standard"
    else:
        return "mixed_aff_and_stand"       

#loop through df and merge these values in this 
#update dataframe 

#write df to modified_housing.csv
def main():
      #read in original file 
      df = pd.read_csv("Affordable_Housing_Production_by_Building_20240402.csv", usecols=['Project ID','Project Name', 'Borough',	'Postcode', 'BBL', 
                                                                                    'BIN', 'NTA - Neighborhood Tabulation Area',
                                                                                    'Extremely Low Income Units',	'Very Low Income Units','Low Income Units',
                                                                                    'Moderate Income Units',	'Middle Income Units',	'Other Income Units',	
                                                                                    'Counted Rental Units', 'Counted Homeownership Units', 'All Counted Units',	
                                                                                    'Total Units'
      ])
      #drop empty cells 
      df = df.dropna()
    #poverty levels 
      columns_to_merge = ['Extremely Low Income Units','Very Low Income Units','Low Income Units', 'Moderate Income Units','Middle Income Units']
      new_column = []
      #create new values into a list 
      for i,row in df.iterrows():
          update_vals = df.loc[i,columns_to_merge]
          new_label = merge_income_vals(update_vals)
          new_column.append(new_label)
      #append new_column to df 
      df['Income'] = new_column
      #remove columns to merge
      df = df.drop(columns=columns_to_merge)

      #rented vs owned counter 
      ro_cols = ['Counted Rental Units', 'Counted Homeownership Units', 'All Counted Units']
      ro_new = []
      for i,row in df.iterrows():
          update_vals2 = df.loc[i,ro_cols]
          new_label = rental_rate(update_vals2)
          ro_new.append(new_label)
      df['Rented_vs_Owned'] = ro_new

      #towards affordable ratio
      afford_cols = ['All Counted Units','Total Units']
      aff_new = []
      for i,row in df.iterrows():
          update_vals3 = df.loc[i,afford_cols]
          new_label = afford_reg(update_vals3)
          aff_new.append(new_label)
      df['Level of Affordable in Building'] = aff_new

      dropping_cols = ['Counted Rental Units', 'Counted Homeownership Units', 'All Counted Units','Total Units']
      df = df.drop(columns=dropping_cols)

      #dropping post bin bil and super unit
      bin_bil = ['Postcode','BBL','BIN','Other Income Units']
      df = df.drop(columns=bin_bil)

      #remvoe project id: 
      df = df.drop(columns=['Project ID'])

      #analysis purpose 
      #data[‘column_name’].value_counts()[value]
      mod_income = df["Income"].value_counts()['moderately_low']
      low_income = df["Income"].value_counts()['low']
      try:
        very_low_income = df["Income"].value_counts()['very_low']
      except:
          very_low_income = 0
      print("moderate income count: ", mod_income)
      print("low income count: ", low_income)
      print("very low income count: ", very_low_income)

      #write to output 
      df.to_csv('modified_housing.csv', index=False)
      #print(df[:10])

if __name__ == "__main__":
    main()