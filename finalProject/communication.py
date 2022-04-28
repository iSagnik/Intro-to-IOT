from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC830f3ae839a9e467da9c46c2c770a7b8"
auth_token = "0588b5bd57388181f94a8cc7437ff4bd"
from_user = '+19205888804'
client = Client(account_sid, auth_token)

def send_message(number, msg):
    message = client.messages \
        .create(
            body=msg,
            from_= from_user,
            to=number
        )
    return (message.status, message.sid)

if __name__=="__main__":
    print("This module should only be imported.")
    result = send_message('+17045773529', "Sup Lauren - Sagnik")
    # print(result)