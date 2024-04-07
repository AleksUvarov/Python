import requests
from zeep import Client

# Список допустимых категорий запросов
categories = {
    "столица": "GetCapital",
    # Добавьте другие категории запросов здесь
}

# URL для SOAP-сервиса
soap_service_url = 'http://www.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'

# Функция для формирования запроса к SOAP-сервису
def make_soap_request(category, query):
    client = Client(soap_service_url)
    method_name = categories.get(category)
    if not method_name:
        return "Недопустимая категория запроса."
    method = getattr(client.service, method_name)
    result = method(query)
    return result

# Программа для обработки запросов пользователя
def main():
    print("Допустимые категории запросов:", list(categories.keys()))
    while True:
        user_input = input("Введите запрос (например, 'столица России'): ").split()
        if len(user_input) < 2:
            print("Неверный формат запроса. Попробуйте снова.")
            continue
        category = user_input[0].lower()
        query = ' '.join(user_input[1:])
        result = make_soap_request(category, query)
        print("Ответ:", result)

if __name__ == "__main__":
    main()
