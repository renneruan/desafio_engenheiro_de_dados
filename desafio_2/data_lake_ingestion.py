# Tendo em vista que não foi fornecido o prefixo de url para a API
# nem exemplos de ID de loja a serem consultadas, o código a seguir
# será feito com base em dados de mockup, ou seja artificiais para testes

import json
import requests
import boto3
import re
from datetime import datetime

s3 = boto3.resource("s3")


class ApiIngestion:
    def __init__(self, urlPrefix, bucketName):
        self.urlPrefix = urlPrefix
        self.bucketName = bucketName

    def __store_data(self, path, json_data):
        """
        Função utilizada para armazenar no bucket o arquivo JSON
        Irá resgatar a data atual para salvar no último nó da hierarquia

        Parâmetros:
        - path: Caminho completo que o arquivo será armazenado
        - json_data: Objeto json a ser salvo
        """

        final_path = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".json"
        final_path = "raw/" + path + final_path

        # Esta chamada para a ingestão em S3 presume que as credenciais AWS estejam configuradas
        # na máquina em que o código está sendo executado.

        s3.Bucket(self.bucketName).put_object(
            Key=final_path, Body=json.dumps(json_data)
        )

    def __get_path_string(self, url, busDt, storeId):
        """
        Função utilizada para resgatar o caminho total do arquivo a partir
        dos parâmetros fornecidos.

        Parâmetros:
        - url: Url que desejamos encontrar as informações
        - busDt: Data de parâmetro da requisição
        - storeId: Id da loja correspondente
        """
        busDt_datetime = datetime.strptime(busDt, "%Y-%m-%d")

        year = busDt_datetime.year
        month = busDt_datetime.month
        day = busDt_datetime.day

        url_elements = url.strip("/").split("/")

        # Pega apenas os elementos finais da URL, garantindo que não peguemos elementos
        # como o http ou o prefixo
        url_elements = url_elements[-2:]

        # Verifica onde há uma string seguida de outra maíscula e insere um _ entre elas
        snake_case_url = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", url_elements[1]).lower()

        return f"{storeId}/{url_elements[0]}/{snake_case_url}/{year}/{month:02d}/{day:02d}/"

    def __get_and_store(self, url, busDt, storeId):
        """
        Assumimos que os objetos de payload informados possam ser passados como parâmetros
        Tal requisição não foi testada com o endpoint real fornecido, então a corretudo
        do fluxo do código é uma suposição baseado em testes feito com dados arbitrários

        Parâmetros:
        - url: URL que será feita a requisição
        - busDt: Data inerente aos dados que queremos
        - storeId: Id da loja correspondente

        Retorno:
        - json_data: Dados obtidos a partir da requisição
        """
        response = requests.post(url, params={"busDt": busDt, "storeId": storeId})
        # response = {"status_code": 200, "data": "Teste de arquivo JSON"}

        # Para response em JSON de teste trocar para response["status_code"]
        # if response["status_code"] < 400:
        if response.status_code < 400:
            json_data = response.json()
            # json_data = response

            path = self.__get_path_string(url, busDt, storeId)
            self.__store_data(path, json_data)

            return json_data
        else:
            print(f"Não foi possível resgatar dados para a URL: {url}")

        return None

    def get_and_store_fiscal_invoice(self, busDt, storeId):
        url = self.urlPrefix + "/bi/getFiscalInvoice"
        return self.__get_and_store(url, busDt, storeId)

    def get_and_store_guest_checks(self, busDt, storeId):
        url = self.urlPrefix + "/res/getGuestChecks"
        return self.__get_and_store(url, busDt, storeId)

    def get_and_store_charge_back(self, busDt, storeId):
        url = self.urlPrefix + "/org/getChargeBack"
        return self.__get_and_store(url, busDt, storeId)

    def get_and_store_transactions(self, busDt, storeId):
        url = self.urlPrefix + "/trans/getTransactions"
        return self.__get_and_store(url, busDt, storeId)

    def get_and_store_cash_management_details(self, busDt, storeId):
        url = self.urlPrefix + "/inv/getCashManagementDetails"
        return self.__get_and_store(url, busDt, storeId)


# teste = ApiIngestion(urlPrefix="http://www.teste.com/", bucketName="cb-lab-bucket")
# result = teste.get_and_store_guest_checks("2024-11-01", 1)
