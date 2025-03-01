from rest_framework import viewsets
from .models import (
    Cover_tbl, ConsentLocation_tbl, FarmerIdentificationtbl, OwnerIdentificationTbl,
    WorkerInTheFarmTbl, AdultInHouseholdTbl, ChildInHouseholdTbl, ChildRemediationTbl,
    HouseholdSensitizationTbl, EndOfCollection
)
from .serializers import (
    CoverSerializer, ConsentLocationSerializer, FarmerIdentificationSerializer,
    OwnerIdentificationSerializer, WorkerInTheFarmSerializer, AdultInHouseholdSerializer,
    ChildInHouseholdSerializer, ChildRemediationSerializer, HouseholdSensitizationSerializer,
    EndOfCollectionSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Cover_tbl
from .serializers import CoverSyncSerializer

class CoverViewSet(viewsets.ModelViewSet):
    queryset = Cover_tbl.objects.all()
    serializer_class = CoverSerializer

class ConsentLocationViewSet(viewsets.ModelViewSet):
    queryset = ConsentLocation_tbl.objects.all()
    serializer_class = ConsentLocationSerializer

class FarmerIdentificationViewSet(viewsets.ModelViewSet):
    queryset = FarmerIdentificationtbl.objects.all()
    serializer_class = FarmerIdentificationSerializer

class OwnerIdentificationViewSet(viewsets.ModelViewSet):
    queryset = OwnerIdentificationTbl.objects.all()
    serializer_class = OwnerIdentificationSerializer

class WorkerInTheFarmViewSet(viewsets.ModelViewSet):
    queryset = WorkerInTheFarmTbl.objects.all()
    serializer_class = WorkerInTheFarmSerializer

class AdultInHouseholdViewSet(viewsets.ModelViewSet):
    queryset = AdultInHouseholdTbl.objects.all()
    serializer_class = AdultInHouseholdSerializer

class ChildInHouseholdViewSet(viewsets.ModelViewSet):
    queryset = ChildInHouseholdTbl.objects.all()
    serializer_class = ChildInHouseholdSerializer

class ChildRemediationViewSet(viewsets.ModelViewSet):
    queryset = ChildRemediationTbl.objects.all()
    serializer_class = ChildRemediationSerializer

class HouseholdSensitizationViewSet(viewsets.ModelViewSet):
    queryset = HouseholdSensitizationTbl.objects.all()
    serializer_class = HouseholdSensitizationSerializer

class EndOfCollectionViewSet(viewsets.ModelViewSet):
    queryset = EndOfCollection.objects.all()
    serializer_class = EndOfCollectionSerializer




class CoverSyncView(APIView):
    """
    This endpoint accepts a nested JSON containing all sections of data
    for a particular farmer (identified by Cover_tbl) and creates or updates
    the master record along with all its related data.
    """
    def post(self, request, *args, **kwargs):
        serializer = CoverSyncSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                cover_instance = serializer.save()
            return Response(CoverSyncSerializer(cover_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            cover_instance = Cover_tbl.objects.get(pk=pk)
        except Cover_tbl.DoesNotExist:
            return Response({'error': 'Cover record not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CoverSyncSerializer(cover_instance, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                cover_instance = serializer.save()
            return Response(CoverSyncSerializer(cover_instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
