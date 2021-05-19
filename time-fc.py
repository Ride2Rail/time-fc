import os
import json
import redis
from flask import Flask, request
from datetime import datetime as dt
from datetime import timedelta
import configparser as cp

from cache_operations import extract_data_from_cache
import rush_hours
import rod

service_name = os.path.splitext(os.path.basename(__file__))[0]
app = Flask(service_name)

# config
config = cp.ConfigParser()
config.read(f'{service_name}.conf')

# cache
cache = redis.Redis(host=config.get('cache', 'host'),
                    port=config.get('cache', 'port'),
                    decode_responses=True)

@app.route('/compute', methods=['POST'])
def extract():
    
    data = request.get_json()
    request_id = data['request_id']

    # ask for the entire list of offer ids
    offer_data = cache.lrange('{}:offers'.format(request_id), 0, -1)
    print('\n\nRequest ID:', request_id) 
    print('Offer data [21]:', offer_data)

    response = app.response_class(
        response=f'{{"request_id": "{request_id}"}}',
        status=200,
        mimetype='application/json'
    )

    output_offer_level, output_tripleg_level = extract_data_from_cache(pa_cache=cache, pa_request_id=request_id,
                                                                       pa_offer_level_items=['start_time', 'end_time'],
                                                                       pa_tripleg_level_items=['start_time', 'end_time'])
    #print('\n\nOutput offer level [33]:', json.dumps(output_offer_level, indent=4, sort_keys=True))
    print('\n\nOutput tripleg level [34]:', json.dumps(output_tripleg_level, indent=4, sort_keys=True))
    
    # to be replaced with the actual date and time of the request
    current_time = dt(2019, 5, 5)
    
    offer_features = {'duration':{},
                      'time_to_departure':{},
                      'waiting_time':{},
                      'rush_overlap':{}}
    
    for offer_id in output_offer_level['offer_ids']:
        offer_start_time = dt.strptime(output_offer_level[offer_id]['start_time'], '%Y-%m-%dT%H:%M:%S')
        offer_end_time = dt.strptime(output_offer_level[offer_id]['end_time'], '%Y-%m-%dT%H:%M:%S')
        offer_duration = (offer_end_time - offer_start_time).total_seconds()/60
        offer_time_to_departure = (offer_start_time - current_time).total_seconds()/60
        rush_minutes, rush_overlap = rush_hours.calc_rush_overlap(offer_start_time, offer_end_time, country='default')
        
        # compute the overall waiting time between legs
        leg_ids = sorted(output_tripleg_level[offer_id]['triplegs'])
        waiting_time_between_legs = 0
        if len(leg_ids) > 1:
            for i in range(1, len(leg_ids)):
                previous_end_time = dt.strptime(output_tripleg_level[offer_id][leg_ids[i-1]]['end_time'], '%Y-%m-%dT%H:%M:%S')
                next_start_time = dt.strptime(output_tripleg_level[offer_id][leg_ids[i]]['start_time'], '%Y-%m-%dT%H:%M:%S')
                waiting_time_between_legs += (next_start_time - previous_end_time).total_seconds()/60
                            
        offer_features['duration'][offer_id] = offer_duration
        offer_features['time_to_departure'][offer_id] = offer_time_to_departure
        offer_features['waiting_time'][offer_id] = waiting_time_between_legs
        offer_features['rush_overlap'][offer_id] = rush_overlap
        
    # rank offers by score and convert scores to weights
    offer_features_weights = {}
    for feature in offer_features:
        offer_ranks = rod.rank_offers(offer_features[feature])
        offer_features_weights[feature] = rod.assign_rod_weights(offer_ranks)
        
    print('\n\nOffer features:')
    print(json.dumps(offer_features, indent=4, sort_keys=True))   
    
    print('\n\nOffer features (weights):')
    print(json.dumps(offer_features_weights, indent=4))  
    
    
    return response


if __name__ == '__main__':
    
    FLASK_PORT = 5000
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    os.environ["FLASK_ENV"] = "development"

    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    #print(cache.keys())

    app.run(port=FLASK_PORT, debug=True)