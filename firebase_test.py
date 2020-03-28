from firebase import firebase

firebase = firebase.FirebaseApplication('https://winhacks2020-44957.firebaseio.com', None)
result = firebase.get('/Users', None)
print(result)

data = {
	"Name" : name,
	"Phone" : contact,
	"Location" : loc
}

result = firebase.post('/Users', data);
print(result)