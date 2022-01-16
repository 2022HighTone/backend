import copy
import googlemaps

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers

from domains.models import Store, Menu, Review


User = get_user_model()


class ReviewSeralizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    best_menu_name = serializers.CharField(source='menu.name', read_only=True)
    menu = serializers.CharField(write_only=True)

    class Meta:
        model = Review
        fields = ('text', 'rating', 'menu', 'username', 'best_menu_name')

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        menu_name = validated_data.pop('menu')
        
        user = User.objects.get(id=user_id)
        menu = Menu.objects.get(name=menu_name)
        store = self.context['store']

        return Review.objects.create(
            user=user,
            menu=menu,
            store=store,
            **validated_data
        )


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('name', 'price')


class StoreSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name')
    distance_name = serializers.CharField(source='distance.name')
    category_name = serializers.CharField(source='category.name')
    menus = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'id', 'name', 'address', 'latitude', 'longitude', 'school', 'distance', 'category',
            'school_name', 'distance_name', 'category_name', 'menus', 'reviews'
        )

    def create(self, validated_data):
        store = Store.objects.filter(Q(name=validated_data['name']) | Q(address=validated_data['address']))

        if store.exists():
            return store.first()

        data = copy.deepcopy(validated_data)

        gmaps = googlemaps.Client(key='AIzaSyCYFtPj7vyLQwM2YxY49oYbNavUU57OwcA')

        geocode_result = gmaps.geocode(data['address'])

        n_lat = geocode_result[0]['geometry']['location']['lat']
        n_lng = geocode_result[0]['geometry']['location']['lng']

        data['latitude'] = n_lat
        data['longitude'] = n_lng
        
        return Store.objects.create(**data)

    def get_menus(self, obj):
        price = self.context.pop('price', None)
        if price is None or price == '':
            menus = Menu.objects.filter(store=obj)
        else:
            menus = Menu.objects.filter(
                Q(store=obj) & Q(price__lte=price)
            )
        data = MenuSerializer(menus, many=True).data

        return data

    def get_reviews(self, obj):
        reviews = Review.objects.filter(store=obj)
        data = ReviewSeralizer(reviews, many=True).data

        return data