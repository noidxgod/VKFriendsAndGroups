import vk
import requests
from bs4 import BeautifulSoup
import pandas as pd
#c9629303c9629303c9629303c0c91e256dcc962c9629303abebc34f6c48065e41da0bd4

if __name__ == "__main__":
    token = "c9629303c9629303c9629303c0c91e256dcc962c9629303abebc34f6c48065e41da0bd4"
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)
    screenname = str(input())
    try:
        id = vk_api.utils.resolveScreenName(screen_name = screenname, v=5.92)
        dict = { "Имя":'', "Ссылка1":'', "Подписки":'',"Ссылка2":''}
        dict["Ссылка1"] = (vk_api.friends.get(user_id=id['object_id'], v=5.92, order='hints')["items"])
        dict["Ссылка2"] = (vk_api.users.getSubscriptions(user_id=id['object_id'], v=5.92, order='hints')["groups"]["items"])
        for i in range(0,len(dict["Ссылка1"])):
            dict["Ссылка1"][i] = "https://vk.com/id" + str(dict["Ссылка1"][i])
        for i in range(0,len(dict["Ссылка2"])):
            dict["Ссылка2"][i] = "https://vk.com/club" + str(dict["Ссылка2"][i])
        names = []
        titles = []
        print("Загрузка друзей..")
        for i in range(0, len(dict["Ссылка1"])):
            print('\r', 'Процесс', str(i * 100 // len(dict["Ссылка1"])), '%', end='')
            url = str(dict["Ссылка1"][i])
            response = requests.get(url)
            soup = str(BeautifulSoup(response.text, 'lxml'))
            str1 = "title"
            str2 = "ВКонтакте</title"
            names.append(soup[soup.rfind(str1, 0, soup.rfind(str2)) + 6:soup.rfind(str2) - 3])
        print('\r', 'Процесс', str(100), '%', end='')
        print()
        print("Загрузка групп..")
        for i in range(0, len(dict["Ссылка2"])):
            print('\r', 'Процесс', str(i * 100 // len(dict["Ссылка2"])), '%', end='')
            url = str(dict["Ссылка2"][i])
            response = requests.get(url)
            soup = str(BeautifulSoup(response.text, 'lxml'))
            str1 = "title"
            str2 = "ВКонтакте</title"
            titles.append(soup[soup.rfind(str1, 0, soup.rfind(str2)) + 6:soup.rfind(str2) - 3])
        print('\r', 'Процесс',str(100), '%', end='')
        dict["Имя"] = names
        dict["Подписки"] = titles
        excel = pd.DataFrame.from_dict(dict, orient='index')
        excel = excel.transpose()
        excel.to_excel('./vk.xlsx')
    except vk.exceptions.VkAPIError:
        print("Ошибка, возможно профиль пользователя закрыт.")
