#!/usr/bin/python
#-*- conding: utf-8 -*-

import logging
from asyncio import sleep
from models import Chat
from decouple import config
from models import Message
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import MMSMessage, MediaMessage

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
    """
    Função que faz a busca dos ids dos chats
    :param driver: Driver de conexão com o whatsapp.
    :type driver: Object.
    :return: Todos os Ids de chats existentes num perfil de whatsapp or False
    :rtype: Lista
    """
    try:
        chats_ids = driver.get_all_chat_ids()
        return chats_ids
    except BaseException as e:
        print(e)
        return False


def unread_msg(driver):
    """
    Busca mensagens não lidas enviadas por grupos ou pessoas.
    :return: Objeto contacts.
    :rtype: Object.
    """
    for contact in driver.get_unread():
        if contact is None:
            unread_msg()
        return contact


def get_unread_messages(chats_ids):
    for chat_id in chats_ids:
        if chat_id is not None:
            try:
                messages_in_chat = driver.get_unread(include_me=True)
                return messages_in_chat
            except AttributeError:
                return None


def get_data_message(unread):
    for msg in unread.messages:
        if msg.type not in ['call_log', 'e2e_notification', 'gp2']:
            msg_type = msg.type,
            chat_id = msg.chat_id['_serialized']
            chat = driver.get_chat_from_id(chat_id)
            chat_obj = chat.get_js_obj()
            chat_name = chat_obj.get('name')
            save_chat(chat_name)
            if msg_type == 'image':
                msg_content = 'IMG',
            elif isinstance(msg, MMSMessage):
                msg_content = 'MMSMessage'
            elif isinstance(msg, MediaMessage):
                msg_content = 'MediaMessage'
            elif isinstance(msg, Message):
                msg_content = msg.safe_content
            else:
                try:
                    msg_content = msg.content
                except AttributeError:
                    msg_content = None
            message = {
                'msg_id': msg.id,
                'msg_type': msg.type,
                'msg_chat_id': chat_id,
                'chat_name': chat_name,
                'msg_sender_id': msg.sender.id,
                'msg_sender': msg.sender.name,
                'msg_date': msg.timestamp,
                'msg': msg_content,
            }
            return message
        return None


def save_message(message: dict):
    """
    Faz o salvamento das frases no banco de dados.
    :param message: Texto contendo as mensagem.
    :type message: dict
    """
    db_url = config('DATABASE_URL')
    port = config('DATABASE_PORT', cast=int)
    m = Message(db_url, port, message)
    m.save_message()


def save_chat(chat_name: str):
    """
    Salva o nome de todos os chats
    :param str_chat: Lista contendo o nome de todos os chats.
    :type str_chat: list
    """
    db_url = config('DATABASE_URL')
    port = config('DATABASE_PORT', cast=int)
    c = Chat(db_url, port, chat_name)
    chat_obj = c.find_chat()
    if chat_obj is False:
        c.update_chat()


if __name__ == '__main__':
    driver = WhatsAPIDriver(loadstyles=True)
    connect = connect_bot()
    while connect is True:
        sleep(3)
        unread = unread_msg(driver)
        if unread is not None:
            message = get_data_message(unread)
            if message is not None:
                save_message(message)
            continue
        continue
