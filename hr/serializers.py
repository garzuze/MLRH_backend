from rest_framework import serializers
from .models import Resume, Position
from django.contrib.auth import get_user_model

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    desired_positions = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)

    class Meta:
        model = Resume
        fields = [
            'id', 'name', 'user', 'cpf', 'gender', 'birth_date', 'birth_place', 
            'marital_status', 'spouse_name', 'spouse_profession', 'has_children', 
            'children_ages', 'is_smoker', 'has_car', 'has_disability', 
            'disability_cid', 'address', 'neighborhood', 'city', 'state', 'cep',
            'phone', 'contact_phone', 'email', 'linkedin', 'education_level', 
            'education_details', 'english_level', 'spanish_level', 
            'other_languages', 'computer_skills', 'additional_courses', 
            'desired_positions', 'expected_salary', 'available_full_time', 
            'available_morning_afternoon', 'available_afternoon_night', 
            'available_night_shift', 'available_1236', 'available_as_substitute', 
            'status', 'created_at',   'updated_at',
        ]