import json
def video_load(message, response, success):
    with open('tiktok_data.json', 'a', encoding='utf8') as f:
        video_data = {'user': {'id': message.chat.id, 'name': message.from_user.first_name}, 'play': {'video': response['data']['hdplay'], 'audio': response['data']['music']}, 'success': success}
        f.write(json.dumps(video_data, ensure_ascii=False, indent=2) + '\n')

def new_user(message):
    import time
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    hours_minutes = time.strftime("%H:%M", local_time)
    with open('users_data.json', 'a', encoding='utf8') as f:
        user_data = {'name': message.from_user.first_name, 'id': message.from_user.id, 'time': hours_minutes}
        f.write(json.dumps(user_data, ensure_ascii=False, indent=2) + '\n')

def parrot(message, turn):
    with open('database.json', 'r', encoding='utf8') as f:
        try:
            data = json.load(f, ensure_ascii=False)
        except:
            data = {}
        if message.chat.id not in data:
            data[message.chat.id] = {}
            data[message.chat.id]['name'] = message.from_user.first_name
            data[message.chat.id]['parrot'] = {}
        data[message.chat.id]['parrot'] = turn
    with open('database.json', 'w', encoding='utf8') as f:
        print(data)
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_parrot(message):
    with open('database.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        if data[str(message.chat.id)]['parrot'] == True:
            return True
        else:
            return False