#!/usr/bin/python
#-*- conding: utf-8 -*-
import json
import logging
from asyncio import sleep

from decouple import config

from models import Message
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import MMSMessage

logging.basicConfig(level=logging.ERROR)


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
        return True
    except BaseException as e:
        if e == 'Timeout: Not logged':
            driver.close()
            connect_bot()


def get_chats_ids(driver):
    try:
        chats_ids = driver.get_all_chat_ids()
        return chats_ids
    except BaseException as e:
        print(e)
        return False

#def get_message(driver, id_chat):
#   unread_messages = driver.get_unread_messages_in_chat(str(id_chat), include_me=True)


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


def save_message(messages_chat: list):
    """
    Faz o salvamento das frases no banco de dados.
    :param message: Texto contendo as mensagem.
    :type message: dict
    """
    db_url = config('DATABASE_URL')
    port = config('DATABASE_PORT', cast=int)
    m = Message(db_url, port)
    # Precisa salvar as mensagens em banco de dados



def save_word(words):
    w = Word()
    for word in words:
        w.save(word)


def get_unread_messages(driver):
    for chat_id in chats_ids:
        if chat_id is not None:
            try:
                messages_in_chat = driver.get_unread(include_me=True, include_notifications=True)
                return messages_in_chat
            except AttributeError:
                return None


def get_data_message(content):
    for msg in content.messages:
        if msg.type not in ['call_log', 'e2e_notification', 'gp2']:
            msg_type = msg.type,
            chat_id_obj = json.dumps(msg.chat_id['_serialized']),
            chat_id = chat_id_obj[0][1:-1]
            if msg_type == 'image':
                msg_content = 'IMG',
            elif isinstance(msg, MMSMessage):
                msg_content = 'MMSMessage'
            else:
                msg_content = msg.content
            message = {
                'msg_id': msg.id,
                'msg_type': msg.type,
                'msg_chat_id': chat_id,
                'msg_sender_id': msg.sender.id,
                'msg_sender': msg.sender.name,
                'msg_date': msg.timestamp,
                'msg': msg_content,
            }
            return message
        return None


if __name__ == '__main__':
    driver = WhatsAPIDriver(loadstyles=True)
    connect = connect_bot()
    while connect is True:
        chats_ids = get_chats_ids(driver)
        unread_message = get_unread_messages(driver)
        if unread_message is not None:
            for content in unread_message:
                message = get_data_message(content)
                if message is not None:
                    save_message(message)
                continue
        continue
