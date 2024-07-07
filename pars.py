import requests
from bs4 import BeautifulSoup



def parse(url):
    response = requests.get(url)
    # Создайте объект BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    # Найдите все теги <p>
    p_tags = soup.find_all('p')

    # Извлеките текст из каждого тега <p>
    visible_texts = [p_tag.get_text(strip=True) for p_tag in p_tags]
    full_text = ' '.join(visible_texts)
    error = "На сайте информации нет, опирайся на свои знания"
    if full_text == "К сожалению, мы не смогли найти запрашиваемую вами страницу. Пожалуйста, обратитесь к владельцу сайта, с которого вы перешли на эту ссылку, чтобы сообщить ему, что ссылка не работает.":
        return error
    else:
    # Верните результат
        return full_text


