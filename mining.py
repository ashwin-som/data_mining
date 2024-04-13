import pandas as pd
import sys
from itertools import combinations

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

def apriori_gen(l,k,support):
    candidates = []
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            p = list(l[i])
            q = list(l[j])
            p.sort()
            q.sort()
            if p[:-1] == p[:-1] and p[-1] < q[-1]:
                c = l[i].union({q[-1]})
                candidates.append(c)

    #prune step
    final_candidates = []
    for c in candidates:
        subsets = []
        for comb in combinations(c,k-1):
            subsets.append(comb)
        flag = False
        for subset in subsets:
            if subset not in l:
                flag = True
                break
        if not flag:
            final_candidates.append(c)

    return final_candidates



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
    l_k = set() #this is supposed to contain the large 1-itemsets.
    freq_item_sets = set()
    while True:
        k+=1
        c_k = apriori_gen(l_k,k,support)
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

