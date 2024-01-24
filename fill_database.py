from src.database.models import DVDModel
from src.database.models import PhysicalDVDModel
from src.database.models import CategoryModel
from src.database.models import DVDCategoryRelationModel
from src.database.models import HistoryLogModel
from src.database.models import ClientModel
from src.database.database_manager import DatabaseManager
from datetime import datetime
from random import randrange

def get_dvd_id(dvd_name):
    return DVDModel.select({'name': dvd_name}).get_id()

def get_physical_codes():
    alph = "ABCDEFGHIJKLMNOPRSTWXYZ"
    num = "0123456789"
    code = ''
    codes = []
    for _i in range(100):
        while code in codes or code == '':
            code = ''
            code += alph[randrange( len(alph) )] \
            + alph[randrange(len(alph))] \
            + num[randrange(len(num))] \
            + num[randrange(len(num))] \
            + num[randrange(len(num))]
        codes.append(code)
        code = ''
    return codes

dvd_arr = [
    { 'name': "Nietykalni",                         'date': datetime(2011, 9, 23) },
    { 'name': "Zielona mila",                       'date': datetime(1999, 12, 6) },
    { 'name': "Ojciec chrzestny",                   'date': datetime(1972, 3, 14) },
    { 'name': "Dwunastu gniewnych ludzi",           'date': datetime(1957, 4, 10) },
    { 'name': "Forrest Gump",                       'date': datetime(1994, 6, 23) },
    { 'name': "Ojciec chrzestny II",                'date': datetime(1974, 12, 12) },
    { 'name': "Władca Pierścieni: Powrót króla",    'date': datetime(2003, 12, 1) },
    { 'name': "Władca Pierścieni: Dwie wieże",      'date': datetime(2002, 12, 5) },
    { 'name': "Siedem",                             'date': datetime(1995, 9, 15) },
    { 'name': "Podziemny krąg",                     'date': datetime(1999, 9, 10) },
    { 'name': "Pianista",                           'date': datetime(2002, 5, 24) },
    { 'name': "Jocker",                             'date': datetime(2019, 8, 31) },
    { 'name': "Incepcja",                           'date': datetime(2010, 7, 8) },
    { 'name': "Wyspa tajemnic",                     'date': datetime(2010, 2, 13) },
]

category_arr = [
    'akcja',            #1
    'horror',           #2
    'thriller',         #3
    'psychologiczny',   #4
    'przygodowy',       #5
    'tajemniczy',       #6
    'mroczny',          #7
    'biograficzny',     #8
    'dramat',           #9
    'komedia',          #10
    'fantasy',          #11
    'wojenny',          #12
    'kryminał',         #13
    'surrealistyczny',  #14
    'sci-fi',           #15
]
dvd_category_relation_arr = [
    [8, 9, 10],
    [9],
    [9],
    [9],
    [9, 10],
    [9],
    [11, 5],
    [11, 5],
    [3, 13],
    [3, 4],
    [8, 9, 12],
    [9, 13, 4],
    [14, 15, 3],
    [3, 9],
]
#
# def get_random_name():
#     names = [ 'Marek', 'Klaudiusz', 'Bartek', 'Bogdan', 'Bogumił', 
#             'Tomek', 'Freddy', 'Sandra', 'Karolina', 'Zuzanna', 'Jaśko']
#     return names[randrange(len(names))]
#
# def get_random_last_names():
#     names = ['Kawazaki', 'Cago', 'Krico', 'Estriper', 'Fazbear', 
#              'Paluch', 'Stopa', 'Kciuk', 'Drill']
#     return names[randrange(len(names))]
#
# def get_random_phone_number():
#     digits = '1234567890'
#     number = ''
#     for _i in range(9):
#         number += digits[randrange(len(digits))]
#     return number
#
# client_arr = []
# for _x in range(20):
#     name = get_random_name()
#     last_name = get_random_last_names()
#     client_arr.append({
#         'first_name': name,
#         'last_name': last_name, 
#         'email': name.lower() + last_name.lower() + '@poczta.pl', 
#         'phone_number': get_random_phone_number()
#     })


history_log_arr = [
    
]
rental_state_arr = []

def insert():
    for dvd in dvd_arr:
        DVDModel.insert(dvd)

    codes = get_physical_codes()
    physical_dvd_arr = [{
        'physical_code': code, 
        'dvd_id': randrange(1, len(dvd_arr)+1), 
        'rental_state': DatabaseManager.RETURNED
    } for code in codes]

    for physical_dvd in physical_dvd_arr:
        PhysicalDVDModel.insert(physical_dvd)

    categories = [{'name': x} for x in category_arr]
    for category in categories:
        CategoryModel.insert(category)

    for dvd, relation in enumerate(dvd_category_relation_arr):
        for category in relation:
            DVDCategoryRelationModel.insert({'dvd_id':dvd+1, 'category_id': category})

    # for client in client_arr:
    #     ClientModel.insert(client)
    #
    # for history_log in history_log_arr:
    #     HistoryLogModel.insert(history_log)

if __name__ == "__main__":
    DatabaseManager.all_tables_delete()
    DatabaseManager.all_tables_create()
    insert()
