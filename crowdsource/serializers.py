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
    class Meta:
        model = Tweets
        fields = '__all__'

class TweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ['tweet_text', 'Sentiment', 'timestamp']
