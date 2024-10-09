from doc_query.utils import get_query_embedding
from google.cloud import aiplatform_v1
from google.cloud import aiplatform
from cfg.config import load_config
from cfg.logger import get_logger
import time
from typing import Optional, Dict
logger = get_logger()
config = load_config()

API_ENDPOINT=config['api_endpoint']
INDEX_NAME =config['index_name']
INDEX_ENDPOINT=config['index_endpoint']
DEPLOYED_INDEX_ID=config['deployed_index_id']

def semantic_match(query: str):
    """Returns semantic match from vector store with QA based on query
    Parameters:
    query(str): User's question
    Returns: 
        dict: 
            id - id of the hashed question in redis
            confidence - confidence of similartiy 
    TODO: Add confidence threshold, think whether to add restricts
    """
    query_embed = get_query_embedding(query)
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=INDEX_ENDPOINT)
    match =  my_index_endpoint.find_neighbors(deployed_index_id=DEPLOYED_INDEX_ID,queries=[query_embed])
    top_match = match[0][0]
    id = top_match.id
    confidence = round(1-top_match.distance,2)
    top_match_dict = {'id':id,'confidence':confidence}
    return(top_match_dict)




def handle_semantic_match(question: str, start_time: float, upsert: bool=False, confidence: float=0.85) -> Dict[str, Optional[str]]:
    """
    Handle the search in Vector Store with documnet chunk when no exact or semantic matches have been found

    Parameters:
        question (str): User's question.
        start_time (float): Timestamp when the query processing started.
        upsert(bool) Flag whether to upsert the question to the vector database (not used)
        confidence(float): Above what confidence we should consider the quesiton as similar

    Returns:
        dict: Details about the processed question.
    """
    try:
        answer = semantic_match(question)
        ret_conf = answer['confidence']
        ret_id = answer['id']
        if ret_conf >= confidence:
            logger.log_text(f'Confidence above threshold level {ret_conf} found, with id {ret_id} ')
            if upsert == True:
                logger.log_text(f'Upsert true, not implemented', severity='ERROR')
                return(None)
            
            exact_match = match(ret_id,tohash=False)
            if exact_match == None:
                logger.log_text('No exact match found, discrepancy between Vector Store and Memory Store',severity='ERROR')
                return(None)
            else:
                return({
                    "question":question,
                    "closest_question_id":ret_id,
                    "confidence":ret_conf,
                    "match_type":"SIMILARITY_QNA",
                    "answer": exact_match,
                    "exec_time": (time.time() - start_time)*1000
                })
    except Exception as e:
        logger.log_text(f"Error during native search: {str(e)}")

if __name__ == '__main__':
    quest = 'Дай ми повече информация за кампанията 6 месеца неограничени MB на максимална скорост'
    start_time = time.time()
    #native_answ = handle_semantic_match(question=quest,start_time=start_time)
    #print(native_answ)
    #match = handle_semantic_match('Какво е Петък с Yettel?', start_time=start_time)

    #print(match)
    print(semantic_match('какво е петък с Yettel?'))
               