from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

account_sid = "ACd37c9f284658c4b14ed1878a1b4f7feb" # Your Account SID from www.twilio.com/console
auth_token  = "d4338b36ba002e27a41ddd4c3452bfce"  # Your Auth Token from www.twilio.com/console
def MessageUser(telephone, type, user, que):
	client = TwilioRestClient(account_sid, auth_token)
	try:
		message = client.messages.create(body=str(user)+ " has requested a " + str(type) + " meeting with you. Respond <" + str(que) +"> <Your Message>",
			to=telephone,
			from_="+17865654843") # Replace with your Twilio number
		return (True, message.sid)
	except TwilioRestException as e:
		return(False, e)
def Notify(telephone, user, response):
	client = TwilioRestClient(account_sid, auth_token)
	try:
		message = client.messages.create(body=str(user) + " has responded to your request with " + str(response),
			to="+"+telephone,
			from_="+17865654843") # Replace with your Twilio number
		return True
	except TwilioRestException as e:
		return(e)