from wsrequests import WsRequests

wsr = WsRequests()

# login django
wsr.get('http://localhost:3000/accounts/login/')
wsr.post(
    'http://localhost:3000/accounts/login/',
    data={
        'username': 'test',  # Djangoのユーザ名とパスワード
        'password': 'test',
        'csrfmiddlewaretoken': wsr.cookies['csrftoken'],
        'next': '/',
    }
)
wsr.connect('ws://localhost:3000/ws/boards/1')
wsr.receive_message()
wsr.disconnect()
