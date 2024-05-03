from typing import Dict, List
from flask import request as FlaskRequest
from src.drivers.interfaces.driver_handler_interface import DriverHandlerInterface
from src.errors.http_unprocessable_entity import HttpUnprocessableEntityError

class Calculator2:
    def __init__(self, driver_handler: DriverHandlerInterface) -> None:
        self.__driver_handler = driver_handler

    def calculate(self, request: FlaskRequest) -> Dict: # type: ignore
        '''
            - N números são enviados
            - Todos esses N números são multiplicados por 11 e elevados a potência de 0.95
            - Por fim, é retirado o desvio padrão desses resultados e retornado o inverso desse valor (1/result)
        '''
        body = request.json
        input_data = self.__validate_body(body)
        calculeted_number = self.__process_data(input_data)

        formated_response = self.__format_response(calculeted_number)
        return formated_response
    

    def __validate_body(self, body: Dict) -> List[float]:
        if "numbers" not in body:
            raise HttpUnprocessableEntityError("Body mal formatado")
        
        input_data = body["numbers"]
        return input_data
    
    def __process_data(self, input_data: List[float]) -> float:
        first_process_result = [(num * 11) ** 0.95 for num in input_data]
        result = self.__driver_handler.standard_derivation(first_process_result)
        return 1 / result
    
    def __format_response(self, calculeted_number: float) -> Dict:
        return {
            "data": {
                "Calculator": 2,
                "result": round(calculeted_number, 2)
            }
        }