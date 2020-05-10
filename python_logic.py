from dateutil import parser

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