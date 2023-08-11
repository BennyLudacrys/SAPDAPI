from twilio.rest import Client


def sendsms():
    account_sid = 'AC164923848ad15b49f5dd618ca97337ab'
    auth_token = 'a44648c7ded4ba1b3831d36899528b3c'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="detectado com sucesso",
        from_='+14172753908',
        to='+258860240592'
    )

    print(message.sid)
