from bit import Key
from multiprocessing import Pool, cpu_count
import telebot

bot = telebot.TeleBot("7511543104:AAGUYN_RGyEN4sIbOGqyYYXvwAU3Dge6_PY")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    result = find_private_key(user_message)
    if result:
        bot.reply_to(message, f"Private Key Found: {result[0]}\nAddress: {result[1]}")

def process_input(input_string):
    start, stop, address = input_string.split(':')
    return start.zfill(64), stop.zfill(64), address

def process_private_key(priv_key_int):
    priv_key_bytes = priv_key_int.to_bytes(32, byteorder='big')
    key = Key.from_bytes(priv_key_bytes)
    return priv_key_bytes.hex(), key.address

def search_for_target_address(start_key_hex, stop_key_hex, target_address):
    start_key = int(start_key_hex, 16)
    stop_key = int(stop_key_hex, 16)
    num_cores = cpu_count()

    with Pool(num_cores) as pool:
        for priv_key_hex, address in pool.imap(process_private_key, range(start_key, stop_key + 1), chunksize=1000):
            if address == target_address:
                return priv_key_hex, address
    return None, None

def find_private_key(input_string):
    start_key, stop_key, address = process_input(input_string)
    found_key, found_address = search_for_target_address(start_key, stop_key, address)
    return found_key, found_address if found_key else None

bot.polling()
