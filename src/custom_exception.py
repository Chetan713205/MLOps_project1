import traceback
import sys


# This class inherits from Python’s built-in Exception class.
class CustomException(Exception):
    
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)
        
    
    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_tb = traceback.sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error occurred in script: [{file_name}] at line number: [{line_number}] with message: [{error_message}]"
  

    def __str__(self):
        return self.error_message