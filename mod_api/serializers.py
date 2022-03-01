from rest_framework import serializers
from mod_api.models import News, UserFavouriteNews


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id','location','source','headline',)


class UserFavouriteNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteNews
        fields = "__all__"
        # fields = ("favourite",'user__email','news',)