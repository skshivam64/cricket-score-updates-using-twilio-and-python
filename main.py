from twilio.rest import Client
from bs4 import BeautifulSoup
from urllib import request
import time

# Your Account SID from twilio.com/console
account_sid = "Your_Account_SID"
# Your Auth Token from twilio.com/console
auth_token = "Your_Authentication_Token"
# Receiver's number
receiver = "Reciever's_Number"
# Your twilio number
sender = "Your_Twilio_Number"


def extract_score(my_url, *id_kargs):
    try:
        resp = request.urlopen(my_url).read()
        soup = BeautifulSoup(resp, "html.parser")
        score = soup.find_all("a", class_=id_kargs[0])
        return score
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

        
def prettify(data):
    str = ''
    for each in data:
        for each_next in each:
            try:
                str += each_next.get_text()
            except Exception as e:
                str += each_next
            str += ' '
        str += '\n'
    return str


def main():
    while 1:
        my_data = extract_score("http://www.cricbuzz.com", "cb-font-12")
        sms_str = ''
        my_data = my_data[:4]
        # extracted just the four top results
        # one can also go with my_data[0] if he/she wants just the topmost result

        for each in my_data:
            sms_str += prettify(each)
            sms_str += "...............................................\n"

        send_sms(account_sid, auth_token, receiver, sender, sms_str)
        print(sms_str)
        time.sleep(600)
        # delayed further execution by 10 minutes
        
        
if __name__ == "__main__": main()

