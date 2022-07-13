import base64


# def get_password():
# 	short_code='295515'
# 	timestamp='20180615121533'
# 	passkey='cf731bec8f1f41287754580732cc926888c7cbfd193163da54e3bae6ab7496bb'


# 	return base64.b64encode(short_code+timestamp+passkey)


# password=get_password()

# print(password)

def get_sp_password():

	short_code = '4032353'
	timestamp = '20190228132847'
	passkey = 'a511aee7db4c5dcd34a0b2d627679d46a87f912c2b65c91e93846d8437a33d2d'
	password = (short_code+passkey+timestamp).encode('utf-8')

	return (base64.b64encode(password).decode())


password = get_sp_password()

print(password)
