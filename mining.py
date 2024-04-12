import pandas as pd
import sys

dataset = None   #stores the data so we can access the records and calculate support whenever needed




def generate_candidates(df,occurence_counts,k):
    #depending on value for k, update dictionary_counts 
    if k==1: #iterate through whole database 
        for index, row in df.iterrows():
            for col in df.keys().tolist():
                value = row[col]
                if (value,) in occurence_counts:
                    occurence_counts[(value,)] += 1 
                else:
                    occurence_counts[(value,)] = 1 
    
    #compute the rest for k bwetween 2 and 6
    #incorporate pruning -> ie only add if confidence of each inidividual item exists 


    return occurence_counts




def compute_support(tup,occurence_counts,num_rows):
    if tup in occurence_counts:
        support = occurence_counts[tup]/num_rows
    else:
        support = 0
    return support 

def find_new_item_sets(c_k,k,support):
    res = []
    for c in c_k:
        if compute_support(c)>=support:
            res.append(c)
    return res


def apriori(item_sets,support):
    k = 0
    l_k = set() #originally only contains  the empty element
    freq_item_sets = set()
    while True:
        k+=1
        c_k = generate_candidates(l_k,k,support)
        l_k = find_new_item_sets(c_k,k,support)
        if len(l_k)==0:
            break
        else:
            freq_item_sets.append(i for i in l_k)
    return freq_item_sets

def mine_association_rules(freq_item_sets):
    pass

def main(): 

    '''   NOTE: k can be up to 6 for this specific file '''

    dataset = pd.read_csv('modified_housing.csv')
    num_transactions = len(dataset) #use this to calculate support 
    frequency_count = {}
    individual_count = generate_candidates(dataset,frequency_count,1)
    print(individual_count)
    
    '''support = sys.argv[1]
    confidence = sys.argv[2]
    #generate initial item_sets
    itemsets = set()

    freq_item_sets = apriori(itemsets)

    assoc_rules = mine_association_rules(freq_item_sets,confidence)

    #print freq item sets and association rules
    print(freq_item_sets)
    print(assoc_rules)'''

if __name__=="__main__": 
    main() 

