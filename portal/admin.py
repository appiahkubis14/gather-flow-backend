
from django.contrib import admin
from .models import Cover_tbl, ConsentLocation_tbl, FarmerIdentificationtbl, OwnerIdentificationTbl, WorkerInTheFarmTbl, EndOfCollection,AdultInHouseholdTbl,ChildInHouseholdTbl,ChildRemediationTbl,HouseholdSensitizationTbl

admin.site.register(Cover_tbl)
admin.site.register(ConsentLocation_tbl)
admin.site.register(FarmerIdentificationtbl)
admin.site.register(OwnerIdentificationTbl)
admin.site.register(WorkerInTheFarmTbl)
admin.site.register(AdultInHouseholdTbl)
admin.site.register(ChildInHouseholdTbl)
admin.site.register(ChildRemediationTbl)
admin.site.register(HouseholdSensitizationTbl)
admin.site.register(EndOfCollection)
