from wsgiref import validate
from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    
    """Handles serialization and deserialization of User objects."""
    amount =serializers.IntegerField(required=False)
    # Passwords must be at least 8 characters, but no more than 128 
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'balance', 'amount')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and 
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)
    
    def update(self, instance, validated_data):
        """Performs an update on a User."""
        print("in user update function")
        print("USER UPDATE VALIDATE_DATA: ", validated_data)
        print("User serializer update, instance is: ", instance)
        #do a request to the transaction or mongodb server


        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)
        amount = validated_data.pop('amount')
        print("validated data: ", validated_data.items())
        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)
        if amount is not None:
            instance.balance = instance.balance + amount
        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    def validate(self, data):
        username = data.get('username', None)
        if username is None:
            raise serializers.ValidationError(
                'An username is required'
            )
        return { "username": username}
    
    def update(self, validated_data):
        """Performs an update on a User."""
        return "MESSAGE"
        
class UsernameStockSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    ticker = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        username = data.get('username', '')
        ticker = data.get("ticker", '')
        
        if username is None:
            raise serializers.ValidationError(
                'A username is required'
            )
        if ticker is None:
             raise serializers.ValidationError(
                'A ticker is required '
            )
       
        return { "username": username, "ticker": ticker}
    
    def update(self, validated_data):
        """Performs an update on a User."""
        
       
        return "message"

class UsernameAmountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    amount = serializers.FloatField(required=True)
   

    def validate(self, data):
        username = data.get('username', None)
        amount = data.get("amount", None)
        if username is None:
            raise serializers.ValidationError(
                'An username is required'
            )
        if amount is None:
            raise serializers.ValidationError(
                'An amount is required'
            )
        
        return { "username": username, "amount": amount}

    def update(self, validated_data):
        """Performs an update on a User."""
        
       
        return "message"

class UsernameAmountStockSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    ticker = serializers.CharField(max_length=255, required=True)
    amount = serializers.FloatField(required=True)

    def validate(self, data):
        username = data.get('username', None)
        amount = data.get("amount", None)
        ticker = data.get("ticker", None)
       
        if username is None:
            raise serializers.ValidationError(
                'An username is required'
            )
        if amount is None:
            raise serializers.ValidationError(
                'An amount is required'
            )
        if ticker is None:
            raise serializers.ValidationError(
                'An amount is required'
            )
        return { "username": username, "amount": amount, "ticker": ticker}
    
    def post(self, validated_data):
        """Performs an update on a User."""
        print("the data is: ", validated_data)
        return "message"

    

class UsernameDumplogSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        username = data.get('username', None)
        filename = data.get("filename", None)

        if username is None:
            raise serializers.ValidationError(
                'A username is required'
            )
        return { "username": username, "filename": filename}

    def update(self,  validated_data):
        """Performs an update on a User."""
        print ("validated data is: ", validated_data.items())
       
        return "updated data"

class DumplogSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255, required=True)
    def validate(self, data):
        filename = data.get("filename", None)
        if filename is None:
                raise serializers.ValidationError(
                    'A filename is required'
                )
        return { "filename": filename}

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    balance = serializers.IntegerField(read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)
        print("login serializer data: ", data)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
            'balance': user.balance
        }

