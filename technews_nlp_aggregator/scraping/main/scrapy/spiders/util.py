from urllib.parse import urlparse, unquote
from datetime import date, datetime, timedelta
from string import punctuation
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def extract_date(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
        if (index >= len(arrs)):
            return None
    if (all([arrs[index].isdigit(), arrs[index + 1].isdigit(), arrs[index + 2].isdigit()])):
        year, month, day = map(int, (arrs[index], arrs[index + 1], arrs[index + 2]))
    #date_str = day + '-' + month + '-' + year
        return date(year, month, day)
    else:
        logging.warning("Could not parse date in url: {}".format(url))
        return None

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_names_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_date_from_string(date_str):
    result = None
    if (date_str):
        date_str_l = date_str.split(',')
        month_and_day, year, month_index = None, None, 1
        if (len(date_str_l) == 3):
            month_and_day, year, time = date_str.split(',')
        if (len(date_str_l) == 2):
            month_and_day, year = date_str.split(',')
        if (month_and_day and year):
            month_and_day_l = month_and_day.split()
            if (len(month_and_day_l ) == 2):
                month, day = month_and_day.split()
                if month in month_names:
                    month_index = month_names.index(month) + 1
                if month in month_names_short:
                    month_index = month_names_short.index(month) + 1
                if month_index:
                    article_date = date(int(year), month_index , int(day))
                    result = article_date
    return result

def end_condition(date, go_back_date):
    if not date:
        return False
    if date < go_back_date:
    #if date.year < 2017:
        return True
    else:
        return False


def build_text_from_paragraphs(all_paragraphs, punct_end = ".!?", punct_add_point= ""):
    all_paragraph_text = ""
    for paragraph in all_paragraphs:
        if len(paragraph) == 0 or paragraph[0] == '\n':
            continue
        if (paragraph[-1] in punct_add_point):
            paragraph = paragraph + "."
        if (paragraph[-1] in punct_end):
            paragraph = paragraph + "\n"
        elif (paragraph[-1] in punctuation):
            paragraph = paragraph + " "

        all_paragraph_text = all_paragraph_text + paragraph
    return all_paragraph_text