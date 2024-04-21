import pandas as pd
import sys
from itertools import combinations
import math
import heapq
dataset = None   #stores the data so we can access the records and calculate support whenever needed




'''def generate_candidates(df,occurence_counts,k):
    #depending on value for k, update dictionary_counts 
    if k==1: #iterate through whole database 
        for index, row in df.iterrows():
            for col in df.keys().tolist():
                value = row[col]
                if (value,) in occurence_counts:
                    occurence_counts[(value,)] += 1 
                else:
                    occurence_counts[(value,)] = 1 '''
    
    #compute the rest for k bwetween 2 and 6
    #incorporate pruning -> ie only add if confidence of each inidividual item exists 

def create_l1(df, support):
    occurence_counts = {}
    for index, row in df.iterrows():
            
            for col in df.keys().tolist():
                value = row[col]
                if value != value:
                    print("row #: ", index)
                    print("column #: ", col)
                '''if (value, ) == (nan,):
                    print("row #: ", index)
                    print("column #: ", col)'''
                if (value,) in occurence_counts:
                    occurence_counts[(value,)] += 1 
                else:
                    occurence_counts[(value,)] = 1

    to_delete = set()
    for i in occurence_counts:
        if occurence_counts[i]<support:
           to_delete.add(i)
    for i in to_delete:
        del occurence_counts[i]

    
    return occurence_counts

def apriori_gen(l,k,support): #C 
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

        

def create_candidates(prev_dictionary,k):
    prev_set = set()
    for key in prev_dictionary:
        for item in key:
            if item not in prev_set:
                prev_set.add(item)
    #now convert all items to be pairings based of k 
    #convert set into a list and sort it so it is consistent 
    set_list = sorted(prev_set)
    candidates = {}
    for combo in combinations(set_list,k):
            #candidates.append(combo)
            candidates[combo] = 0 
    return candidates 

def database_item_set(candidates,database,k, support):
    #iterate through database
    #if combo exists in row ++ val in dictionary 
    #print("value of k is: ", k)
    #print("value of support is: ", support)


    for index, row in database.iterrows():
        row_items = []
        for col in database.keys().tolist():
            value = row[col]
            row_items.append(value)
        #generate tuple pairings in row 
        #print("row items: ",row_items)
        #print("k-val: ",k)
        for combo in combinations(row_items,k):
            #print("combo is: ", combo)
            if combo in candidates:

                for item in combo:
                    if item == 'nan':
                        print("printing row items: ",row_items)

                #print("combo is in candidates")
                candidates[combo] += 1 
    
    #now delete items in candidates if does not reach supposrt 

    #print("candidates pre deletion for item size ",k, ": ", candidates)
    #return candidates

    to_delete = set()
    for i in candidates:
        if candidates[i]<support:
           to_delete.add(i)
    for i in to_delete:
        del candidates[i]

    #print("candidates for item size ",k, ": ", candidates)
    return candidates
        



    #iterate through dictionary 
    #if support not met, delete it 

    #return updates dictionayr 



def compute_support(tup,occurence_counts,num_rows):
    if tup in occurence_counts:
        support = occurence_counts[tup]/num_rows
    else:
        support = 0
    return support 

def find_new_item_sets(c_k,k,support): #L -> I think this should be a dictionary 
    res = []
    for c in c_k:
        if compute_support(c)>=support:
            res.append(c)
    return res


def TID_C_K(): #C-head
    #do we even really need to do this? 
    #may be necessary for computing support? to see if they exist together?
    pass



### essentially need to decide if we want to do AprioriTid or Apriori -> up to us ###
### let's look at runtime ####


def apriori_take2(item_sets,support,database):
    L = []
    C = []
    l_1 = {}
    l_1 = create_l1(database,l_1)
    L.append(l_1)
    C.append({}) #C[0] is essentially empty but keep formatting 
    k = 2
    while k <= 6: #iterate through k 
        if L[k-2] == {}: #if nothing generated for previous k 
            break
        C_kmin1 = apriori_gen(L[k-2],k,support)
        C.append(C_kmin1)

#modification to this -> convert data structure to be list of length 6 for C and L that store dictioanry 
#while k <= 6 instead of true bc we already have the break statemetn
def apriori(database,support):
    k = 1
    L= []
    C=[]
    #l_1 = {}
    l_1 = create_l1(database,support)
    #l_k = set() #this is supposed to contain the large 1-itemsets.
    #freq_item_sets = set()
    L.append(l_1)
    while k <= 6:
        print("k-value is:", k)
        k+=1
        c_k = create_candidates(L[k-2],k) #compute options on database given prev exiisting options 
        #print("c_k at index ", k, " is:", c_k)
        #print(c_k)
        #l_k = find_new_item_sets(c_k,k,support) #iterate through database to see if possible 
        l_k = database_item_set(c_k,database,k, support)
        #if len(l_k)==0:
        if not l_k:
            print(k)
            break
        else:
            #freq_item_sets.append(i for i in l_k)
            L.append(l_k)
            C.append(c_k)
    #return freq_item_sets
    return L,C

def mine_association_rules(freq_list, conf_threshold,length_of_dataset):
    freq_item_sets = {}
    for map in freq_list:
        for i in map:
            temp = list(i)
            temp.sort()
            temp = tuple(temp)
            freq_item_sets[temp] = map[i]/length_of_dataset
    
    assoc_rules = {}
    for itemset in freq_item_sets:
        for i in itemset:
            rhs = tuple([i])
            lhs = list(itemset).copy()
            lhs.remove(rhs[0])
            lhs = tuple(lhs)
            possible_lhs = []
            for k in range(1,len(lhs)+1):
                possible_lhs.extend(combinations(lhs,k))
            for LHS in possible_lhs:
                #if LHS not in freq_item_sets:
                    #continue
                total = list(LHS+rhs)
                total.sort()
                total = tuple(total)
                confidence_val = freq_item_sets[total]/freq_item_sets[LHS]
                if confidence_val>=conf_threshold:
                    key = repr(lhs)+'=>'+repr(rhs)
                    assoc_rules[key] = (confidence_val,freq_item_sets[itemset])
    return assoc_rules

def main(): 

    '''   NOTE: k can be up to 6 for this specific file '''
    #support = .01
    #confidence = .1
    support = float(sys.argv[1])
    confidence = float(sys.argv[2])

    dataset = pd.read_csv('modified_housing.csv')
    num_transactions = len(dataset) #use this to calculate support 
    print("nun transactions: ", num_transactions)
    frequency_count = {}
    updated_support = support*num_transactions
    individual_count = create_l1(dataset,updated_support )
    L, C = apriori(dataset,updated_support)
    '''for i,dict in enumerate(L): 
        #if i > 0:
        print("L at index ",i+1, ": ", dict)
        print()
        print()
        print()'''

    print('==Frequent itemsets (min_supp={0}%)'.format(support*100))
    heap_support = []
    for dict in L:
        for key in dict:
            support = dict[key]
            proper_support = support/num_transactions
            heapq.heappush(heap_support,(key,proper_support*100))
    while heap_support:
        item = heapq.heappop(heap_support)
        print('{0},  {1}%'.format(list(item[0]),item[1]))
    #print(L)
    #print("C: ", C)
    #print(individual_count)
    print()
    print()
    '''support = sys.argv[1]
    confidence = sys.argv[2]
    #generate initial item_sets
    itemsets = set()

    freq_item_sets = apriori(itemsets) #freq_item_sets should be a list of dictionaries
'''

    #printing the association rules
    
    assoc_rules = mine_association_rules(L,confidence,num_transactions)
    print('==High-confidence association rules (min_conf={0}%)'.format(confidence*100))
    heap = []
    for rule in assoc_rules:
        heapq.heappush(heap,(assoc_rules[rule][0]*-1,assoc_rules[rule][1]*-1,rule))
    while heap:
        item = heapq.heappop(heap)
        print('{0} (Conf: {1:.3f}%, Supp: {2:.3f}%)'.format(item[2],item[0]*-100,item[1]*-100))
    

if __name__=="__main__": 
    main() 

