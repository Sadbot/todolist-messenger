import logging
import pymorphy2
import string

from pymorphy2.analyzer import Parse
from pymorphy2.tagset import OpencorporaTag
from typing import List


class MorphAnalyzer:

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger('morph_analyzer')
        self.morph = pymorphy2.MorphAnalyzer()
        self.filter_pos = (
            'NPRO',  # местоимения
            'INTJ',  # междометия
            'PRCL',  # частицы
            'CONJ',  # союзы
            'PREP'  # предлоги
        )

    def is_part_of_speech(self, pars_word: Parse) -> bool:
        """
        Если слово - это дополнительная часть речи (местоимение или т.п.)
        то возвращаем False
        """
        is_additional_part = pars_word.tag.POS not in self.filter_pos
        if pars_word.word in ('по', 'есть', ):
            is_additional_part = True
        self.logger.debug(f'is part of speech: {pars_word.word}, decision: {is_additional_part}')

        return is_additional_part

    def parse_most_valuable_word(self, word: str) -> Parse:
        """
        Полный морфологический разбор слова и
        возвращение морфологически наиболее подходящего
        """
        return next(iter(self.morph.parse(word)))

    def clear_punctuation(self, text):
        """ Удаление знаков препинания и лишних пробелов из исходного текста """
        trans_tab = str.maketrans(dict.fromkeys(string.punctuation))
        result = text.strip().translate(trans_tab)
        self.logger.debug(f'clear punctuation before: {text}, after: {result}')

        return result

    def analyze_normal_sentences(self, text: str) -> List[str]:
        """Нормализация частей предложения"""
        normal_list = []
        for word in text.split(','):
            word = self.clear_punctuation(word)
            parse_word = self.parse_most_valuable_word(word)
            if self.is_part_of_speech(parse_word):
                normal_list.append(parse_word.normal_form)
        self.logger.debug(f'Analyze sentences: {text}, normal_list = {normal_list}')
        return normal_list

    def analyze_words(self, text: str) -> List[Parse]:
        """Производится разбивка строки на слова, парсинг/анализ каждого слова
        и возвращение списка распарщенных объектов
        """
        normal_list = []
        prepare_mask = {
            ord(' '): ord(','),
            ord(';'): ord(','),
            ord('.'): ord(','),
            ord('/'): ord(','),
            ord('\\'): ord(','),
        }
        prepared_text = text.translate(prepare_mask).split(',')
        prepared_text = filter(None, prepared_text)

        for word in prepared_text:
            word = self.clear_punctuation(word)
            parse_word = self.parse_most_valuable_word(word)
            if self.is_part_of_speech(parse_word):
                normal_list.append(parse_word)

        return normal_list

    def analyze_list_normal_words(self, text: str) -> List[str]:
        analyze_list = self.analyze_words(text)
        normal_list = [parse.normal_form for parse in analyze_list]
        self.logger.debug(f"text = {text}, normal_list = {normal_list}")

        return normal_list


if __name__ == '__main__':
    m = MorphAnalyzer()
    w = m.analyze_list_normal_words('люди гуляли, и бегали')
    w = m.analyze_words('тест Сергей Гулько бегает по кругу')
    # Выделить из предложения только Имя и Фамилию
    print(w)
    w2 = [i for i in w if 'Surn' in i.tag or 'Name' in i.tag]
    print(w2)
