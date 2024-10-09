from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from vertexai.preview.language_models import TextEmbeddingModel
from cfg.logger import get_logger
from cfg.config import load_config
from typing import List
logger = get_logger()

config = load_config()

def get_query_embedding(query: str) -> List[float]:
    """
    Generates embeddings for a given query.

    Args:
        query (str): The query string.

    Returns:
        List[float]: The query embeddings.
    """
    model = TextEmbeddingModel.from_pretrained(config['text_embed_model_name'])
    return model.get_embeddings([query])[0].values


def find_neighbors(query_embedding: List[float], deployed_index_name: str, index_endpoint_id: str, num_neighbors: int):
    """
    Finds neighbors for the given query embedding and logs results.

    Args:
        query_embedding (List[float]): The query embeddings.
        deployed_index_name (str): The name of the deployed index.
        index_endpoint_id (str): The ID of the index endpoint.
        num_neighbors (int): The number of neighbors to return.
    """
    logger.log_text(f'deployed_index_name is {deployed_index_name} and index_endpoint_id is {index_endpoint_id}')
    try:
        ## this should not be hardcoded but read from the config.yml

        my_index_endpoint = MatchingEngineIndexEndpoint(index_endpoint_name=deployed_index_name)
        logger.log_text('Sucessfuly connected ot datapoint')
        logger.log_text(f'Using index endpoint: {index_endpoint_id} and index_name {deployed_index_name}')
        response = my_index_endpoint.find_neighbors(deployed_index_id=deployed_index_name, 
                                                    queries=[query_embedding], 
                                                    num_neighbors=num_neighbors, 
                                                    return_full_datapoint=True)
        logger.log_text("Neighbors found successfully.")
        return response
    except Exception as e:
        logger.log_text(f"Failed to find neighbors: {e}",severity='ERROR')
        return None


#query = 'Какво е петък с Yettel?'
#query_embed = get_query_embedding(query)
#response = find_neighbors(query_embedding=query_embed,deployed_index_name='yetdocindexid',index_endpoint_id='projects/258111191672/locations/europe-west3/indexEndpoints/5769498150754582528', num_neighbors=3)
#print(response)