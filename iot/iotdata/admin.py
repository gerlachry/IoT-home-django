from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from iotdata.models import Feed, ReadingType, FeedType
from import_export import resources, fields

# Register your models here.

#admin.site.register(ReadingType)
#admin.site.register(FeedType)


class ReadingTypeResource(admin.StackedInline):
    model = ReadingType


class FeedTypeResource(admin.StackedInline):
    model = FeedType


class FeedResource(resources.ModelResource):
    #reading_name = fields.Field(column_name='reading_name', attribute='reading_name', widget=ForeignKeyWidget(ReadingType, 'reading_type'))

    class meta:
        model = Feed
        #fields = ('feed_name', 'feed_desc', 'reading_name', 'data_location')


@admin.register(ReadingType)
class ReadingTypeAdmin(ImportExportModelAdmin):
    list_display = ('reading_name',)
    list_filter = ('reading_name',)
    search_fields =['reading_name']
    resource_class = ReadingTypeResource

@admin.register(FeedType)
class FeedTypeAdmin(ImportExportModelAdmin):
    list_display = ('feed_type', 'feed_desc')
    resource_class = FeedTypeResource


@admin.register(Feed)
class StudyAdmin(ImportExportModelAdmin):
    list_display = ('feed_name', 'data_location', 'feed_desc', 'reading_name')
    #list_filter = ('compound', 'study_phase')
    #search_fields =['study_synopsis','compound','drug_name','study_design','study_title']
    resource_class = FeedResource

    def reading_name(self, instance):
        return instance.reading_type.reading_name