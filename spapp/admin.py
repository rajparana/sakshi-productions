from django.contrib import admin
from .models import *

class AlbumInline(admin.StackedInline):
    model = Album
    extra = 1
    readonly_fields = ['album_preview']
    fieldsets = [
        (None,{'fields':('category', ('album', 'album_preview'))})]

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'thumbnail_preview', 'destination')
    search_fields = ('title', 'category__name', 'destination', 'text')
    list_filter = ('category__name','destination')
    readonly_fields = ['thumbnail_preview']
    fieldsets = [
        ('Filter Fields',{'fields':(('author',),('category','destination'),)}),
        ('Media Fields',{'fields':(('youtube',),('thumbnail','thumbnail_preview'),)}),
        ('Post Fields',{'fields':(('title',),('text',),('created_date','published_date'),)}),]

    inlines = [AlbumInline]


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('post', 'category', 'album_preview','crousel')
    search_fields = ('post', 'category')
    readonly_fields = ['album_preview']
    fieldsets = [
        ('Filter Fields',{'fields':(('post','category'),)}),
        ('Media Fields',{'fields':(('album','album_preview'),)}),
        ('Home Featured',{'fields':(('crousel'),('top_quote','bottom_quote','testimonial','reach_us'),)}),
        ('About Featured',{'fields':(('about_top','about_middle','about_bottom','about_quote'),)}),
        ('Other Featured',{'fields':(('contact','head'),)}),
        ('Time Stamp',{'fields':(('created_date','published_date'),)}),]

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'username', 'mobile', 'is_staff')
    search_fields = ('first_name', 'email', 'username', 'mobile')
    list_filter = ('first_name',)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Album, AlbumAdmin)
admin.site.register(TopQuote)
admin.site.register(BottomQuote)
admin.site.register(CollageCrousel)
admin.site.register(SlideCrousel)
admin.site.register(Reach)
admin.site.register(Testimonial)
admin.site.register(TopAbout)
admin.site.register(MidAbout)
admin.site.register(BottomAbout)
admin.site.register(AboutQuote)
admin.site.register(Service)
admin.site.register(Expertise)
admin.site.register(Contact)
