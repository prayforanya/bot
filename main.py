from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink
import aiogram.utils.markdown as md



API_TOKEN = '5851915685:AAF4bEVJzjYQMVZaZID2qArLWk4imXb2gLw'
bot = Bot(token = API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dtext = {}
badpeople = {}
badwords = {}

class Form(StatesGroup):
    word = State() 
    


buttom1 = 'Плохие слова'
buttom2 = 'Нехороший человек'
buttom3 = 'Активный пользователь'
buttom4 = 'Самый активный'
buttom5 = 'Помоги мне!'
buttom6 = 'Очистить словарь плохих слов'
buttom7 = 'Очистить воспоминания о нехороших людях'
buttom8 = 'Я забываю всех активных'
buttom9 = 'Самая популярная запись'
buttom10 = 'Удалить плохое слово'

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.insert(buttom1).insert(buttom2).insert(buttom3).insert(buttom4).insert(buttom5).insert(buttom6).insert(buttom7).insert(buttom8).insert(buttom9).insert(buttom10)

@dp.message_handler(text='Самая популярная запись')
async def popular(message: types.Message):
    if message.chat.id not in dtext:
        await message.answer('Вам никто не отвечает на записи в канале')
    else:
        if len(dtext[message.chat.id])==0:
            await message.answer('Вам никто не отвечает на записи в канале')
        else:
            dd = {}
            for key in dtext[message.chat.id]:
                for it in dtext[message.chat.id][key]:
                    if key not in dd:
                        dd[key]=len(dtext[message.chat.id][key][it])
                    else:
                        dd[key]+=len(dtext[message.chat.id][key][it])
        
            g = sorted(dd.items(), key=lambda x: x[1], reverse = True)[0][0]
            await bot.send_message (chat_id=g.chat.id, text = 'Вот она!!!', reply_to_message_id=g.message_id)

@dp.message_handler(text='Я забываю всех активных')
async def cldtext(message: types.Message):
    if message.chat.id not in dtext:
         await message.answer('Теперь я больше не помню, кто когда комментировал записи Вашего канала')
    else:
        dtext[message.chat.id].clear()
        await message.answer('Теперь я больше не помню, кто когда комментировал записи Вашего канала')

@dp.message_handler(text='Очистить словарь плохих слов')
async def clbadwords(message: types.Message):
    if message.chat.id not in badwords:
        await message.answer('Я больше не знаю плохих слов, теперь Вам заново придется меня учить)')
    else:
        badwords[message.chat.id].clear()
        await message.answer('Я больше не знаю плохих слов, теперь Вам заново придется меня учить)')

@dp.message_handler(text='Очистить воспоминания о нехороших людях')
async def clbadpeople(message: types.Message): 
    if message.chat.id not in badpeople:
        await message.answer('Все подписчики Вашего канала снова хорошие')
    else:
        badpeople[message.chat.id].clear()
        await message.answer('Все подписчики Вашего канала снова хорошие')

@dp.message_handler(text='Помоги мне!')
async def helper(message: types.Message):
    await message.answer("Чем я могу Вам помочь: \n *Команда* _Плохие слова_ позволяет Вам написать слово, которое Вы не хотите видеть в комментариях от пользователей. Если пользователь использует это слово в своем комментарии под Вашим постом, то сообщение удаляется \n *Команда* _Самый активный_ выводит самого активного пользователя, т. е. того, кто чаще всех комментировал Ваши публицации \n *Команда* _Активный пользователь _ выводит username самого активного человека под публикацией, на которую вы ответители \n *Команда* _Нехороший человек_ выводит username человека, который чаще всех писал в комментарии слова, которые вы запретили командой плохие слова\n *Команда* _ Очистить воспоминания о нехороших людях_  удаляет записи всех тех, кто сквернословил \n *Команда* _ Очистить словарь плохих слов_  очищает словарь плохих слов \n *Команда* _Я забываю всех активных_ удаляет все записи о статистике активных пользователей канала \n *Команда* _Самая популярная запись_ Пересылает в чат самую популярную запись в канале \n *Команда* _Удалить плохое слово_ удаляет введенное Вами слово из словаря плохих слов",  parse_mode = "Markdown")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.answer("*Привет!* Я бот, который _собирает статистику_. \n Добавь меня в *обсуждение* своего канала и запусти там, и я тебе помогу(не забудь сделать меня админом в чате). \n Инструкцию по командам ты можешь найти, тыкнув на кнопку *Помоги мне!*.", parse_mode = "Markdown", reply_markup = greet_kb)

class Form2(StatesGroup):
    word2 = State() 

@dp.message_handler(text='Удалить плохое слово')
async def words(message: types.Message):
    await Form2.word2.set()
    await message.reply("Введи слово, которое хочешь удалить")

@dp.message_handler(state=Form2.word2)
async def wordsname(message: types.Message, state: FSMContext):
    if message.chat.id not in badwords:
        await message.reply('Я не знаю плохих слов')
        await state.finish()
    else:
        if message.text.lower() not in badwords[message.chat.id]:
            await message.reply("Извините но вы не добавляли это слово. Вот слова, которые Вы добавляли, выберите что-то из них и еще раз вызовите команду *Удалить плохое слово*")
            slovarik =''
            for i in range (len(badwords[message.chat.id])):
                slovarik+=badwords[message.chat.id][i]+' '
            await message.answer(slovarik)
            await state.finish()
        else:
            badwords[message.chat.id].remove(message.text.lower())
            await message.answer('_Cлово_ '+message.text.lower()+' _успешно удалено!_ \n Сейчас выведу *слова* через пробел, которые Вы не хотите видеть в комментариях к записям :)', parse_mode = "Markdown")
            slovarik =''
            if len(badwords[message.chat.id])!=0:
                for i in range (len(badwords[message.chat.id])):
                    slovarik+=badwords[message.chat.id][i]+' '
                await message.answer(slovarik)
                await state.finish()
            else:
                await message.answer('Я больше не знаю плохих слов, теперь Вам заново придется меня учить)')
                await state.finish()

@dp.message_handler(text='Плохие слова')
async def words(message: types.Message):
    await Form.word.set()
    await message.reply("Введите слово, которое не хочешь видеть в канале")
    
@dp.message_handler(state=Form.word)
async def process_name(message: types.Message, state: FSMContext):
    f = message.text.split()
    if f[0] == message.text:
        if message.chat.id not in badwords:
            badwords[message.chat.id] = [message.text.lower()]
            await message.answer('_Cлово_ '+message.text.lower()+' _успешно добавлено!_ \n Сейчас выведу *слова* через пробел, которые Вы уже добавили :)', parse_mode = "Markdown")
            slovarik =''
            for i in badwords[message.chat.id]:
                slovarik+=i+' '
            await message.answer(slovarik)
            await state.finish()
        else:
            if message.text.lower() not in badwords[message.chat.id]:
                badwords[message.chat.id].append(message.text.lower())
                await message.answer('_Cлово_ '+message.text.lower()+' _успешно добавлено!_ \n Сейчас выведу *слова* через пробел, которые Вы уже добавили :)', parse_mode = "Markdown")
                slovarik =''
                for i in badwords[message.chat.id]:
                    slovarik+=i+' '
                await message.answer(slovarik)
                await state.finish()
            else:
                await message.answer('Слово, которое Вы написали уже есть в словаре \n Сейчас выведу *слова* через пробел, которые Вы уже добавили :)', parse_mode = "Markdown")
                slovarik =''
                for i in badwords[message.chat.id]:
                    slovarik+=i+' '
                await message.answer(slovarik)
                await state.finish()

    else:
        await message.answer('Вы ввели не одно слово, введите только одно слово еще раз!')
   
            
        

@dp.message_handler(text='Нехороший человек')
async def send_welcome(message: types.Message):
    if message.chat.id not in badpeople:
        await message.answer('Плохих людей нет')
    else:
        if len(badpeople[message.chat.id])==0:
            await message.answer('Плохих людей нет')
        else:
            g = badpeople[message.chat.id]
            bhelp = sorted (g.items(), key=lambda x: x[1], reverse = True)[0][0]
            await message.answer('@'+bhelp)

@dp.message_handler(text='Самый активный')
async def send_welcome(message: types.Message):
    dhelp = {}
    if message.chat.id not in dtext:
        await message.answer('Активных нет')
    else:
        for key in dtext[message.chat.id]:
            for user in dtext[message.chat.id][key]:
                if user not in dhelp:
                    dhelp[user] = len(dtext[message.chat.id][key][user])
                else:
                    dhelp[user] += len(dtext[message.chat.id][key][user])
        if len(dhelp)==0:
            await message.answer('Активных нет')
        else:
            help = sorted(dhelp.items(), key = lambda x: x[1], reverse = True)[0][0]
            await message.answer('@'+help)

class Form1(StatesGroup):
    word1 = State() 
    
@dp.message_handler(text='Активный пользователь')
async def active(message: types.Message):
    await Form1.word1.set()
    await message.reply("Перешлите сообщение, для которого хотите проверить статистику")

@dp.message_handler(state=Form1.word1)
async def active2(message: types.Message, state: FSMContext):
    if message.chat.id not in dtext:
        await message.answer('Активных пользователей нет')
        await state.finish()
    else:    
        if message.reply_to_message not in dtext[message.chat.id ]:
            await message.answer('Активных пользователей нет')
            await state.finish()
        else:
            f = dtext[message.chat.id][message.reply_to_message]
            g = sorted(f.items(), key=lambda x: len(x[1]), reverse = True)[0][0]
            await message.answer('@'+g)
            await state.finish()


@dp.message_handler()
async def schet(message: types.Message):
    f = 0
    str = message.text.lower()
    newstr = str.split()
    if message.chat.id in badwords:
        for w in badwords[message.chat.id]:
            if w in newstr:
                
                if message.chat.id not in badpeople:
                    badpeople[message.chat.id] = {message.from_user.username : 1}

                else:
                    if message.from_user.username not in badpeople[message.chat.id]:
                        badpeople[message.chat.id][message.from_user.username] = 1
                    else:
                        badpeople[message.chat.id][message.from_user.username]+=1
                if message.reply_to_message:
                    f = 1
                    await bot.delete_message(message.chat.id, message.message_id)
                    break

    if message.reply_to_message and f == 0:
        if message.chat.id not in dtext:
            dtext[message.chat.id] = {message.reply_to_message : {message.from_user.username : [message.text]}}
        else:
            if message.reply_to_message not in dtext[message.chat.id]:
                dtext[message.chat.id][message.reply_to_message] = {message.from_user.username : [message.text]}
            else:
                if message.from_user.username not in dtext[message.chat.id][message.reply_to_message]:
                    dtext[message.chat.id][message.reply_to_message][message.from_user.username] = [message.text]
                else:
                    dtext[message.chat.id][message.reply_to_message][message.from_user.username].append(message.text)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
