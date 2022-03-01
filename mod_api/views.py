import datetime
from django.contrib.auth.models import User
from django.db.models import Case, When, Value
from news_aggregator.configuration import NEWS_SOURCES
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from mod_api.models import News, UserFavouriteNews
from mod_api.serializers import NewsSerializer, UserFavouriteNewsSerializer


class NewsModelViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['headline']

    def get_queryset(self):
        """GET MODEL QUERYSET OR FAKE BULK CREATE OBJECTS"""
        filter_query_param = self.request.query_params.get('query')
        extra_args = {}
        if filter_query_param:
            extra_args = {'token': filter_query_param}
        data = News.objects.filter(expiry_date__gt=datetime.datetime.now(),**extra_args)
        print(f'FOUND {data.count()} in DB')
        if not data and filter_query_param:
            print(f'FETCHING RECORDS FOR {filter_query_param}')
            data = []
            for key, value in NEWS_SOURCES.items():
                newdata = NEWS_SOURCES[key].get_data(query=filter_query_param)
                # print(newdata)
                for news in newdata:
                    # NEW_SOURCES must return instances of News ,
                    # couldnt do it in Source file due to django import errors
                    data.append(News(**news, expiry_date=News.expiration_time_calculation(), token=filter_query_param))
                print(data)
            data = News.objects.bulk_create(data)
        return data

    def list(self, request):
        # print(self.request.query_params.get('query'))
        serializer = NewsSerializer(self.get_queryset(), many=True)
        data = serializer.data
        return Response(data)


class UserFavouriteNewsModelViewSet(ModelViewSet):
    serializer_class = UserFavouriteNewsSerializer
    queryset = UserFavouriteNews.objects.all()

    def create(self, request, *args, **kwargs):
        """Favourite article toggler"""
        user_param = self.request.query_params.get('user')
        article_id_param = self.request.query_params.get('id')
        if user_param:
            # find a better way to get the id of user, should be done in serializer
            # to avoid extra query and atleast implement try-except
            requestdata = {"news": article_id_param, "user": User.objects.get(email=user_param).id}
        else:
            # anasbrain158
            requestdata = request.data
        favt_news_qs = UserFavouriteNews.objects.filter(news=requestdata['news'],user=requestdata['user'])
        if favt_news_qs:
            favt_news_qs.update(favourite=Case(When(favourite=True, then=Value(False)), default=Value(True)))
            serializer = self.get_serializer(favt_news_qs, many=True)
        else:
            serializer = self.get_serializer(data=requestdata)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
