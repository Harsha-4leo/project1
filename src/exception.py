import sys
from dbm import error
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error_message [{str(error)}]"

    return error_message

class CustomException(Exception):
    def __init__(self,error_message,erro_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error, error_detail=erro_detail)

    def __str__(self):
        return self.error_message

if __name__=="__main__":

    try:
        a=1/10
        logging.info("No Exception")
    except Exception as e:
        logging.info("Divide by Zero Division")    
        raise CustomException(e,sys)
