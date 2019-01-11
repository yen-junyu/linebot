from flask import Flask, request, abort
from dbmodel import MongoDB
import random
from googletrans import Translator

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,ImageMessage,ButtonsTemplate,TemplateSendMessage,MessageTemplateAction,TextSendMessage,ImageSendMessage,FollowEvent,UnfollowEvent
)

class Personal_setting():
	def __init__(self,id,status):
		self.user_id=id
		self.status=status
	def setStatus(s):
		self.status=s

def In_Usrlist(id):
	for person in user_id_list:
		if id==person.user_id:
			return person
		
def get_url():
	'''
	初始化url_list from db
	'''
	print('url')
	urls=url_collection.find()
	for url in urls:
		url_list.append(url)
def get_user():
	'''
	初始化user_id_list from db
	'''
	print('user')
	users=user_collection.find()
	
	for user in users:
		newone=Personal_setting(user['user_id'],user['status'])
		user_id_list.append(newone)


app = Flask(__name__)
translator = Translator()
line_bot_api = LineBotApi('sPTWas1Ym8raS3EBdO65u6ucGPITp0C8/PxXxDruSILb07Bf/fw9hGpgi/I4HEmii59OqKdR7f/e9g3dOqZD49a+kI20poHfIGbZmDk0hpx3eLJDblc197c1gygHSAdh5pK/Hm5wAN9GlGYR0qjTyAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38fe0a9dda346d346995cd62ecd6bda')

user_id_list=[]
url_list=[]
user_collection=MongoDB('mao','user_information')
url_collection=MongoDB('mao','mao_url')
get_url()
get_user()


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
'''
訊息事件
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	
	print("event.message.text:", event.message.text)
	print(len(user_id_list))
	
	profile = line_bot_api.get_profile(event.source.user_id)
	user=In_Usrlist(profile.user_id)
	
	'''
	print(profile.display_name)
	print(profile.user_id)
	print(profile.picture_url)
	print(profile.status_message)
	'''
	if user is None:
		profile = line_bot_api.get_profile(event.source.user_id)
		newone = Personal_setting(profile.user_id,"normal")
		print('user:'+str(len(user_id_list)))
		user_id_list.append(newone)	#加入新使用者
		print('user'+str(len(user_id_list)))
		user_collection.insert({"user_id":profile.user_id,"status":"normal"}) #把新使用者資料加入db
		content='不好意思 再試一次'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	
	message=event.message.text.split(' ')
	print(user.status)
	
	if user.status=="translator":
		content=translator.translate(event.message.text,dest='en').text
		user.status="normal"
		user_collection.update({"user_id":user.user_id},{"status":"normal"}) #更新資料庫status
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	
	if message[0]=="開始玩貓":
		Buttons_Template=TemplateSendMessage(
				alt_text='開始玩template',
				template=ButtonsTemplate(
					title='貓貓我會',
					text='選擇服務',
					thumbnail_image_url='https://i.imgur.com/PLpC073.png',
					actions=[
						MessageTemplateAction(
							label='賣萌',
							text='賣萌'
						),
						MessageTemplateAction(
							label='電影',
							text='電影'
						),
						MessageTemplateAction(
							label='翻譯貓''',
							text='翻譯'
						),
						MessageTemplateAction(
							label='給我建議',
							text='給我建議'
						)
					]
				)
			)
		line_bot_api.reply_message(event.reply_token, Buttons_Template)
		return 0
	elif message[0]=="賣萌":
		Buttons_Template=TemplateSendMessage(
				alt_text='開始玩template',
				template=ButtonsTemplate(
					title='你要貓貓',
					text='選擇服務',
					thumbnail_image_url=url_list[0]['url'],
					actions=[
						MessageTemplateAction(
							label='學貓叫',
							text='學貓叫'
						),
						MessageTemplateAction(
							label='貓咪照',
							text='貓咪照'
						),
						MessageTemplateAction(
							label='教我說話',
							text='教我說話'
						)
					]
				)
			)
		line_bot_api.reply_message(event.reply_token, Buttons_Template)
		return 0
	elif message[0]=="學貓叫":
		content='抱歉貓咪沙啞了QAQ\nhttps://google-translate-proxy.herokuapp.com/api/tts?query=我們一起學貓叫+一起喵喵描妙妙&language=zh-tw'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	elif message[0]=="貓咪照":
		url_object=random.choice(url_list)
		image_message = ImageSendMessage(
			original_content_url=url_object['url'],
			preview_image_url=url_object['url']
		)
		line_bot_api.reply_message(event.reply_token, image_message)
		return 0
		'''
		message={"type":"audio",
		"originalContentUrl": "https://google-translate-proxy.herokuapp.com/api/tts?query=%E6%88%91%E5%80%91%E4%B8%80%E8%B5%B7%E5%AD%B8%E8%B2%93%E5%8F%AB+%E4%B8%80%E8%B5%B7%E5%BB%9F%E7%9E%84%E5%96%B5%E5%96%B5%E5%96%B5&language=zh-tw",
		"duration": 60000}
		line_bot_api.reply_message(event.reply_token,message)
		return 0
		'''
	elif message[0]=="電影":
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text='還沒寫啦~'))
		pass
	elif message[0]=="翻譯":
		#目前翻譯暫定為中翻英文 還沒結合user_id的個人化
		content='來說吧!'
		#user.status="translator" #狀態變成翻譯
		user.setStatus("translator")
		user_collection.update({"user_id":user.user_id},{"status":"translator"}) #更新資料庫status
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		print(user.status)
		return 0
	elif message[0]=='裡面有誰':
		content=''
		for i in user_id_list:
			content+=i.user_id
			content+='\n'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
	elif message[0]=='離開':
		user_collection.remove({"user_id":profile.user_id})
		for i,o in enumerate(user_id_list):
			if o.user_id==profile.user_id:
				del user_id_list[i]
				break
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text='貓貓我不吵你了 掰掰'))
	elif message[0]=='喵喵傳話':
		if In_Usrlist(message[1]) is not None:
			line_bot_api.push_message(message[1],TextSendMessage(message[2]))
		else :
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text='找不到這個人欸?'))
	else :
		c=['挖聽無啦~','哩底嘞共蝦碗糕','你找碴484啦','蛤?','臭宅醒醒 去打code']
		content=random.choice(c)
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	
	
'''
圖像事件
'''
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event): 
    print(event.message.type)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@handler.add(FollowEvent)
def handle_event(event):
	profile = line_bot_api.get_profile(event.source.user_id)
	newone = Personal_setting(profile.user_id,"normal")
	user_id_list.append(newone)	#加入新使用者
	user_collection.insert({"user_id":profile.user_id,"status":"normal"}) #把新使用者資料加入db
	content='歡迎使用本貓\n輸入 開始玩貓 來使用本喵'
	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
	


if __name__ == "__main__":
	app.run(port=3000)
