import re

from django.utils import timezone
from rest_framework import serializers
from .models import User, Medication, MedicationSchedule, MedicationIntake, NotificationSettings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    name = serializers.CharField(source='username')
    photoUrl = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email', 'password', 'photoUrl')

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True) #чтобы не просил айди при пут запросе
    #фронтенд ждет name, так что переименуем:
    name = serializers.CharField(source='username')
    photoUrl = serializers.CharField(allow_blank=True, allow_null=True)
    #photoUrl = serializers.SerializerMethodField() #значение будет вычисляться с помощью метода ниже
    class Meta:
        model = User
        #fields = ('id', 'name', 'email', 'photoUrl') #указываем какие параметры из модели использовать
        fields = ('id', 'name', 'email', 'photoUrl')  # указываем какие параметры из модели использовать

    # def get_photoUrl(self, obj):
    #     request = self.context.get('request')
    #     if obj.photo and request:
    #         return request.build_absolute_uri(obj.photo.url)
    #     return None


class MedicationSerializer(serializers.ModelSerializer):
    #переписываем все названия в camelCase как во фронтенде
    dosagePerUnit = serializers.CharField(source='dosage_per_unit', allow_blank=True, allow_null=True, required=False)
    totalQuantity = serializers.IntegerField(source='total_quantity')
    remainingQuantity = serializers.IntegerField(source='remaining_quantity')
    lowStockThreshold = serializers.IntegerField(source='low_stock_threshold')
    trackStock = serializers.BooleanField(source='track_stock')
    iconName = serializers.CharField(source='icon_name')
    iconColor = serializers.CharField(source='icon_color')
    createdAt = serializers.IntegerField(source='created_at')
    updatedAt = serializers.IntegerField(source='updated_at')

    class Meta:
        model = Medication
        fields = [
            'id', 'name', 'form', 'dosagePerUnit', 'unit', 'instructions',
            'totalQuantity', 'remainingQuantity', 'lowStockThreshold', 'trackStock',
            'iconName', 'iconColor', 'createdAt', 'updatedAt' #тк user нет на фронте, не передаем его, но на беке храним
        ]
        #убрала readonly тк значения берем с фронта

    def validate_dosage_per_unit(self, value):
        # Пример валидации дозировки (проверка, что значение соответствует формату)
        if not re.match(r'^\d+(mg|g|mcg)$', value):  # Ожидаем, что дозировка будет числом и единицей измерения (mg, g, mcg)
            raise serializers.ValidationError("Invalid dosage format. Expected format: number + unit (mg, g, mcg).")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        #убрала переопределение created_at и updated_at
        return Medication.objects.create(**validated_data)

class MedicationScheduleSerializer(serializers.ModelSerializer):
    #все в camelCase
    medicationId = serializers.CharField(source='medication.id')
    mealRelation = serializers.CharField(source='meal_relation')
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date', allow_null=True, required=False)
    durationDays = serializers.IntegerField(source='duration_days', allow_null=True, required=False)
    createdAt = serializers.IntegerField(source='created_at')
    updatedAt = serializers.IntegerField(source='updated_at')
    class Meta:
        model = MedicationSchedule
        fields = [
            'id', 'medicationId', 'frequency', 'days', 'dates', 'times',
            'mealRelation', 'startDate', 'endDate', 'durationDays',
            'createdAt', 'updatedAt'
        ]
        # скрываем поле user от входа, оно задаётся на сервере
        extra_kwargs = {
            'user': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        medication_id = validated_data.pop('medication').get('id')
        validated_data['medication'] = Medication.objects.get(id=medication_id, user=self.context['request'].user)
        return MedicationSchedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'medication' in validated_data:
            medication_id = validated_data.pop('medication').get('id')
            validated_data['medication'] = Medication.objects.get(id=medication_id, user=self.context['request'].user)
        return super().update(instance, validated_data)


class MedicationIntakeSerializer(serializers.ModelSerializer):
    scheduleId = serializers.CharField(source='schedule.id')
    medicationId = serializers.CharField(source='medication.id')
    #используем CharField как во фронтенде
    scheduledTime = serializers.CharField(source='scheduled_time')
    scheduledDate = serializers.CharField(source='scheduled_date')

    takenAt = serializers.IntegerField(source='taken_at', allow_null=True, required=False)
    createdAt = serializers.IntegerField(source='created_at')
    updatedAt = serializers.IntegerField(source='updated_at')
    medicationName = serializers.CharField(source='medication_name')
    mealRelation = serializers.CharField(source='meal_relation')
    dosagePerUnit = serializers.CharField(source='dosage_per_unit', allow_null=True, required=False)
    dosageByTime = serializers.CharField(source='dosage_by_time')
    iconName = serializers.CharField(source='icon_name')
    iconColor = serializers.CharField(source='icon_color')

    class Meta:
        model = MedicationIntake
        fields = [
            'id', 'scheduleId', 'medicationId', 'scheduledTime', 'scheduledDate',
            'status', 'takenAt', 'createdAt', 'updatedAt', 'medicationName',
            'mealRelation', 'dosagePerUnit', 'dosageByTime', 'unit',
            'instructions', 'iconName', 'iconColor'
        ]

    def create(self, validated_data):
        # Получаем ID расписания
        schedule_data = validated_data.pop('schedule')  # это dict: {'id': '...'}
        schedule_id = schedule_data['id']

        # Получаем объект расписания из базы
        user = self.context['request'].user
        try:
            schedule = MedicationSchedule.objects.get(id=schedule_id, user=user)
        except MedicationSchedule.DoesNotExist:
            raise serializers.ValidationError("Расписание с таким ID не найдено или не принадлежит пользователю")

        # Получаем связанный объект лекарства
        medication = schedule.medication

        # Проставляем связанные объекты
        validated_data['schedule'] = schedule
        validated_data['medication'] = medication
        validated_data['medication_name'] = medication.name
        validated_data['meal_relation'] = schedule.meal_relation
        validated_data['dosage_per_unit'] = medication.dosage_per_unit
        validated_data['instructions'] = medication.instructions
        validated_data['unit'] = medication.unit
        validated_data['icon_name'] = medication.icon_name
        validated_data['icon_color'] = medication.icon_color

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'schedule' in validated_data:
            schedule_id = validated_data.pop('schedule').get('id')
            validated_data['schedule'] = MedicationSchedule.objects.get(id=schedule_id,
                                                                        user=self.context['request'].user)
        if 'medication' in validated_data:
            medication_id = validated_data.pop('medication').get('id')
            validated_data['medication'] = Medication.objects.get(id=medication_id, user=self.context['request'].user)

        if 'schedule' in validated_data or 'medication' in validated_data:
            validated_data['medication_name'] = validated_data['medication'].name
            validated_data['meal_relation'] = validated_data['schedule'].meal_relation
            validated_data['dosage_per_unit'] = validated_data['medication'].dosage_per_unit
            validated_data['instructions'] = validated_data['medication'].instructions
            validated_data['unit'] = validated_data['medication'].unit
            validated_data['icon_name'] = validated_data['medication'].icon_name
            validated_data['icon_color'] = validated_data['medication'].icon_color

        return super().update(instance, validated_data)

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = [
            'id', 'medicationRemindersEnabled',
            'minutesBeforeScheduledTime', 'lowStockRemindersEnabled',
        ]
        # Скрываем поле user от входа, оно задаётся на сервере
        extra_kwargs = {
            'user': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        # Удаляем user из validated_data, если он там есть
        validated_data.pop('user', None)
        # Создаём объект с текущим пользователем и остальными данными
        instance = NotificationSettings(
            user=self.context['request'].user,
            **validated_data
        )
        instance.save()  # save() установит id равным user.id
        return instance

    def update(self, instance, validated_data):
        # Обновляем только изменяемые поля
        instance.medicationRemindersEnabled = validated_data.get(
            'medicationRemindersEnabled', instance.medicationRemindersEnabled
        )
        instance.minutesBeforeScheduledTime = validated_data.get(
            'minutesBeforeScheduledTime', instance.minutesBeforeScheduledTime
        )
        instance.lowStockRemindersEnabled = validated_data.get(
            'lowStockRemindersEnabled', instance.lowStockRemindersEnabled
        )
        instance.save()
        return instance