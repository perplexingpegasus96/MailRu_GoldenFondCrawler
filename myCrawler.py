from bs4 import BeautifulSoup as bs
import requests
import re



class myCrawler(object):


    def getDataFromSoup(self, q_id, soup):
        """
        Принимает обьект BS и возвращает нужную инфу из него
        :return:
        [описание вопроса, сам вопрос, категорию, подкатегорию,
        ответы на вопрос]
        """
        try:
            title = soup.find('h1', 'q--qtext').text.replace("'", '')
            print(title)
        except AttributeError:
            title = None

        try:
            category = bs(str(soup.find('a', 'black list__title list__title')), "xml")\
                                .select_one("span[itemprop*=title]").text.replace("'", '')
        except AttributeError:
            category = None
        print(category)

        try:
            sub_category = bs(str(soup.find('a', 'medium item item_link selected')), "xml")\
                            .select_one("span[itemprop*=title]").text.replace("'", '')
        except AttributeError:
            sub_category = None
        print(sub_category)

        raw_comments = soup.find_all('div', 'q--qcomment medium')
        if raw_comments:
            comments = ' '.join([q.text.replace("'", '') for q in raw_comments])
        else:
            comments = None
        print (comments)

        raw_answers = soup.find_all('div', 'a--atext atext')
        if raw_answers:
            answers = "||".join([a.text.replace("'", '') for a in raw_answers])
        else:
            answers = [None]
        print(answers)
        if title != None:
            return q_id, title, category, sub_category, comments, answers

    def getPage(self, questNum):
        """
        Берем код страницы с ответов Мэил ру
        :param questNum:
        :return:
        """
        text_page = requests.get('https://otvet.mail.ru/question/'
                                 + str(questNum)).text
        return text_page


    def pageToSoup(self, page):
        """
        Принимает номер страницы в mail.ru и возвращает обьект BS
        :return:
        обьект BS
        """
        soup = bs(page, 'lxml')
        return soup

    def writeToDB(self, parsedData, cursorObject, connObject):
        """
        записываем в бд строку
        :return: void
        """
        query = "INSERT INTO data(q_id, title, category,subcategory,comment, answer) " \
                "                 VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}')"\
                                        .format(parsedData[0],
                                                parsedData[1],
                                                parsedData[2],
                                                parsedData[3],
                                                parsedData[4],
                                                parsedData[5])
        print(query)

        cursorObject.execute(query)
        connObject.commit()

    def __isPageValid(self, soup):
        """
        Можем ли мы обработать стратницу и достать оттуда данные?
        :return:
        да/нет
        """
        content = soup.find_all('div', 'page-404-white')
        if content:
            return False
        else:
            return True



    def fetchPages(self, from_quest, till_quest):
        """
        Создадим генератор для страниц, добавляем в генератор только
        правильные страницы
        :return:
        генератор со страницами
        """
        for q_id in range(from_quest, till_quest):
            soup = self.pageToSoup(self.getPage(q_id))
            #проверим на правильность страничку
            if soup != None and self.__isPageValid(soup):
                yield(q_id, soup)
            else:
                self.loggingFunction(q_id)


    def downloadPages(self, generator, cursorObject, connObject):
        """
        для каждого обьекта генератора, обработаем страницу и запихнем в базу данных
        :return:
        """
        for q_id, page in generator:
            data = self.getDataFromSoup(q_id, page)
            self.writeToDB(data, cursorObject, connObject)


    def loggingFunction(self, q_id):
        """
        логируем в файл ошибку страницы
        :param q_id:
        :return:
        """
        with open('log.txt', 'a') as f:
            f.write(str(q_id) + '\n')