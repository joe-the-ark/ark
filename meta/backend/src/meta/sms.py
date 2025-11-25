import requests, json

def send_sms(phone, code):
    send_messag_example(phone,code)
    return True

def send_messag_example(phone,code):
	resp = requests.post("http://sms-api.luosimao.com/v1/send.json",auth=("api", "112b0a8bb357d7ecce843086d8d9f97a"),
	data={
		"mobile": phone,
		"message": " 您的验证码：%s【NU努高科技】" % (code)
	},timeout=3 , verify=False)

	result =json.loads(resp.content.decode())
	
	return result