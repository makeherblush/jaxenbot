import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = '8807715605:AAGAzrsJzWDGKwVy2Ri8MiV4fkbP-8ydHgA' 
ADMIN_GROUP_ID = '-5465430711' 

bot = telebot.TeleBot(TOKEN)
user_state = {} 


@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    btn1 = InlineKeyboardButton("📩 Kirim Laporan", callback_data="laporan")
    btn2 = InlineKeyboardButton("📝 Kritik & Saran", callback_data="saran")
    btn3 = InlineKeyboardButton("👥 List Admin", callback_data="admin")
    btn4 = InlineKeyboardButton("📜 Rules & Info", callback_data="rules")
    markup.add(btn1, btn2, btn3, btn4)

    
    teks = """*Selamat datang di Bot Pelayanan Thunder Crew ⚡*

Halo! Tempat ini dibuat khusus sebagai wadah komunikasi privat antara lu dan para admin. Punya keluhan, laporan, atau ide segar buat *circle* kita? Tumpahin semuanya di sini.

Silakan pilih menu di bawah ini buat mulai:"""

    bot.send_message(message.chat.id, teks, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "laporan":
        bot.send_message(chat_id, "Silakan ketik laporan lu sekarang. Laporan akan dikirim ke admin secara anonim (hanya isi pesan).\n\n_Ketik /cancel jika ingin membatalkan._", parse_mode='Markdown')
        user_state[chat_id] = 'laporan' # Menyimpan status user
        
    elif call.data == "saran":
        bot.send_message(chat_id, "Punya ide atau masukan buat Thunder Crew? Tulis di sini ya!\n\n_Ketik /cancel jika ingin membatalkan._", parse_mode='Markdown')
        user_state[chat_id] = 'saran'
        
    elif call.data == "admin":
        teks_admin = """👥 *List Admin Thunder Crew:*
1. jegrav (@grzdrious)
2. jevalric (@jxvaltherion)
3. bara (@bisikbar)
4. sagara (@sagarajabr)
5. nakula (@lel4kimahal)
6. juan (@iPecandhol)
7. fafa (@Jacnthef4)
8. zhain

_Silakan hubungi admin yang sedang aktif kalau ada urusan darurat!_"""
        bot.send_message(chat_id, teks_admin, parse_mode='Markdown')
        
    elif call.data == "rules":
        teks_rules = """📜 *RULES & INFO THUNDER CREW* ⚡

_Mixed edition. Pastiin lo bukan akun pers/rl._

Nih, sebelum join inget ya:
• GC ini *ONLY RP*. Bukan pers, bukan RL juga.
• Dilarang keras bahas atau kirim hal yang berbau RL atau semacamnya.
• Kaga nerima numpang nama.
• Anti CDC.
• **WAJIB** join CH.

📢 *CH:* @ChThunderCrew"""
        bot.send_message(chat_id, teks_rules, parse_mode='Markdown')

@bot.message_handler(commands=['cancel'])
def cancel_action(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]
    bot.send_message(chat_id, "Aksi dibatalkan. Ketik /start untuk kembali ke menu utama.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    
    if chat_id in user_state:
        state = user_state[chat_id]
        
        
        pengirim = message.from_user.username or message.from_user.first_name
        
        if state == 'laporan':
            pesan_ke_admin = f"🚨 *LAPORAN BARU MASUK* 🚨\nDari: @{pengirim}\n\n*Isi Laporan:*\n{message.text}"
            bot.send_message(ADMIN_GROUP_ID, pesan_ke_admin, parse_mode='Markdown')
            bot.send_message(chat_id, "✅ Laporan lu udah berhasil dikirim dan masuk ke radar admin. Thank you!")
            
        elif state == 'saran':
            pesan_ke_admin = f"💡 *KRITIK & SARAN BARU* 💡\nDari: @{pengirim}\n\n*Isi Saran:*\n{message.text}"
            bot.send_message(ADMIN_GROUP_ID, pesan_ke_admin, parse_mode='Markdown')
            bot.send_message(chat_id, "✅ Masukan lu udah terkirim ke ruang admin. Thank you atas idenya!")
            
        
        del user_state[chat_id]
    else:
        
        bot.send_message(chat_id, "Gua gak ngerti maksud lu. Ketik /start buat memunculkan menu ya.")


print("Bot Thunder Crew sedang menyala...")
bot.polling(none_stop=True)