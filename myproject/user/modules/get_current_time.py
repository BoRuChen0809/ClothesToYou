from datetime import datetime

def get_current_time():
    curr_time = datetime.now()
    #print(curr_time.year)
    curr_time_str = '_'.join([str(curr_time.year), str(curr_time.month), str(curr_time.day), str(curr_time.hour), str(curr_time.minute), str(curr_time.second)])
    print(curr_time_str)
    return curr_time_str
