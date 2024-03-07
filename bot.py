import telebot
import googletrans
from telebot import types
# from googletrans import Translator
import sqlite3
from itertools import chain
import deepl

auth_key = "###########################################"
translator = deepl.Translator(auth_key)

bot = telebot.TeleBot('#########################################################')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    mess = f'Yey, {message.from_user.username}, Hi! This is my bot for translating and destroying the language ' \
           f'barrier! Use Info for more information:)' \
           f''

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("My friend👥")
    button2 = types.KeyboardButton("My language📓")
    button3 = types.KeyboardButton("My ID🆔")
    button4 = types.KeyboardButton("Info➿")
    button5 = types.KeyboardButton("Chat☁️️")

    markup.add(button1, button2, button3, button4, button5)

    bot.send_message(message.from_user.id, mess, reply_markup=markup)
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    query = f"""SELECT usersid from infoAboutFriend"""
    cursor.execute(query)
    result = list(chain.from_iterable(cursor.fetchall()))
    if not str(message.from_user.id) in result:
        query = f""" INSERT INTO infoAboutFriend (usersid, idaboutfriend, lang) VALUES({message.from_user.id}, {message.from_user.id}, 'en-gb')"""
        cursor.execute(query)
        query = f"""UPDATE infoAboutFriend SET nickname = '{message.from_user.username}' WHERE usersid = '{message.from_user.id}'"""
        cursor.execute(query)
        db.commit()
        db.close()


@bot.message_handler(content_types=['text'])
def globalfunction(message):
    #bot.send_message(1220686189, f"{message.text} from user {message.from_user.username} +  ### Привет от Никиты!")
    print(message.text + ' from user ' + message.from_user.username)
    if message.text == "My friend👥":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        iduser = message.from_user.id
        query = f"""SELECT idaboutfriend from infoAboutFriend WHERE usersid = {iduser}"""
        cursor.execute(query)
        result = list(chain.from_iterable(cursor.fetchall()))
        query = f"""SELECT nickname from infoAboutFriend WHERE usersid = {result[0]}"""
        cursor.execute(query)
        result = list(chain.from_iterable(cursor.fetchall()))
        mess = f'Yours friend now is {result}. Do you want to change it?'
        db.commit()
        db.close()
        button1 = types.KeyboardButton("No❌")  # a napisana kirillicej
        button2 = types.KeyboardButton("Sim✅")
        markup.add(button1, button2)
        bot.send_message(message.from_user.id, mess, reply_markup=markup)

    if message.text == "Sim✅":
        send = bot.send_message(message.from_user.id, 'Please, write your friends nickname without @')
        bot.register_next_step_handler(send, addtobase)

    if message.text == "No❌":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("My friend👥")
        button2 = types.KeyboardButton("My language📓")
        button3 = types.KeyboardButton("My ID🆔")
        button4 = types.KeyboardButton("Info➿")
        button5 = types.KeyboardButton("Chat☁️")

        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.from_user.id, 'Okay!', reply_markup=markup)

    if message.text == "My language📓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = 'EN-GB'
        languages = "Target languages: Bulgarian (BG), Czech (CS), Danish (DA), German (DE) supports formality, Greek (" \
                    "EL), English (British) (EN-GB), English (American) (EN-US), Spanish (ES) supports formality, " \
                    "Estonian (ET), Finnish (FI), French (FR) supports formality, Hungarian (HU), " \
                    "Italian " \
                    "(IT) supports formality, Japanese (JA), Lithuanian (LT), Latvian (LV), Dutch (NL) supports " \
                    "formality, " \
                    "Polish (PL) supports formality, Portuguese (Brazilian) (PT-BR) supports formality, Portuguese (" \
                    "European) (PT-PT) supports formality, Romanian (RO), Russian (RU) supports formality, " \
                    "Slovak (SK), " \
                    "Slovenian (SL), Swedish (SV), Turkish (TR), Ukrainian (UK), Chinese (simplified) (ZH) "
        bot.send_message(message.chat.id, languages)
        markup.add(btn)
        send = bot.send_message(message.chat.id, 'Type your languages like British English - EN-GB or Russian - RU or Brazil Portugese PT-BR for example',
                                reply_markup=markup)
        bot.register_next_step_handler(send, lang)

    if message.text == "My ID🆔":
        bot.reply_to(message, message.from_user.id)

    if message.text == "Info➿":
        bot.reply_to(message, f"Hi, {message.from_user.username}! This was my first bot here, glad you are using it!")
        bot.send_message(message.from_user.id, "How to use it? \n Use the navigation buttons \n To write to a friend, "
                                               "first use the /My Friend/ button. \n After that, you can text your "
                                               "friend. \n If you have some problems, you can type to me: "
                                               "@wkvivmalina \n This bot cannot send any media \nSpecial thanks to "
                                               "Daniil Zhdanov for his help in testing")

    if message.text == "Chat☁️":
        print(message)
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        query = f""" UPDATE infoAboutFriend SET chat = 1 WHERE usersid = {message.from_user.id}"""
        cursor.execute(query)
        db.commit()
        db.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Stop Chatting❌")
        markup.add(btn)
        bot.send_message(message.from_user.id, 'Now, you are chatting with you friend \n type any text',
                         reply_markup=markup)

    if message.text == "Stop Chatting❌":
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        query = f""" UPDATE infoAboutFriend SET chat = 0 WHERE usersid = {message.from_user.id}"""
        cursor.execute(query)
        db.commit()
        db.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("My friend👥")
        button2 = types.KeyboardButton("My language📓")
        button3 = types.KeyboardButton("My ID🆔")
        button4 = types.KeyboardButton("Info➿")
        button5 = types.KeyboardButton("Chat☁️")

        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.from_user.id, 'Now, you are stop chatting with you friend',
                         reply_markup=markup)

    else:
        if message.text != 'Chat☁️':
            db = sqlite3.connect('bot.db')
            cursor = db.cursor()
            query = f""" SELECT chat from infoAboutFriend WHERE usersid = {message.from_user.id}"""
            cursor.execute(query)
            chat_switcher = cursor.fetchall()
            db.commit()
            db.close()
            print(chat_switcher)
            if chat_switcher[0][0] == 1:
                db = sqlite3.connect('bot.db')
                cursor = db.cursor()
                query = f""" SELECT idaboutfriend from infoAboutFriend WHERE usersid = {message.from_user.id}"""
                cursor.execute(query)
                record = cursor.fetchall()
                query = f"""SELECT lang from infoAboutFriend WHERE usersid = {message.from_user.id}"""
                cursor.execute(query)
                source_lang = cursor.fetchall()
                query = f"""SELECT lang from infoAboutFriend WHERE usersid = {record[0][0]}"""
                cursor.execute(query)
                dist_lang = cursor.fetchall()
                db.commit()
                db.close()
                if not record:
                    bot.reply_to(message, 'you cant write because you are not here')
                else:
                    result = translator.translate_text(message.text, target_lang=dist_lang[0][0])
                    bot.send_message(record[0][0],
                                     str(result.text) + '\n  >>' + 'message from ' + message.from_user.username)
                print(message.text)




def addtobase(message):
    print(message.text + ' from ' + message.from_user.username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("My friend👥")
    button2 = types.KeyboardButton("My language📓")
    button3 = types.KeyboardButton("My ID🆔")
    button4 = types.KeyboardButton("Info➿")
    button5 = types.KeyboardButton("Chat☁️")
    markup.add(button1, button2, button3, button4, button5)

    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    query = f"""SELECT nickname from infoAboutFriend"""
    cursor.execute(query)
    record = list(chain.from_iterable(cursor.fetchall()))
    if message.text in record:
        query = f"""SELECT usersid from infoAboutFriend WHERE nickname = '{message.text}'"""
        cursor.execute(query)
        uselessId = cursor.fetchall()[0][0]
        query = f"""UPDATE infoAboutFriend SET idaboutfriend = {uselessId} WHERE usersid = {message.from_user.id}"""
        cursor.execute(query)
        bot.send_message(message.from_user.id, f'Okey, now yours friend is {message.text}', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Sorry, we are dont have this user:(', reply_markup=markup)
    db.commit()
    db.close()


def lang(message):
    l = "BG CS DA DE EL EN-GB EN-US ES ET FI FR HU IT JA LT LV NL PL PT-BR PT-PT RO RU SK SL SV TR UK ZH".split(' ')
    if message.text in l:
        db = sqlite3.connect('bot.db')
        cursor = db.cursor()
        query = f""" UPDATE infoAboutFriend SET lang = '{message.text}' WHERE usersid = {message.from_user.id}"""
        cursor.execute(query)
        db.commit()
        db.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("My friend👥")
        button2 = types.KeyboardButton("My language📓")
        button3 = types.KeyboardButton("My ID🆔")
        button4 = types.KeyboardButton("Info➿")
        button5 = types.KeyboardButton("Chat☁️")

        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, 'Understood, your language {lang}'.format(lang=message.text),
                         reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("My friend👥")
        button2 = types.KeyboardButton("My language📓")
        button3 = types.KeyboardButton("My ID🆔")
        button4 = types.KeyboardButton("Info➿")
        button5 = types.KeyboardButton("Chat☁️")

        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, 'Cant find your language, sorry'.format(lang=message.text),
                         reply_markup=markup)


# @bot.message_handler(func=lambda message: message.text[0] == '+')
# def pasteInBd(message):
# bot.reply_to(message, 'Okey, got you!')
# db = sqlite3.connect('bot.db')
# cursor = db.cursor()
# query = f"""SELECT usersid from infoAboutFriend"""
# cursor.execute(query)
# result = list(chain.from_iterable(cursor.fetchall()))
# if str(message.from_user.id) in result:
#    query = f""" UPDATE infoAboutFriend SET idaboutfriend = {message.text} WHERE usersid = {message.from_user.id}"""
#    cursor.execute(query)
# else:
#    query = f""" INSERT INTO infoAboutFriend (usersid, idaboutfriend) VALUES({message.from_user.id}, {message.text})"""
#    cursor.execute(query)
#    query = f"""UPDATE infoAboutFriend SET nickname = '{message.from_user.username}' WHERE usersid = '{message.from_user.id}'"""
#    cursor.execute(query)
# db.commit()
# db.close()


@bot.message_handler(commands=['writetoadminwithoutpermission'])
def adminheadoffice(message):
    send = bot.send_message(message.from_user.id, 'What do you want to write?')
    bot.register_next_step_handler(send, sendtoadmin)


def sendtoadmin(message):
    bot.send_message("1341584381", f"\n|||||{message.text} from {message.from_user.id} {message.from_user.username}")


bot.infinity_polling()
