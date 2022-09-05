import os
import configparser

try:
    from telethon import TelegramClient, events

except ModuleNotFoundError:
    os.system("pip install telethon==1.24.0")
    from telethon import TelegramClient, events

print("\nThis program is used to scrape message from different telegram channel/group, and send to your private channel/group.")

def parse_api():
	
	#Read the hash from "api.ini" file
	config_parser = configparser.ConfigParser()
	read_config = config_parser.read("api.ini")
	if not read_config:
		#Write api id and hash in the api.ini file if not found
		print("If you do not have api id and api hash, please get them from https://my.telegram.org/")
		write_config = configparser.ConfigParser()
		config_parser.add_section("API_CONFIG")
		api_id = input("Enter api id:")
		api_hash = input("Enter api hash:")
		
		config_parser.set("API_CONFIG","api_id",api_id.strip())
		config_parser.set("API_CONFIG","api_hash",api_hash.strip())
		with open('api.ini', 'w') as api:
			config_parser.write(api)

	else:
		# Read hash files if alread exist
		config_parser.read("api.ini")
		api_id = config_parser.get("API_CONFIG", "api_id")
		api_hash = config_parser.get("API_CONFIG", "api_hash")
  
	return api_id, api_hash

def GetPostLink(channel_id, message_id):
    PostLink = f"\nMain Link:https://t.me/c/{channel_id}/{message_id}"

    return PostLink

print("\n       BOT STARTED! Ctl+C to STOP the Program\n")

#Parse and obtaining api id from parse_api method
api_id, api_hash = parse_api()


#Get list of groups
ChatID_AllMsg = []
with open("AllMessage/ChatID_AllMsg.txt") as tg:
    while (line := tg.readline().rstrip()):
        ChatID_AllMsg.append(int(line))

ChatID_PinMsg = []
with open("PinMessage/ChatID_PinMsg.txt") as tg:
    while (line := tg.readline().rstrip()):
        ChatID_PinMsg.append(int(line))

AllMsg_ChatTitles = []
with open("AllMessage/AllMsg_ChatTitles.txt") as tg:
    while (line := tg.readline().rstrip()):
        AllMsg_ChatTitles.append(line)

PinMsg_ChatTitles = []
with open("PinMessage/PinMsg_ChatTitles.txt") as tg:
    while (line := tg.readline().rstrip()):
        PinMsg_ChatTitles.append(line)

print(f"ChatID_AllMsg: {ChatID_AllMsg}")
print(f"ChatID_PinMsg: {ChatID_PinMsg}")
print(f"AllMsg_ChatTitles: {AllMsg_ChatTitles}")
print(f"PinMsg_ChatTitles: {PinMsg_ChatTitles}\n")

def get_title(channel_id):
    index = ChatID_AllMsg.index(int('-100' + str(channel_id)))

    return index

# the tg client started and sending api request to telegram.org
client = TelegramClient('TelegramToTelegram', api_id.strip(), api_hash.strip()).start()

# async method to get new messages
async def get_message():
        #Get incoming message from specific group this can send docs and img too. Use https://t.me/getidsbot to get ID and paste it inside ChatID_AllMsg.txt


        @client.on(events.NewMessage(chats=ChatID_AllMsg))
        async def handle_incoming(event1):
            channel_id, message_id = event1.message.peer_id.channel_id, event1.id
            event_message = event1.message
            event_message.message = event_message.message + f"\n\n\n{AllMsg_ChatTitles[get_title(channel_id)]}: {GetPostLink(channel_id, message_id)}"
            print(f"\n{event_message}")
            await client.send_message(
                'https://t.me/cryptetete',
                event_message,
                link_preview=False
            )

        #Get incoming pinned message from specific group this can send docs and img too. Use https://t.me/getidsbot to get ID and paste it inside ChatID_PinMsg.txt
        @client.on(events.ChatAction(chats=ChatID_PinMsg))
        async def handle_pinned_msg(event):
            if event.new_pin == True:
                pinned_message = await event.get_pinned_message()
                channel_id, message_id = pinned_message.peer_id.channel_id, pinned_message.id
                pinned_message.message = pinned_message.message + f"\n\n\{PinMsg_ChatTitles[get_title(channel_id)]}: {GetPostLink(channel_id, message_id)}"
                print(f"\n{pinned_message}")
                await client.send_message(
                    'https://t.me/cryptetete',
                    pinned_message,
                    link_preview=False
                )
	
# run the client loop until disconnected
with client:
	client.loop.run_until_complete(get_message())
	client.run_until_disconnected()