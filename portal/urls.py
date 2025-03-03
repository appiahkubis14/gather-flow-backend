from django.urls import path
from .views import (
    CoverViewSet, ConsentLocationViewSet, FarmerIdentificationViewSet, 
    AdultInHouseholdViewSet, ChildInHouseholdViewSet, ChildRemediationViewSet,
    HouseholdSensitizationViewSet, EndOfCollectionViewSet, CoverSyncView
)

# Standard endpoints using viewset.as_view() for individual CRUD actions
cover_list = CoverViewSet.as_view({'get': 'list', 'post': 'create'})
cover_detail = CoverViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

consent_list = ConsentLocationViewSet.as_view({'get': 'list', 'post': 'create'})
consent_detail = ConsentLocationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

farmer_list = FarmerIdentificationViewSet.as_view({'get': 'list', 'post': 'create'})
farmer_detail = FarmerIdentificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

adult_list = AdultInHouseholdViewSet.as_view({'get': 'list', 'post': 'create'})
adult_detail = AdultInHouseholdViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

child_list = ChildInHouseholdViewSet.as_view({'get': 'list', 'post': 'create'})
child_detail = ChildInHouseholdViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

child_remediation_list = ChildRemediationViewSet.as_view({'get': 'list', 'post': 'create'})
child_remediation_detail = ChildRemediationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

sensitization_list = HouseholdSensitizationViewSet.as_view({'get': 'list', 'post': 'create'})
sensitization_detail = HouseholdSensitizationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

end_of_collection_list = EndOfCollectionViewSet.as_view({'get': 'list', 'post': 'create'})
end_of_collection_detail = EndOfCollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('cover/', cover_list, name='cover-list'),
    path('cover/<int:pk>/', cover_detail, name='cover-detail'),

    path('consent-location/', consent_list, name='consent-location-list'),
    path('consent-location/<int:pk>/', consent_detail, name='consent-location-detail'),

    path('farmer-identification/', farmer_list, name='farmer-identification-list'),
    path('farmer-identification/<int:pk>/', farmer_detail, name='farmer-identification-detail'),

    path('adult-in-household/', adult_list, name='adult-in-household-list'),
    path('adult-in-household/<int:pk>/', adult_detail, name='adult-in-household-detail'),

    path('child-in-household/', child_list, name='child-in-household-list'),
    path('child-in-household/<int:pk>/', child_detail, name='child-in-household-detail'),

    path('child-remediation/', child_remediation_list, name='child-remediation-list'),
    path('child-remediation/<int:pk>/', child_remediation_detail, name='child-remediation-detail'),

    path('household-sensitization/', sensitization_list, name='household-sensitization-list'),
    path('household-sensitization/<int:pk>/', sensitization_detail, name='household-sensitization-detail'),

    path('end-of-collection/', end_of_collection_list, name='end-of-collection-list'),
    path('end-of-collection/<int:pk>/', end_of_collection_detail, name='end-of-collection-detail'),

    # Nested sync endpoint for Cover_tbl and related objects:
    path('cover-sync/', CoverSyncView.as_view(), name='cover-sync'),
    path('cover-sync/<int:pk>/', CoverSyncView.as_view(), name='cover-sync-detail'),
]
