from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user.models import Profile, Buddy, User

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'username', 'bio', 'profile_pic', 'date_of_birth', 'gender', 'phone_number', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email address."), code='invalid')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        if not token or not new_password:
            raise serializers.ValidationError(_('Both token and new password are required.'))

        try:
            user = UserModel.objects.get(**default_token_generator.check_token(token))
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(_('Invalid or expired token.'))

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(_('Invalid or expired token.'))

        return attrs


class BuddySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buddy
        fields = '__all__'
