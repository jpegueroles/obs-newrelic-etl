import requests
import json
import logging
import newrelic.agent

logger = logging.getLogger()

def getData(key, acc_id, guid):
    newrelic.agent.set_transaction_name("getData")
    # GraphQL query to NerdGraph
    #obtenemos todos los recursos que tienen nulo o no tienen los tags: tags.ApplicationName y tags.label.ApplicationName

    query = """
       {
            actor {
                    account(id: %s) {
                        nrql(
                            query: "SELECT average(newrelic.goldenmetrics.apm.application.responseTimeMs) AS 'Response Time Ms' FROM Metric WHERE entity.guid in ('%s') LIMIT MAX TIMESERIES"
                        ) {
                            rawResponse
                    }
                }
            }
        }
    """ % (acc_id,guid)

    # NerdGraph endpoint
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'API-Key': f'{key}'}
    response = requests.post(endpoint, headers=headers, json={"query": query})

    if response.status_code == 200:
        # convert a JSON into an equivalent python dictionary
        json_dictionary = json.loads(response.content) 
        # must handle cursor
        #total_count = json.dumps(response.json()['data'])
        #nextCursor = str.replace(json.dumps(response.json()['data']['nextCursor']), '"', '')
        #logger.info(f'total_count: {total_count}')
        
        nextCursor = "null"

        while nextCursor != "null":
            query2 = """
       
            """ % (acc_id)

            response2 =requests.post(endpoint, headers=headers, json={"query": query2})
            payload = json.loads(response2.content)

            if payload['data']['nextCursor'] is None:
                nextCursor = "null"
            else:
                nextCursor = payload['data']['nextCursor']
        

        
        results = json_dictionary['data']['actor']['account']['nrql']['rawResponse']
        logger.info(f'try to get total current objects {len(results)}')
    else:
        # raise an error with a HTTP response code
        raise Exception("Nerdgraph query failed with a",response.status_code)
    
    return results

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################