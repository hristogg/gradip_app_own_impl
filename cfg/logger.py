# TODO think of custom logging implementation if needed

from google.cloud import logging
def get_logger(logger_name:str = 'v2_yettel_budy'):
    logging_client = logging.Client()
    return  logging_client.logger(logger_name)