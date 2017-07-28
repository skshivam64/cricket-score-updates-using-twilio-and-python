from twilio.rest import Client
from bs4 import BeautifulSoup
from urllib import request
import time

# Your Account SID from twilio.com/console
account_sid = "AC950b83acecb0840855a65741bc435b16"
# Your Auth Token from twilio.com/console
auth_token = "dc976b7faf7ef333a91587285bb4a357"
# Receiver's number
receiver = "+918809263651"
# Your twilio number
sender = "+13013218912"


def extract_score(my_url, *id_kargs):
    try:
        resp = request.urlopen(my_url).read()
        soup = BeautifulSoup(resp, "html.parser")
        score = soup.find_all("a", class_=id_kargs[0])
        return score[:4]
        # extracted just the four top results
        # one can also go with return score[0] if he/she wants just the best result
    except Exception as e:
        print(str(e))
        return "Network Error"


def send_sms(acc_sid, auth_tok, to_num, from_num, score):
    try:
        client = Client(acc_sid, auth_tok)
        message = client.messages.create(
                                            to=to_num,
                                            from_=from_num,
                                            body=score
                                        )
        print(message.sid)
    except Exception as e:
        print(str(e))


def main():
    while 1:
        data = extract_score("http://www.cricbuzz.com", "cb-font-12")
        for each in data:
            send_sms(account_sid, auth_token, receiver, sender, each.get_text())
        time.sleep(600)
        # delayed further execution by 10 minutes
if __name__ == "__main__": main()

