import pandas as pd
import sys

dataset = None   #stores the data so we can access the records and calculate support whenever needed

def generate_candidates(l):
    pass


def compute_support(tup):
    pass

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
    dataset = pd.read_csv('INTEGRATED_DATASET.csv')
    support = sys.argv[1]
    confidence = sys.argv[2]
    #generate initial item_sets
    itemsets = set()

    freq_item_sets = apriori(itemsets)

    assoc_rules = mine_association_rules(freq_item_sets,confidence)

    #print freq item sets and association rules
    print(freq_item_sets)
    print(assoc_rules)

