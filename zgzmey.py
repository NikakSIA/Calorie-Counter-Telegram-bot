import json
import telebot
from telebot import types

#Класс для описания еды
class Food:

    def __init__(self, name, calories, proteins, fats, carbohydrates):
        self.name = name
        self.calories = int(calories)
        self.proteins = int(proteins)
        self.fats = int(fats)
        self.carbohydrates = int(carbohydrates)
    
    def clear(self):
        self.calories = 0
        self.proteins = 0
        self.fats = 0
        self.carbohydrates = 0

    def __str__(self):
        return  f"{self.calories} {self.proteins} {self.fats} {self.carbohydrates}"

#Функция создания Reply клавиатуры
def make_reply_keyboard(*bttns):
    bttns = list(bttns)
    for bttn in bttns:
        if isinstance(bttn, list):
            bttns.remove(bttn)
            bttns += bttn
    global keyboardr
    keyboardr = types.ReplyKeyboardMarkup(row_width=3)
    for bttn in bttns:
        button = types.KeyboardButton(str(bttn))
        keyboardr.add(button)

#Функция создания Inline клавиатуры
def make_inline_keyboard(**bttns):
    global keyboardi
    keyboardi = types.InlineKeyboardMarkup()
    for cd, text in bttns.items():
        button = types.InlineKeyboardButton(text=text, callback_data=cd)
        keyboardi.add(button)

#Глобальные переменные    
username = ""
basic_buttons = ["Съесть что-нибудь", "Добавить шаблон", "Ввести норму потребления", "Вывести съеденное за день"]
standart = Food("норма", 2000, 170, 60, 200)
templates = []
keyboardr = 0
keyboardi = 0
log_in_flag = False
register_flag = False
write_food = False
write_standard = False
write_weight = False
write_without_template = False
reset = False
delete_template = False
save_data_flag = False
product = Food("еде", 0, 0, 0, 0)
eaten = Food("съеденное", 0, 0, 0, 0)
with open("kbju_fans.json", encoding="UTF-8") as file_in:
    json_data = json.load(file_in)

bot = telebot.TeleBot('Вставьте свой код для телеграм бота от BotFather')

#Ну старт, первое сообщение и его логика
@bot.message_handler(commands = ['start'])
def start(message):
    global write_food, write_standard, standart, templates, eaten, product, write_weight, reset, delete_template, username, log_in_flag, register_flag, save_data_flag, write_without_template
    log_in_flag = False
    register_flag = False
    write_food = False
    write_standard = False
    write_weight = False
    write_without_template = False
    reset = False
    delete_template = False
    save_data_flag = False
    username = ""
    standart = Food("норма", 2000, 170, 60, 200)
    templates = []
    product = Food("еде", 0, 0, 0, 0)
    eaten = Food("съеденное", 0, 0, 0, 0)
    make_reply_keyboard("Войти", "Зарегистрироваться")
    bot.reply_to(message, 'Привет! Нажми "Зарегистрироваться", чтобы создать аккаунт, или "Войти", чтобы зайти в уже существующий.', reply_markup=keyboardr)

#Обработка данных с Inline клавиатуры
@bot.callback_query_handler()
def inline_output(call):
    global write_food
    if call.data == "make_template":
        bot.send_message(call.message.chat.id, "Напиши назание продукта. \nЗатем введи через пробел по порядку содержание в продукте калорий, белков, жиров и углеводов на 100 грамм. \nПример: Куриное филе 200 30 8 0")
        write_food = True

#Обработка текста
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global keyboardr, keyboardi, write_food, write_standard, standart, templates, eaten, product, write_weight, reset, delete_template, username, log_in_flag, register_flag, json_data, save_data_flag, write_without_template, basic_buttons
    
    
    #Очистка данных о съеденном
    if reset:
        eaten.clear()
        reset = False
    
    
    #Логика кнопки "Войти"
    if message.text == "Войти":
        log_in_flag = True
        keyboardr = types.ReplyKeyboardRemove()
        bot.reply_to(message, "Теперь введи имя", reply_markup=keyboardr)
    elif log_in_flag:
        if message.text in json_data.keys():
            username = message.text
            templates = []
            for data in json_data[username]["templates"]:
                name = ''.join([c for c in data if c.isalpha() or c == " "]).strip()
                nums = [int(float(i)) for i in ''.join([c for c in data if c.isdigit() or c == " "]).split()]
                templates.append(Food(name, nums[0], nums[1], nums[2], nums[3]))
            eaten = Food("съеденное", int(float(json_data[username]["eaten"].split()[0])), int(float(json_data[username]["eaten"].split()[1])), int(float(json_data[username]["eaten"].split()[2])), int(float(json_data[username]["eaten"].split()[3])))
            standart = Food("норма", int(float(json_data[username]["standart"].split()[0])), int(float(json_data[username]["standart"].split()[1])), int(float(json_data[username]["standart"].split()[2])), int(float(json_data[username]["standart"].split()[3])))
            save_data_flag = True
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)
        else:
            make_reply_keyboard("Войти", "Зарегистрироваться")
            bot.reply_to(message, "Аккаунт не найден!", reply_markup=keyboardr)
        log_in_flag = False
    
    
    #Логика кнопки "Зарегистрироваться"
    elif message.text == "Зарегистрироваться":
        keyboardr = types.ReplyKeyboardRemove()
        register_flag = True
        bot.reply_to(message, "Теперь введи имя", reply_markup=keyboardr)
    elif register_flag:
        if message.text not in json_data.keys():
            username = message.text
            json_data[username] = {"templates": [], "eaten": "0 0 0 0", "standart": "0 0 0 0"}
            templates = []
            for data in json_data[username]["templates"]:
                name = ''.join([c for c in data if c.isalpha() or c == " "]).strip()
                nums = [int(float(i)) for i in ''.join([c for c in data if c.isdigit() or c == " "]).split()]
                templates.append(Food(name, nums[0], nums[1], nums[2], nums[3]))
            eaten = Food("съеденное", int(float(json_data[username]["eaten"].split()[0])), int(float(json_data[username]["eaten"].split()[1])), int(float(json_data[username]["eaten"].split()[2])), int(float(json_data[username]["eaten"].split()[3])))
            standart = Food("норма", int(float(json_data[username]["standart"].split()[0])), int(float(json_data[username]["standart"].split()[1])), int(float(json_data[username]["standart"].split()[2])), int(float(json_data[username]["standart"].split()[3])))
            save_data_flag = True
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)
        else:
            make_reply_keyboard("Войти", "Зарегистрироваться")
            bot.reply_to(message, "Аккаунт с таким именем уже существует!", reply_markup=keyboardr)
        register_flag = False
    
    
    #Логика кнопки "Съесть что-нибудь"
    elif message.text == "Съесть что-нибудь":        
        make_reply_keyboard(sorted([i.name for i in templates]), "Ввести без шаблона", "Назад", "Удалить шаблон")
        bot.reply_to(message, "Выберите шаблон", reply_markup=keyboardr)
    elif message.text in [i.name for i in templates] and not delete_template:
        product = [i for i in templates if i.name == message.text][0]
        write_weight = True
        keyboardr = types.ReplyKeyboardRemove()
        bot.reply_to(message, "Отлично! Теперь введи массу продукта в граммах", reply_markup=keyboardr)
    elif write_weight:
        try:
            k = round(int(message.text) / 100, 2)
        except Exception:
            bot.reply_to(message, "Данные введены неверно! Попробуй ещё раз!")
        else:
            eaten.calories += product.calories * k
            eaten.proteins += product.proteins * k
            eaten.fats += product.fats * k
            eaten.carbohydrates += product.carbohydrates * k
            write_weight = False
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)
    elif message.text == "Ввести без шаблона":
        write_without_template = True
        keyboardr = types.ReplyKeyboardRemove()
        bot.reply_to(message, "Введи через пробел по порядку потребленные калории, белки, жиры и углеводы. \nПример: 200 30 8 0", reply_markup=keyboardr)
    elif write_without_template:
        try:
            nums = [int(i) for i in message.text.split()]
            eaten.calories += nums[0]
            eaten.proteins += nums[1]
            eaten.fats += nums[2]
            eaten.carbohydrates += nums[3]
        except Exception:
            bot.reply_to(message, "Данные введены неверно! Попробуй ещё раз!")
        else:
            write_without_template = False
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)


    #Логика кнопки "Добавить шаблон"
    elif message.text == "Добавить шаблон":
        keyboardr = types.ReplyKeyboardRemove()
        bot.reply_to(message, 'Напиши назание продукта. \nЗатем введи через пробел по порядку содержание в продукте калорий, белков, жиров и углеводов на 100 грамм. \nПример: Куриное филе 200 30 8 0', reply_markup=keyboardr)
        write_food = True
    elif write_food:
        try:
            name = ''.join([c for c in message.text if c.isalpha() or c == " "]).strip()
            nums = [int(i) for i in ''.join([c for c in message.text if c.isdigit() or c == " "]).split()]
            templates.append(Food(name, nums[0], nums[1], nums[2], nums[3]))
        except Exception:
            bot.reply_to(message, "Данные введены неверно! Попробуй ещё раз!")
        else:
            write_food = False
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)
    
    
    #Логика кнопки "Ввести норму потребления"
    elif message.text == "Ввести норму потребления":
        keyboardr = types.ReplyKeyboardRemove()
        bot.reply_to(message, "Введи желаемое потребление КБЖУ за день. \nПример: 2400 170 60 250", reply_markup=keyboardr)
        write_standard = True
    elif write_standard:
        try:
            nums = [int(i) for i in message.text.split()]
            standart = Food("норма", nums[0], nums[1], nums[2], nums[3])
        except Exception:
            bot.reply_to(message, "Данные введены неверно! Попробуй ещё раз!")
        else:
            write_standard = False
            make_reply_keyboard(basic_buttons)
            bot.reply_to(message, "Данные сохранены!", reply_markup=keyboardr)
    
    
    #Логика кнопки "Вывести съеденное за день"
    elif message.text == "Вывести съеденное за день":
        make_reply_keyboard("Назад", "Очистить данные о съеденном", "Вывести данные о съеденном")
        bot.reply_to(message, "Выбери один из вариантов", reply_markup=keyboardr)
    elif message.text == "Очистить данные о съеденном":    
        reset = True
        make_reply_keyboard(basic_buttons)
        bot.reply_to(message, "Данные очищены!", reply_markup=keyboardr)
    elif message.text == "Вывести данные о съеденном":    
        make_reply_keyboard(basic_buttons)
        bot.reply_to(message, f"Сегодня ты съел {eaten.calories}/{standart.calories} калорий, {eaten.proteins}/{standart.proteins} белков, {eaten.fats}/{standart.fats} жиров и {eaten.carbohydrates}/{standart.carbohydrates} углеводов")


    #Логика кнопки "Назад"
    elif message.text == "Назад":
        make_reply_keyboard(basic_buttons)
        bot.reply_to(message, 'Главное меню', reply_markup=keyboardr)
    
    
    #Логика кнопки "Удалить шаблон"
    elif message.text == "Удалить шаблон":
        make_reply_keyboard([i.name for i in templates], "Назад")
        delete_template = True
        bot.reply_to(message, "Выбери шаблон", reply_markup=keyboardr)
    elif delete_template:
        templates.remove([i for i in templates if i.name == message.text][0])
        make_reply_keyboard(basic_buttons)
        delete_template = False
        bot.reply_to(message, "Шаблон удален!", reply_markup=keyboardr)
    
    
    #Запись данных в json файл
    if save_data_flag:
        json_data[username]["templates"] = sorted([f"{i.name} {str(i)}" for i in templates])
        json_data[username]["eaten"] = str(eaten)
        json_data[username]["standart"] = str(standart)
        with open("kbju_fans.json", "w", encoding="UTF-8") as file_out:
            json.dump(json_data, file_out, ensure_ascii=False, indent=4)

#((((3!)^(3!))!)^(3!))! This is very important

bot.polling(none_stop = True)
