#!/usr/bin/python
#-*- conding: utf-8 -*-

import logging
from asyncio import sleep
from webwhatsapi import WhatsAPIDriver

logging.basicConfig(level=logging.ERROR)

driver = WhatsAPIDriver(loadstyles=True)


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


if __name__ == '__main__':
    connect_bot()
