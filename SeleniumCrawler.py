import sqlite3
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys



class SeleniumCrawler(object):

    def __init__(self, databaseLocation):
        self._goldenFondResourse = "https://otvet.mail.ru/golden/"
        self._website = "https://otvet.mail.ru/"
        self._databaseLocation = databaseLocation

  

        conn = sqlite3.connect(self._databaseLocation, timeout=10)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS data(
                            'q_id' INTEGER,
                            'title' TEXT,
                            'category'TEXT,
                            'subcategory' TEXT,
                            'comment'TEXT,
                            'answer'  TEXT);       
                           """)

    def getGoldenFondQuestionList(self):
        """
        список вопросов из Золотого Фонда Mail.ru
        """
        self._driver.get(self._goldenFondResourse)
        questionsText = self._driver.find_elements_by_class_name("q--li--text")
        return questionsText

    def GoldenQuestionPageArray(self, questionURL:str):
        """
        :param questionURL: 
        :return data about QA and Author:
        """
        self._driver.get(questionURL)
        questionTitle = self._driver.find_element_by_class_name("q--qtext entry-title").text
        questionSubtitle = self._driver.find_element_by_class_name("q--qcomment h4 entry-content").text
        questionBestAnswer = self._driver.find_element_by_class_name("a--atext-value").text
        bestAnswerAuthorRating = self._driver.find_element_by_class_name("a--2line").text
        bestAnswerLikeCount = self._driver.find_elements_by_class_name("totalmarks bold btn--text")[1].text
        return questionTitle, questionSubtitle, questionBestAnswer, bestAnswerAuthorRating,bestAnswerLikeCount


    def loadMore(self, questionURL):
        """
        if this is the last question in array, click button more
        :param questionURL:
        """
        self._driver.get(questionURL)

    def clickNext(self):
        self._driver.get(self._goldenFondResourse)
        prevClick = 0
        currentClick = 1
        while prevClick != currentClick:
            try:
                prevClick = len(self._driver.find_elements_by_class_name("q--li--text"))
                nextButton = self._driver.find_element_by_class_name('btn btn-more btn-primary')
                nextButton.click()
                time.sleep(3)
                currentClick = len(self._driver.find_elements_by_class_name("q--li--text"))
                print(prevClick, currentClick)
            except Exception:
                pass






    # def getOneQAFromList(self):
if __name__ == "__main__":
    crawler = SeleniumCrawler("database")
    x = crawler.clickNext()
    # crawler.getGoldenFondQuestionList()
    # for question in crawler._questionsText:
    #     print(question.get_property('href') ,question.text)




