from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.accounts.permissions import *
from .serializers import *
from .bank import *

class Step1FormView(APIView):
	serializer_class=UserDetailSerializer
	permission_classes=[permissions.IsAuthenticated]

	def get(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		return Response({"message":"success","data":self.serializer_class(details).data},200)

	def post(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		data=request.data
		city=data.get('city')
		state=data.get('state')
		if not city: return Response({"message":"city is required"},400)
		if not state: return Response({"message":"state is required"},400)
		details.city=city
		details.state=state
		if details.step==0:
			details.step=1
		details.save()
		return Response({"message":"updated successfully","data":self.serializer_class(details).data},200)

	def put(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		data=request.data
		city=data.get('city',details.city)
		state=data.get('state',details.state)
		details.city=city
		details.state=state
		details.save()
		return Response({"message":"updated successfully"},200)


class Step2FormView(APIView):
	serializer_class=UserDetailSerializer
	permission_classes=[permissions.IsAuthenticated]

	def get(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		return Response({"message":"success","data":self.serializer_class(details).data},200)

	def post(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		data=request.data
		aadhar=data.get('aadhar_number')
		pan=data.get('pan_number')
		gstin=data.get('gstin_id')
		if not aadhar: return Response({"message":"aadhar number is required"},400)
		if not pan: return Response({"message":"pan number is required"},400)
		if not pan: return Response({"message":"gstin id is required"},400)
		details.aadhar_number=aadhar
		details.pan_number=pan
		details.gstin_id=gstin
		if details.step==1:
			details.step=2
		details.save()
		return Response({"message":"updated successfully","data":self.serializer_class(details).data},200)

	def put(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		data=request.data
		aadhar=data.get('aadhar_number',details.aadhar_number)
		pan=data.get('pan_number',details.pan_number)
		gstin=data.get('gstin_id',details.gstin_id)
		details.aadhar_number=aadhar
		details.pan_number=pan
		details.gstin_id=gstin
		details.save()
		return Response({"message":"updated successfully"},200)




class VirtualBankView(APIView):
	permission_classes=[IsVerified]

	def get(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		if not details.rzrp_details:
			bank=VirtualBank(request.user)
			data,status=bank.create()
			if not status:
				return Response({"message":data},400)
			details.rzrp_details=data
			details.save()
		bank=VirtualBank(request.user)
		data,status=bank.get_payments()
		return Response({"message":"success","data":details.rzrp_details,"transactions":data},200)

	def post(self,request):
		details,status=UserDetail.objects.get_or_create(user=request.user)
		if not details.rzrp_details:
			bank=VirtualBank(request.user)
			data,status=bank.create()
			if not status:
				return Response({"message":data},400)
			details.rzrp_details=data
			details.save()
		return Response({"message":"successfully created","data":details.rzrp_details})

	def put(self,request):
		bank=VirtualBank(request.user)
		data,status=bank.get_payments()
		if status:
			return Response({"message":"success","data":data},200)
		else:
			return Response({"message":data},400)



