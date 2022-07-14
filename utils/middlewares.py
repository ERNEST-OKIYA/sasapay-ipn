from payments.models import PayoutsSourceLog
from ipware import get_client_ip
from django.conf import settings


class IpThrottler:

	def __init__(self,get_response):
		self.get_response = get_response

	def __call__(self,request):
		client_ip, is_routable = get_client_ip(request)

		if client_ip is None:
			raise KeyError(
				'Key Not Found'
			)

		else:

			if client_ip not in settings.ALLOWED_CLIENTS and self.is_payout(request):
				data={'source_ip':client_ip,'access':request.path}
				log=PayoutsSourceLog(**data)
				log.save()
				raise KeyError(
					'Key Not Found'
				)



		response = self.get_response(request)



		return response

	def is_payout(self,request):
		return '/ipn/pay/' in request.path