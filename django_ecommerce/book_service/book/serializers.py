from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model
    """
    class Meta:
        model = Book
        fields = '__all__'
        
    def validate_isbn(self, value):
        """
        Validate ISBN format (basic check)
        """
        if len(value) != 13 and len(value) != 10:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long")
        
        # Check if ISBN is numeric
        if not value.isdigit():
            # Allow 'X' only at the end of ISBN-10
            if not (len(value) == 10 and value[:-1].isdigit() and value[-1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X')):
                raise serializers.ValidationError("ISBN must contain only digits (except for ISBN-10 which can end with 'X')")
        
        return value 