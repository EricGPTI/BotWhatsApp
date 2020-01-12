#!/usr/bin/python
#-*- conding: utf-8 -*-

import logging
from asyncio import sleep
from webwhatsapi import WhatsAPIDriver


logging.basicConfig(level=logging.ERROR)

driver = WhatsAPIDriver(loadstyles=True)


# connection = MongoClient('192.168.10.165', 27017)
# db = connection.whatsapp
#
# es = Elasticsearch([{'host': '192.168.10.165', 'port': 9200}])

def connect_bot():
    """
    Roda a função de conexão com whatsapp. Se conecatado chama a função main, se não chama a sim mesma recursivamente.
    :return: Não retorna nada.
    """
    try:
        sleep(10)
        print('Connecting...')
        print('Waiting for loging...')
        driver.wait_for_login()
        print('Bot Starded!')
        get_msg()
    except BaseException as e:
        if e == 'Timeout: Not logged':
            driver.close()
            connect_bot()


def get_msg():
    while True:
        chats_ids = driver.get_all_chat_ids()
        for id in chats_ids:
            if id is not None:
                # if chat == '553499768872-1541449260@g.us' or chat == '5511995192105-1520886507@g.us':
                # messages = driver.get_all_messages_in_chat(chat=chat_teste)
                contact_message = driver.get_unread_messages_in_chat(str(id), include_me=True)
                for msg in contact_message:
                    message = msg.content
                    print(message)
                    frase(message)
                    words = word_tokenize(message.lower())
                    save_word(words)
                continue
            else:
                continue
        continue
    get_msg()


def unread_msg():
    """
    Busca mensagens não lidas enviadas por grupos ou pessoas.
    :return: Objeto contacts.
    :rtype: Object.
    """
    for contact in driver.get_unread():
        if contact is None:
            unread_msg()
        return contact


def stop_words(words):
    """
    Trata texto retornando os stopwords.
    :param words: Lista de palavras
    :type words: List
    :return: Lista de stopwords.
    :rtype: List
    """
    stops = stopwords.words('portuguese')
    return stops


def frase(message):
    """
    Faz o salvamento das frases no banco de dados.
    :param message: Texto contendo as mensagem.
    :type message: String
    """
    f = Frase()
    save = f.save(message)

def save_word(words):
    w = Word()
    for word in words:
        w.save(word)


'''
    #contact = unread_msg()
    #if contact is None:
    #    main()
    #for data_message in contact.messages:
    #    try:
    #        messsage = data_message.content
    #    except AttributeError as e:
    #        if str(e) == "'NoneType' object has no attribute 'messages'":
    #            continue
    #        elif str(e) == "'MMSMessage' object has no attribute 'content'":
    #            continue
    #        elif str(e) == "'MediaMessage' object has no attribute 'content'":
    #            continue
    #        elif str(e) == "'Message' object has no attribute 'content'":
    #            continue
    #        main()

def insert_db(doc_update):
    new_date_db = doc_update['Date_Msg']
    dates = date_convert.date_time_db(new_date_db)

    date_now = dates[0]
    date_msg_converted = dates[1]
    doc_update.update(Date_Msg=date_msg_converted, Date_Update=date_now)
    counter = 0
    try:
        db.updates.insert_one(doc_update)
        return True
    except(BaseException) as e:
        if str(e).__contains__("E11000 duplicate key error collection"):
            print(e)
            pass
        else:
            with open('log.txt', 'a') as l:
                l.write("Date: " + str(date_now) + "\n" + "Error: " + str(e) + "\n" + "Local: InsertDB" + "\n\n")
                counter += 1
                if counter == 100:
                    l.write("Date: " + str(
                        date_now) + "\n" + "uma atualização não foi salva por problemas com o banco.\n\n")
                    pass
                else:
                    sleep(3)
            return False


def insert_index(doc_update):
    new_date_index = doc_update['Date_Msg']
    dates = date_convert.date_index(new_date_index)
    date_now = dates[0]
    date_msg_converted = dates[1]
    doc_update.update(Date_Msg=date_msg_converted, Date_Update=date_now)
    counter = 0
    del doc_update['_id']
    try:
        res = es.index(index="whatsapp", doc_type="whatsapp", body=doc_update)
        return True
    except(BaseException) as e:
        date_error = str(doc_update['Date_Update'])
        with open('log.txt', 'a') as l:
            l.write("Date: " + date_error + "\n" + "Error: " + str(e) + "\n" + "Local: Insert_Index" + "\n\n")
            counter += 1
            if counter == 100:
                l.write("Date: " + date_error + '\n' + 'uma atualização não foi indexada pelo seguinte erro: ' + str(
                    e) + '\n\n')
                pass
            else:
                sleep(10)
                insert_index(doc_update)
        return False
        main()
'''
