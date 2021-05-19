from datetime import timedelta

rush_hours = {'default': 
                  {'am': (timedelta(hours=8), timedelta(hours=10)), 
                   'pm': (timedelta(hours=15), timedelta(hours=17))
                  },
              'italy':
                  {'am': (timedelta(hours=8), timedelta(hours=10)), 
                   'pm': (timedelta(hours=17), timedelta(hours=20))
                  }
             } 

def calc_rush_overlap(start_time, end_time, country='default'):
    
    if start_time.hour < 12:
        rush_interval = rush_hours[country]['am']
    else:
        rush_interval = rush_hours[country]['pm']

    start_in_rush = False
    end_in_rush = False
    start_timedelta = timedelta(hours=start_time.hour, minutes=start_time.minute)
    end_timedelta = timedelta(hours=end_time.hour, minutes=end_time.minute)
    if start_timedelta >= rush_interval[0] and start_timedelta <= rush_interval[1]:
        start_in_rush = True
    if end_timedelta >= rush_interval[0] and end_timedelta <= rush_interval[1]:
        end_in_rush = True

    if start_in_rush and end_in_rush:
        rush_minutes = (end_timedelta - start_timedelta).seconds/60
    elif start_in_rush:
        rush_minutes = (rush_interval[1] - start_timedelta).seconds/60
    elif end_in_rush:
        rush_minutes = (end_timedelta - rush_interval[0]).seconds/60
    else:
        rush_minutes = 0
    
    rush_overlap = rush_minutes / ((end_timedelta - start_timedelta).seconds/60)

    print()
    print(rush_interval[0], rush_interval[1])
    print(start_timedelta, end_timedelta)
    print(start_in_rush, end_in_rush)
    print('rush minutes:', rush_minutes)
    
    return rush_minutes, rush_overlap
