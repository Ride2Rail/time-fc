weights = {2: [0.6932, 0.3068],
           3: [0.5232, 0.3240, 0.1528],
           4: [0.4180, 0.2986, 0.1912, 0.0922],
           5: [0.3471, 0.2686, 0.1955, 0.1269, 0.0619],
           6: [0.2966, 0.2410, 0.1884, 0.1387, 0.0908, 0.0445],
           7: [0.2590, 0.2174, 0.1781, 0.1406, 0.1038, 0.0679, 0.0334],
           8: [0.2292, 0.1977, 0.1672, 0.1375, 0.1084, 0.0805, 0.0531, 0.0263],
           9: [0.2058, 0.1808, 0.1565, 0.1332, 0.1095, 0.0867, 0.0644, 0.0425, 0.0211],
           10: [0.1867, 0.1667, 0.1466, 0.1271, 0.1081, 0.0893, 0.0709, 0.0527, 0.0349, 0.0173]}

# ´´offers´´ is a dict where keys are offer ids and values are scores
# if performance is crucial, we can optimize and apply ranking and weights in the same function, in the same loop
def rank_offers(offers):
    
    sorted_offer_ids = sorted(offers, key=offers.get)
    offer_ranks = {sorted_offer_ids[0]:0}
    k = 0
    for i in range(1, len(sorted_offer_ids)):
        if offers[sorted_offer_ids[i]] >  offers[sorted_offer_ids[i-1]]:
            k += 1
        offer_ranks[sorted_offer_ids[i]] = k
    
    return offer_ranks


# ´´offer_ranks´´ is a dict where keys are offer ids and values are ranks (position index in the ranked list of offers)
def assign_rod_weights(offer_ranks):
    assert len(offer_ranks) <= 10
    
    offer_weights = {}
    for offer_id in offer_ranks:
        offer_weights[offer_id] = weights[len(offer_ranks)][offer_ranks[offer_id]]
        
    return offer_weights
        
        
    