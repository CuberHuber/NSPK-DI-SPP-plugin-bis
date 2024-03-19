"""
Парсер плагина SPP

1/2 документ плагина
"""
import logging
import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.spp.types import SPP_document


class BIS:
    """
    Класс парсера плагина SPP

    :warning Все необходимое для работы парсера должно находится внутри этого класса

    :_content_document: Это список объектов документа. При старте класса этот список должен обнулиться,
                        а затем по мере обработки источника - заполняться.


    """

    SOURCE_NAME = 'bis'
    HOST = 'https://www.bis.org'
    url_template = f'{HOST}/research/index.htm?bis_fsi_publs_page='
    date_begin = datetime(2019, 1, 1)

    _content_document: list[SPP_document]


    def __init__(self, webdriver, max_count_documents: int = None, last_document: SPP_document = None, *args, **kwargs):
        """
        Конструктор класса парсера

        По умолчанию внего ничего не передается, но если требуется (например: driver селениума), то нужно будет
        заполнить конфигурацию
        """
        # Обнуление списка
        self._content_document = []

        # Webdriver Selenium для парсера
        self._driver = webdriver
        self._max_count_documents = max_count_documents
        self._last_document = last_document

        # Логер должен подключаться так. Вся настройка лежит на платформе
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Parser class init completed")
        self.logger.info(f"Set source: {self.SOURCE_NAME}")
        ...

    def content(self) -> list[SPP_document]:
        """
        Главный метод парсера. Его будет вызывать платформа. Он вызывает метод _parse и возвращает список документов
        :return:
        :rtype:
        """
        self.logger.debug("Parse process start")
        try:
            self._parse()
        except Exception as e:
            self.logger.debug(f'Parsing stopped with error: {e}')
        else:
            self.logger.debug("Parse process finished")
        return self._content_document


    def _parse(self):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter to {self.HOST}")

        # ========================================
        # Тут должен находится блок кода, отвечающий за парсинг конкретного источника
        # -
        checker = True
        page_number = 0


        while checker:
            page_number = page_number + 1
            if page_number >= 4: break

            self.logger.info(f'Загрузка страницы: {self.url_template}{page_number}')
            self._driver.get(url=f"{self.url_template}{page_number}")
            req = requests.get(f"{self.url_template}{page_number}")
            time.sleep(5)
            page = self._driver.page_source
            if req.status_code == 200:
                checker = self._parse_page(page)
            else:
                self.logger.error('Не удалось загрузить страницы')

        # Логирование найденного документа
        # self.logger.info(self._find_document_text_for_logger(document))

        # ---
        # ========================================
        ...

    def _parse_page(self, page) -> bool:
        soup = BeautifulSoup(page, 'html.parser')
        page_with_links = soup.find('table', class_='documentList')
        if page_with_links is None:
            return False

        for link in page_with_links.find_all('tr'):
            title = f"""{(link.find('div', class_="title")).find('a').get_text(strip=True)}"""
            div_pdf_info = f"""{(link.find('div', class_="pdfdocinfo")).get_text(strip=True).replace("&nbsp;", " ")}""".replace(
                '\n', ' ').replace('\t', ' ').replace("¶", " ").replace("▲",
                                                                        " ").replace(
                '\xa0', ' ').replace('\r', ' ').replace('—', "-").replace("’", "'").replace("“",
                                                                                            '"').replace(
                "”", '"').replace(" ", " ").replace("<", "_").replace(">", "_").replace(":",
                                                                                        "_").replace(
                '"', "_").replace("/",
                                  "_").replace(
                "\\", "_").replace("?", "_").replace("*", "_")
            if "|" in div_pdf_info:
                doc_type = (div_pdf_info.split('|'))[0]
            else:
                doc_type = div_pdf_info
            print(f"Тип документа: {doc_type}")
            abstract = ""
            autor = ""
            print(f"Название: {title}")
            source = (link.find('div', class_="title")).find('a').get('href')
            date_info = link.find('td', class_="item_date").get_text(strip=True)
            official_date = datetime.strptime(date_info, '%d %b %Y')
            if official_date > self.date_begin:
                web_link: str = self.HOST+source
                try:
                    if ".pdf" not in source:
                        doc_page = requests.get(web_link)
                        new_soup = BeautifulSoup(doc_page.content.decode('utf-8'), 'html.parser')
                        interval_source = new_soup.find('a', class_="pdftitle_link")
                        div_autor = new_soup.find("div", class_="authorline")
                        if div_autor:
                            autor = (self.get_text_from_div(div_autor)).replace('\n', ' ').replace('\t', ' ').replace("¶",
                                                                                                                      " ").replace(
                                "▲",
                                " ").replace(
                                '\xa0', ' ').replace('\r', ' ').replace('—', "-").replace("’", "'").replace("“",
                                                                                                            '"').replace(
                                "”", '"').replace(" ", " ").replace("<", "_").replace(">", "_").replace(":",
                                                                                                        "_").replace(
                                '"', "_").replace("/",
                                                  "_").replace(
                                "\\", "_").replace("|", "_").replace("?", "_").replace("*", "_")
                        div_cms_content = new_soup.find("div", id="cmsContent")
                        if div_cms_content:
                            abstract = (self.get_text_from_div(div_cms_content)).replace('\n', ' ').replace('\t',
                                                                                                            ' ').replace(
                                "¶", " ").replace("▲",
                                                  " ").replace(
                                '\xa0', ' ').replace('\r', ' ').replace('—', "-").replace("’", "'").replace("“",
                                                                                                            '"').replace(
                                "”", '"').replace(" ", " ").replace("<", "_").replace(">", "_").replace(":",
                                                                                                        "_").replace(
                                '"', "_").replace("/",
                                                  "_").replace(
                                "\\", "_").replace("|", "_").replace("?", "_").replace("*", "_")
                        while "  " in abstract:
                            abstract = abstract.replace("  ", " ")
                        while "  " in autor:
                            autor = autor.replace("  ", " ")

                        if interval_source is not None:
                            source_link = interval_source.get('href')
                            web_link = f"{self.HOST}{source_link}"

                        else:
                            self.logger.debug(f'Для {self.HOST}{source} не получилось найти ссылку на документ')
                except:
                    self.logger.error(f'Ошибка парсинга')
                else:
                    document = SPP_document(
                        None,
                        title=title,
                        abstract=abstract if abstract else None,
                        text=None,
                        web_link=web_link,
                        local_link=None,
                        other_data=None,
                        pub_date=official_date,
                        load_date=None,
                    )
                    if autor:
                        document.other_data = {'author': autor}
                    self.find_document(document)
            else:
                return False

        return True

    @staticmethod
    def _find_document_text_for_logger(doc: SPP_document):
        """
        Единый для всех парсеров метод, который подготовит на основе SPP_document строку для логера
        :param doc: Документ, полученный парсером во время своей работы
        :type doc:
        :return: Строка для логера на основе документа
        :rtype:
        """
        return f"Find document | name: {doc.title} | link to web: {doc.web_link} | publication date: {doc.pub_date}"

    def get_text_from_div(self, div):
        text = ""
        for element in div.contents:
            if element.name == "div":
                text += self.get_text_from_div(element)
            if element.name == "p":
                text += element.get_text() + " "
            if element.name == "a":
                text += element.get_text() + " "
        return text

    def find_document(self, _doc: SPP_document):
        """
        Метод для обработки найденного документа источника
        """
        if self._last_document and self._last_document.hash == _doc.hash:
            raise Exception(f"Find already existing document ({self._last_document})")

        if self._max_count_documents and len(self._content_document) >= self._max_count_documents:
            raise Exception(f"Max count articles reached ({self._max_count_documents})")

        self._content_document.append(_doc)
        self.logger.info(self._find_document_text_for_logger(_doc))