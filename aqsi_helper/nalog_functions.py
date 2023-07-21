import requests
import config as cfg
import re


def get_nalog_info(aqsi_list):
    '''
    Функция get_nalog_info принимает список серийных номеров терминалов AQSI
    и проверяет их с помощью сервиса на сайте налоговой,
    используя модуль request
    '''
    # Переменная с URL для запроса
    link = cfg.NALOG_URL
    # Словарь для сохранения результата проверки
    aqsi_res_dict = {}
    # Необходимые заголовки для запроса
    headers = {
        "User-Agent": "PostmanRuntime/7.28.4",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    proxy = {"http": cfg.HTTP_PROXY_URL, "https": cfg.HTTPS_PROXY_URL}
    payload = ""
    try:
        s = requests.Session()
        # s.proxies = proxy
        # Основной цикл проверки
        for sn in aqsi_list:
            # Запрос на сайт налоговой. В качестве параметров передаются срийный номер (sn), и номер модели
            # (0127 - AQSI)
            response = s.get(link, headers=headers, params={"factory_number": sn,
                                                                       "model_code": "0127"}, data=payload)
            # Терминал исправен
            if response.json()["check_status"] == 1:
                aqsi_res_dict[sn] = 1
            elif response.json()["check_status"] == 0:
                # Терминал фискализирован (неисправен)
                if response.json()["check_result"] == "Экземпляр с данным заводским номером уже используется." \
                                                          " Повторная регистрация не допускается. Проверьте" \
                                                          " корректность вводимого значения.":
                    aqsi_res_dict[sn] = -1
                # Терминал не найден в реестре
                if response.json()["check_result"] == "Заводской номер ККТ отсутствует в реестре произведенных" \
                                                          " экземпляров ККТ":
                    aqsi_res_dict[sn] = 0
        # Если сервер налоговой недоступен, header "check_status" не будет получен в ответе, поэтому вызовется исключение.
        # Обрабатываем это исключение.
    except Exception:
        return "Сервер временно недоступен"
    return aqsi_res_dict


def read_aqsi_list(aqsi_sn_str):
    '''
    Функция read_aqsi_list ищет в передаваемой строке aqsi_sn_str серийные номера AQSI (по одному в каждой строке)
    и составляет на их основе возвращаемый список aqsi_sn_list_new
    '''
    # Разделяем строку на слова
    aqsi_sn_list = aqsi_sn_str.split()
    # Список найденных серийных номеров
    aqsi_sn_list_new = []
    for element in aqsi_sn_list:
        aqsi_sn_pos = re.search('100\d+', element)
        if aqsi_sn_pos:
            aqsi_sn_list_new.append(aqsi_sn_pos.group(0))
    return aqsi_sn_list_new


def print_check_str(res_dict):
    '''
    Функция print_check_str принимает словарь с результатами проверки терминалов и распредляет информацию из него на
    три строки: успешно прошедшие проверку, провалившие проверку и не обнаруженные в реестре. Далее строки объединяются
    в одну, которую функция возвращает
    '''
    # Результирующая строка
    result_aqsi_str = ''
    # Строка успешно прошедших проверку терминалов
    ok_aqsi_str = ''
    # Строка не прошедших проверку терминалов
    fisk_aqsi_str = ''
    # Строка не наденных в реестре терминалов
    not_found_str = ''
    # Распределение терминалов по строкам
    for sn in res_dict:
        if res_dict[sn] == -1:
            fisk_aqsi_str += sn + '\n'
        elif res_dict[sn] == 1:
            ok_aqsi_str += sn + '\n'
        elif res_dict[sn] == 0:
            not_found_str += sn + '\n'
    # Добавление строк в результирующую с соответствующими подписями
    if len(fisk_aqsi_str) > 0:
        result_aqsi_str += "Фискализированные терминалы AQSI\n (НЕИСПРАВНЫЕ): \n" + fisk_aqsi_str + "\n"
    if len(ok_aqsi_str) > 0:
        result_aqsi_str += "Не фискализированные терминалы AQSI\n (ОК): \n" + ok_aqsi_str + "\n"
    if len(not_found_str) > 0:
        result_aqsi_str += "Следующие терминалы в базе данных\n налоговой НЕ НАЙДЕНЫ: \n" + not_found_str
    return result_aqsi_str


def main():
    # Набор серийных номеров терминалов AQSI для примера
    example_aqsi_str = '1006529827014676\n1006078009010998\n1006710060021992\n1006869639018788\n1006814919022687\n' \
                       '1006239226000826\n1006955057016596\n1006971425023499\n1006117069023371\n1006749264015028\n' \
                       '1006256370020376\n1006498677011579\n1006840781017412\n1006951656021237\n1006385058008524'
    aqsi_list = read_aqsi_list(example_aqsi_str)
    aqsi_res_dict = get_nalog_info(aqsi_list)
    res_aqsi_str = print_check_str(aqsi_res_dict)
    print(res_aqsi_str)


if __name__ == '__main__':
    main()

