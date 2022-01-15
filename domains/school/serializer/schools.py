import requests
import copy
import googlemaps

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers

from domains.models import School, Store
from domains.store.serializer import StoreSerializer

User = get_user_model()


class SchoolSerializer(serializers.ModelSerializer):
    stores = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = '__all__'

    def create(self, validated_data):
        school = School.objects.filter(Q(name=validated_data['name']) | Q(address=validated_data['address']))

        if school.exists():
            return school.first()

        data = copy.deepcopy(validated_data)

        gmaps = googlemaps.Client(key='AIzaSyCYFtPj7vyLQwM2YxY49oYbNavUU57OwcA')

        geocode_result = gmaps.geocode(data['address'])

        n_lat = geocode_result[0]['geometry']['location']['lat']
        n_lng = geocode_result[0]['geometry']['location']['lng']

        data['latitude'] = n_lat
        data['longitude'] = n_lng
        
        return School.objects.create(**data)

    def get_stores(self, obj):
        categories = self.context['categories']
        distance = self.context['distance']
        stores = Store.objects.filter(
            Q(school=obj) & Q(category__in=categories) & Q(distance__in=distance)
        )
        data = StoreSerializer(stores, many=True).data

        return data


def school_list_method(name):
    res = requests.get(f'https://open.neis.go.kr/hub/schoolInfo?key=815471348a0d4d169c2ae84576251be5&Type=json&SCHUL_NM={name}')

    res_dict = {}

    try:
        school_info = res.json()['schoolInfo'][1]['row'][0]
        name = school_info['SCHUL_NM']
        address = school_info['ORG_RDNMA']
        res_dict['name'] = name
        res_dict['address'] = address
        return res_dict

    except:
        return res_dict