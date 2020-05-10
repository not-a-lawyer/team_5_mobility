from dateutil import parser

def compute_emissions(transportation_types: list, transportation_length: list):
    co2_emission = 0

    co2_emission_dict = {'car':140,
                         'bike': 0.3,
                         'transit': 65,
                         'pedestrian': 0}

    if len(transportation_types) == len(transportation_length):
        i = 0
        for type in transportation_types:
            co2_emission += co2_emission_dict[type]*transportation_length[i]
            i +=1
        return co2_emission

    else:
        raise Exception('Lists are not the same length')



def compute_overall_trip_time(modal_data_request):
    """
    looks at the first and last time of the intermodal route, computing overall trip time
    :param modal_data_request:
    :return: final_time
    """
    try:



        start_time = parser.parse(modal_data_request['routes'][1]['sections'][0]['departure']['time'])
        end_time = parser.parse(modal_data_request['routes'][1]['sections'][-1]['arrival']['time'])

        final_time = end_time - start_time
        return final_time




    except:
        print('No route')