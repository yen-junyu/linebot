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
    MessageEvent, TextMessage,ImageMessage,ButtonsTemplate,TemplateSendMessage,MessageTemplateAction,TextSendMessage,ImageSendMessage,FollowEvent
)

app = Flask(__name__)
translator = Translator()
line_bot_api = LineBotApi('sPTWas1Ym8raS3EBdO65u6ucGPITp0C8/PxXxDruSILb07Bf/fw9hGpgi/I4HEmii59OqKdR7f/e9g3dOqZD49a+kI20poHfIGbZmDk0hpx3eLJDblc197c1gygHSAdh5pK/Hm5wAN9GlGYR0qjTyAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38fe0a9dda346d346995cd62ecd6bda')

user_id_list=[]
url_list=[]
user_collection=MongoDB('mao','user_information')
url_collection=MongoDB('mao','mao_url')

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
	print("event.reply_token:", event.reply_token)
	print("event.message.text:", event.message.text)
	
	profile = line_bot_api.get_profile(event.source.user_id)
	user=In_Usrlist(profile.user_id)
	'''
	print(profile.display_name)
	print(profile.user_id)
	print(profile.picture_url)
	print(profile.status_message)
	'''

	if user is None:
		content='再加一次好友'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	

	if user.status=="translator":
		content=translator.translate(event.message.text,dest='en').text
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		user.status="normal"
		user_collection.update({"user_id":user.user_id},{"status":"normal"}) #更新資料庫status
		return 0
	

	if event.message.text=="開始玩貓":
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
	elif event.message.text=="賣萌":
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
	elif event.message.text=="學貓叫":
		content='抱歉貓咪沙啞了QAQ\nhttps://google-translate-proxy.herokuapp.com/api/tts?query=我們一起學貓叫+一起喵喵描妙妙&language=zh-tw'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		return 0
	elif event.message.text=="貓咪照":
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
	elif event.message.text=="翻譯":
		#目前翻譯暫定為中翻英文 還沒結合user_id的個人化
		content='來說吧!'
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
		user.status="translator" #狀態變成翻譯
		user_collection.update({"user_id":user.user_id},{"status":"translator"}) #更新資料庫status
		return 0
	elif event.message.text=="電影":
		pass

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
	content='歡迎使用本貓\n輸入 開始玩貓 來使用本喵'
	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
	profile = line_bot_api.get_profile(event.source.user_id)
	newone = Personal_setting(profile.user_id,"normal")

	user_id_list.append(newone)	#加入新使用者
	user_collection.insert({"user_id":profile.user_id,"status":"normal"}) #把新使用者資料加入db
	
class Personal_setting():
	def __init__(self,id,status):
		self.user_id=id
		self.status=status

def In_Usrlist(id):
	for person in user_id_list:
		if id==person.user_id:
			return person
		
def get_url():
	'''
	初始化url_list from db
	'''
	urls=url_collection.find()
	for url in urls:
		url_list.append(url)
def get_user():
	'''
	初始化user_id_list from db
	'''
	users=user_collection.find()
	for user in users:
		newone=Personal_setting(user['user_id'],user['status'])
		user_id_list.append(newone)
	
if __name__ == "__main__":
	get_url()
	get_user()
	app.run(ssl_context='adhoc',port=3000)
