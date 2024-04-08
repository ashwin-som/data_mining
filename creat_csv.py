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


#def merge_income_vals(extremely_low, very_low, low, moderate, middle):
def merge_income_vals(count_list):
    #total = extremely_low + very_low + low + moderate + middle
    weight_vector = np.array([1,2,3,4,5]) #skipping zero, so that there is less "exceptions"
    #lue_vector = np.array([extremely_low, very_low, low, moderate, middle])
    value_vector = np.array(count_list)
    total = np.sum(value_vector)
    #multiply each by the percentage of score 
    score = np.dot(weight_vector,value_vector)/total
    if score < 1:
        return "very_low"
    elif score >=1 and score <= 3:
        return "low"
    else: #greater than 3
        return "moderately_low"
        

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
      #write to output 
      df.to_csv('modified_housing.csv', index=False)
      print(df[:10])

if __name__ == "__main__":
    main()