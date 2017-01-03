from grab import Grab
g = Grab(log_file='out.html')
g.go("http://embargo.ua/")
MASSIV_NAME_ITEM = []  # Массив имен товаров
MASSIV_PRICE_ITEM = []  # Массив для цены товара
MASSIV_OF_STOCK_ITEM = []  # Массив в котором хранятся значения есть ли товар на складе или нет
MASSIV_LINK_ITEM = []  # Массив для ссылок на товар
DICT_LINK_AND_NAME = {} # Словарь  имен категорий и ссылок на них


def LinkAllCategoryAndName():  # Парсит имена и ссылки категорий в словарь
    for link, name in zip(g.xpath_list('//a[@class = "home_category_url_title"]//@href'), g.xpath_list('//a[@class = "home_category_url_title"]')):
        DICT_LINK_AND_NAME[name.text_content()] = link
    return DICT_LINK_AND_NAME


def Name_Of_Item_Title():  # Парсит имена предметов
    for i in g.xpath_list('//a[@class = "item_name_link"]'):
        MASSIV_NAME_ITEM.append(i.text_content())
    return MASSIV_NAME_ITEM


def Price_Of_Item():  # Парсит цену предмета
    for i in g.xpath_list('//div[@class = "item_price" ]'):
        MASSIV_PRICE_ITEM.append(i.text_content())
    return MASSIV_PRICE_ITEM


def Link_Of_Item():  # парсит  ссылку на предмет
    for i in g.xpath_list('//a[@class = "item_name_link"]//@href'):
        MASSIV_LINK_ITEM.append(i)
    return MASSIV_LINK_ITEM


def Exsist_In_Stock():  # парсит есть ли на сайте товар
    for i in g.xpath_list('//div[@class = "product_brief_block_wrap"]'):
        if "Нет на складе" in i.text_content():
            MASSIV_OF_STOCK_ITEM.append("Нет на складе")
        else:
            MASSIV_OF_STOCK_ITEM.append("Есть на складе")
    return MASSIV_OF_STOCK_ITEM


def Write_Result(name_file):   # запись результата парсинга в xml
    file = open(str(name_file) + '.xml', 'w', encoding='utf-8')
    file.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + '\n')
    file.write('<data-set xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' + '\n')
    for item, link, price, stock in  zip(MASSIV_NAME_ITEM, MASSIV_LINK_ITEM,  MASSIV_PRICE_ITEM, MASSIV_OF_STOCK_ITEM):
        file.write('<record>')
        file.write('<Item>' + str(item) + '</Item>')
        file.write('<Link>' + str(link) + '</Link>')
        file.write('<Price>' + str(price) + '</Price>')
        file.write('<Stock>' + str(stock) + '</Stock>')
        file.write('</record>' + '\n')
        file.flush()
    file.write('</data-set>')
    file.close()
    file = open(str(name_file) + '.xml', 'r', encoding='utf-8')
    y = file.read().replace('&', '')
    file = open(str(name_file) + '.xml', 'w', encoding='utf-8')
    file.write(y)
    file.close()
    MASSIV_NAME_ITEM.clear()
    MASSIV_LINK_ITEM.clear()
    MASSIV_PRICE_ITEM.clear()
    MASSIV_OF_STOCK_ITEM.clear()


def Start_Parsing():
    dict = LinkAllCategoryAndName()
    for link in dict:
        g.go(dict[link] + "all/")
        Name_Of_Item_Title()
        Link_Of_Item()
        Price_Of_Item()
        Exsist_In_Stock()
        Write_Result(link)
        print("Конец парсинга " + str(link))

Start_Parsing()