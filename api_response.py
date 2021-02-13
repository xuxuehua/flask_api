from enum import Enum


class ApiResult(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ApiResponse:
    def __init__(self, result, message=None, data=None):
        self.result = result
        self.message = message
        self.data = data
        
    def json_output(self):
        return {
            "result": self.result,
            "message": self.message,  
            "data": self.data
        }
        
        
def http200(message=None, data=None):
    return ApiResponse(result=ApiResult.SUCCESS.value,
                       message=message,
                       data=data).json_output(), 200


def http201(message=None, data=None):
    return ApiResponse(result=ApiResult.SUCCESS.value,
                       message=message,
                       data=data).json_output(), 201
