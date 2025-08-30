import os
import json
import telebot
from telebot import types

class TelegramBot:
    def __init__(self):
        self.secrets_file = "secrets.json"
        self.config = self.load_or_create_config()
        
        # בדיקה אם כל הפרטים הנדרשים קיימים
        if not all([self.config.get('bot_token'), self.config.get('user_id'), self.config.get('group_id')]):
            print("חסרים פרטים בהתקנה. מתחיל תהליך הגדרה...")
            self.setup_config()
        else:
            print("מצאתי פרטים שמורים. מפעיל את הבוט...")
            self.initialize_bot()
    
    def load_or_create_config(self):
        if os.path.exists(self.secrets_file):
            try:
                with open(self.secrets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"שגיאה בקריאת קובץ ההגדרות: {e}")
                return {'bot_token': '', 'user_id': '', 'group_id': ''}
        return {'bot_token': '', 'user_id': '', 'group_id': ''}
    
    def save_config(self):
        try:
            with open(self.secrets_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print("הפרטים נשמרו בהצלחה!")
        except Exception as e:
            print(f"שגיאה בשמירת הקובץ: {e}")
    
    def setup_config(self):
        print("=== התקנה ראשונית ===")
        print("נדרשים פרטים להתחברות לבוט Telegram")
        
        self.config['bot_token'] = input("הזן את טוקן הבוט: ").strip()
        self.config['user_id'] = input("הזן את ה-user ID שלך: ").strip()
        self.config['group_id'] = input("הזן את ה-group ID: ").strip()
        
        self.save_config()
        self.initialize_bot()
    
    def initialize_bot(self):
        try:
            self.bot = telebot.TeleBot(self.config['bot_token'])
            
            @self.bot.message_handler(commands=['start'])
            def handle_start(message):
                try:
                    # שליחת התמונה
                    image_path = r"C:\Users\Admin\Desktop\robotush\BOT\Pic\000.JPG"
                    
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as photo:
                            self.bot.send_photo(message.chat.id, photo, 
                                              caption="ברוכים הבאים לאפליקציה שתסייע לכם לעשות כסף דרך הטלגרם!\nלהמשך לחץ:",
                                              reply_markup=self.create_continue_button())
                        print("נשלחה תמונה עם כפתור המשך")
                    else:
                        # אם התמונה לא קיימת - שולחים הודעה רגילה עם כפתור
                        self.bot.send_message(message.chat.id, 
                                            "ברוכים הבאים לאפליקציה שתסייע לכם לעשות כסף דרך הטלגרם!\nלהמשך לחץ:",
                                            reply_markup=self.create_continue_button())
                        print("התמונה לא נמצאה. נשלחה הודעה עם כפתור המשך")
                        
                except Exception as e:
                    print(f"שגיאה בשליחת התמונה: {e}")
                    # גיבוי במקרה של שגיאה
                    self.bot.send_message(message.chat.id, 
                                        "ברוכים הבאים לאפליקציה שתסייע לכם לעשות כסף דרך הטלגרם!\nלהמשך לחץ:",
                                        reply_markup=self.create_continue_button())
            
            # טיפול בלחיצה על כפתור "המשך"
            @self.bot.callback_query_handler(func=lambda call: call.data == 'continue')
            def handle_continue(call):
                try:
                    self.bot.answer_callback_query(call.id)
                    self.bot.send_message(call.message.chat.id, "בקרוב\nוזה יהיה השלב הבא שלנו")
                    print("משתמש לחץ על כפתור 'המשך'")
                except Exception as e:
                    print(f"שגיאה בשליחת הודעת 'בקרוב': {e}")
            
            print("הבוט מופעל ומקשיב להודעות...")
            print("שלח /start לבוט כדי להתחיל")
            self.bot.polling(none_stop=True)
            
        except Exception as e:
            print(f"שגיאה בהפעלת הבוט: {e}")
            print("ייתכן שהטוקן לא תקין. נסה שוב.")
            # איפוס הטוקן כדי לאפשר הזנה מחדש
            self.config['bot_token'] = ''
            self.save_config()
            self.setup_config()
    
    def create_continue_button(self):
        markup = types.InlineKeyboardMarkup()
        continue_button = types.InlineKeyboardButton("המשך", callback_data='continue')
        markup.add(continue_button)
        return markup

if __name__ == "__main__":
    bot = TelegramBot()
    input("לחץ Enter כדי לסיים...")