from rest_framework import serializers
from .models import CSFormData, Tweets

class CSFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSFormData
        fields = ['latitude', 'longitude', 'feet', 'inch', 'location', 'timestamp']

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSFormData
        fields = '__all__'

class TweetsMapSerializer(serializers.ModelSerializer):
    # only address != "" values

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['address'] == "":
            return None
        return data
    
    class Meta:
        model = Tweets
        fields = ['tweet_text', 'sentiment', 'latitude', 'longitude', 'address', 'timestamp']


class TweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ['tweet_text', 'sentiment', 'timestamp']
    