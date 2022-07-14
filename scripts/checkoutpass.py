import base64


# def get_password():
# 	short_code='295515'
# 	timestamp='20180615121533'
# 	passkey='cf731bec8f1f41287754580732cc926888c7cbfd193163da54e3bae6ab7496bb'


# 	return base64.b64encode(short_code+timestamp+passkey)


# password=get_password()

# print(password)

def get_sp_password():

	short_code = '668812'
	timestamp = '20210814202847'
	passkey = '25d3bb558d37e3e6f44c1a6c4e15640142abe9190d175dda69f2adb325aebe49'
	password = (short_code+passkey+timestamp).encode('utf-8')

	return (base64.b64encode(password).decode())


password = get_sp_password()

print(password)
