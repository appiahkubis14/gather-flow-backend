from django.contrib import admin
from .models import (
    Cover_tbl, ConsentLocation_tbl, FarmerIdentificationtbl, EndOfCollection,
    AdultInHouseholdTbl, ChildInHouseholdTbl, ChildRemediationTbl, HouseholdSensitizationTbl,HouseholdMembertbl
)

# Customize the admin site titles
admin.site.site_header = "REVIEW GHA - CLMRSHousehold profiling - 24-25"
admin.site.site_title = "Child Labour Survey Admin"
admin.site.index_title = "Child Labour Survey Administration"

class HouseholdMemberInline(admin.TabularInline):
    model = HouseholdMembertbl
    extra = 1  # Number of empty extra forms to display

@admin.register(AdultInHouseholdTbl)
class AdultInHouseholdAdmin(admin.ModelAdmin):
    list_display = ('cover', 'total_adults')
    inlines = [HouseholdMemberInline]


# @admin.register(ChildInHouseholdTbl)
# class ChildInHouseholdTblAdmin(admin.ModelAdmin):
#     list_display = ('cover', 'total_adults')
#     inlines = [HouseholdMemberInline]
    
    
# Register your models
admin.site.register(Cover_tbl)
admin.site.register(ConsentLocation_tbl)
admin.site.register(FarmerIdentificationtbl)
# admin.site.register(AdultInHouseholdTbl)
admin.site.register(ChildInHouseholdTbl)
admin.site.register(ChildRemediationTbl)
admin.site.register(HouseholdSensitizationTbl)
admin.site.register(EndOfCollection)
