from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Import your models and serializers
from .models import (
    Cover_tbl,
    ConsentLocation_tbl,
    FarmerIdentificationtbl,
    AdultInHouseholdTbl,
    ChildInHouseholdTbl,
    ChildRemediationTbl,
    HouseholdSensitizationTbl,
    EndOfCollection
)
from .serializers import (
    CoverSerializer,
    ConsentLocationSerializer,
    FarmerIdentificationSerializer,
    AdultInHouseholdSerializer,
    ChildInHouseholdSerializer,
    ChildRemediationSerializer,
    HouseholdSensitizationSerializer,
    EndOfCollectionSerializer,
    CoverSyncSerializer  # This serializer handles nested data for Cover_tbl
)

# ------------------------------
# Standard ModelViewSets for CRUD
# ------------------------------

class CoverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Cover_tbl records to be viewed, created, updated or deleted.
    """
    queryset = Cover_tbl.objects.all()
    serializer_class = CoverSerializer


class ConsentLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ConsentLocation_tbl records to be viewed, created, updated or deleted.
    """
    queryset = ConsentLocation_tbl.objects.all()
    serializer_class = ConsentLocationSerializer


class FarmerIdentificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FarmerIdentificationtbl records to be viewed, created, updated or deleted.
    """
    queryset = FarmerIdentificationtbl.objects.all()
    serializer_class = FarmerIdentificationSerializer


class AdultInHouseholdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AdultInHouseholdTbl records to be viewed, created, updated or deleted.
    """
    queryset = AdultInHouseholdTbl.objects.all()
    serializer_class = AdultInHouseholdSerializer


class ChildInHouseholdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ChildInHouseholdTbl records to be viewed, created, updated or deleted.
    """
    queryset = ChildInHouseholdTbl.objects.all()
    serializer_class = ChildInHouseholdSerializer


class ChildRemediationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ChildRemediationTbl records to be viewed, created, updated or deleted.
    """
    queryset = ChildRemediationTbl.objects.all()
    serializer_class = ChildRemediationSerializer


class HouseholdSensitizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows HouseholdSensitizationTbl records to be viewed, created, updated or deleted.
    """
    queryset = HouseholdSensitizationTbl.objects.all()
    serializer_class = HouseholdSensitizationSerializer


class EndOfCollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EndOfCollection records to be viewed, created, updated or deleted.
    """
    queryset = EndOfCollection.objects.all()
    serializer_class = EndOfCollectionSerializer


# ------------------------------
# Custom APIView for Nested Sync
# ------------------------------

class CoverSyncView(APIView):
    """
    This endpoint accepts a nested JSON payload containing data for a Cover_tbl record 
    along with its related objects (e.g. ConsentLocation_tbl, FarmerIdentificationtbl, etc.).
    It creates a new Cover_tbl record (with related nested records) when a POST request is made,
    and updates an existing Cover_tbl record when a PUT request is made.
    """

    def post(self, request, *args, **kwargs):
        # Create a new record using nested data
        serializer = CoverSyncSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                cover_instance = serializer.save()
            return Response(CoverSyncSerializer(cover_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        # Update an existing Cover_tbl record and its related nested records
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
