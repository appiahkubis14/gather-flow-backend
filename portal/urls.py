
from django.urls import path
from .views import (
    CoverViewSet, ConsentLocationViewSet, FarmerIdentificationViewSet, OwnerIdentificationViewSet,
    WorkerInTheFarmViewSet, AdultInHouseholdViewSet, ChildInHouseholdViewSet, ChildRemediationViewSet,
    HouseholdSensitizationViewSet, EndOfCollectionViewSet
)
from .views import CoverSyncView

# For Cover_tbl endpoints
cover_list = CoverViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
cover_detail = CoverViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For ConsentLocation_tbl endpoints
consent_list = ConsentLocationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
consent_detail = ConsentLocationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For FarmerIdentificationtbl endpoints
farmer_list = FarmerIdentificationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
farmer_detail = FarmerIdentificationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For OwnerIdentificationTbl endpoints
owner_list = OwnerIdentificationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
owner_detail = OwnerIdentificationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For WorkerInTheFarmTbl endpoints
worker_list = WorkerInTheFarmViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
worker_detail = WorkerInTheFarmViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For AdultInHouseholdTbl endpoints
adult_list = AdultInHouseholdViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
adult_detail = AdultInHouseholdViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For ChildInHouseholdTbl endpoints
child_list = ChildInHouseholdViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
child_detail = ChildInHouseholdViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For ChildRemediationTbl endpoints
child_remediation_list = ChildRemediationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
child_remediation_detail = ChildRemediationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For HouseholdSensitizationTbl endpoints
sensitization_list = HouseholdSensitizationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
sensitization_detail = HouseholdSensitizationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# For EndOfCollection endpoints
end_of_collection_list = EndOfCollectionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
end_of_collection_detail = EndOfCollectionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('api/cover/', cover_list, name='cover-list'),
    path('api/cover/<int:pk>/', cover_detail, name='cover-detail'),

    path('api/consent-location/', consent_list, name='consent-location-list'),
    path('api/consent-location/<int:pk>/', consent_detail, name='consent-location-detail'),

    path('api/farmer-identification/', farmer_list, name='farmer-identification-list'),
    path('api/farmer-identification/<int:pk>/', farmer_detail, name='farmer-identification-detail'),

    path('api/owner-identification/', owner_list, name='owner-identification-list'),
    path('api/owner-identification/<int:pk>/', owner_detail, name='owner-identification-detail'),

    path('api/worker-in-farm/', worker_list, name='worker-in-farm-list'),
    path('api/worker-in-farm/<int:pk>/', worker_detail, name='worker-in-farm-detail'),

    path('api/adult-in-household/', adult_list, name='adult-in-household-list'),
    path('api/adult-in-household/<int:pk>/', adult_detail, name='adult-in-household-detail'),

    path('api/child-in-household/', child_list, name='child-in-household-list'),
    path('api/child-in-household/<int:pk>/', child_detail, name='child-in-household-detail'),

    path('api/child-remediation/', child_remediation_list, name='child-remediation-list'),
    path('api/child-remediation/<int:pk>/', child_remediation_detail, name='child-remediation-detail'),

    path('api/household-sensitization/', sensitization_list, name='household-sensitization-list'),
    path('api/household-sensitization/<int:pk>/', sensitization_detail, name='household-sensitization-detail'),

    path('api/end-of-collection/', end_of_collection_list, name='end-of-collection-list'),
    path('api/end-of-collection/<int:pk>/', end_of_collection_detail, name='end-of-collection-detail'),
    
     # Other endpoints...
    path('cover-sync/', CoverSyncView.as_view(), name='cover-sync'),
    # For updating an existing record:
    path('api/cover-sync/<int:pk>/', CoverSyncView.as_view(), name='cover-sync-detail'),
]


