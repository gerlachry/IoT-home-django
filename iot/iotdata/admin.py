from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from iotdata.models import Feed, ReadingType
from import_export import resources

# Register your models here.

#admin.site.register(ReadingType)
#admin.site.register(Feed)


class ReadingTypeResource(resources.ModelResource):
    class meta:
        model = ReadingType


class FeedResource(resources.ModelResource):
    class meta:
        model = Feed


@admin.register(ReadingType)
class ReadingTypeAdmin(ImportExportModelAdmin):
    list_display = ('reading_name',)
    list_filter = ('reading_name',)
    search_fields =['reading_name']
    resource_class = ReadingTypeResource


@admin.register(Feed)
class StudyAdmin(ImportExportModelAdmin):
    list_display = ('feed_name', 'data_location', 'feed_desc',)
    #list_filter = ('compound', 'study_phase')
    #search_fields =['study_synopsis','compound','drug_name','study_design','study_title']
    resource_class = FeedResource