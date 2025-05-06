from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError



class User(AbstractUser):
    #id берем с фронтенда
    id = models.CharField(max_length=20, primary_key=True)
    # Убираем уникальность с поля username
    username = models.CharField(max_length=150, blank=True)  # убираем unique=True
    # базовый класс пользователя уже включает поля username, password, first_name, last_name, и прочие.
    email = models.EmailField(unique=True) #делаем email уникальным
    photoUrl = models.CharField(max_length=255, blank=True, null=True)  # Новое поле для URL фотографии
    #photo = models.ImageField(upload_to='avatars/', blank=True, null=True) #будет хранится в папке media/avatars/

    USERNAME_FIELD = 'email' #теперь это логин
    REQUIRED_FIELDS = ['id', 'username'] #в сериализаторе переименован в name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Medication(models.Model):
    class Form(models.TextChoices):
        TABLET = "tablet", "Таблетки"
        CAPSULE = "capsule", "Капсулы"
        DROPS = "drops", "Капли"
        LIQUID = "liquid", "Жидкость"
        OINTMENT = "ointment", "Мазь"
        SPRAY = "spray", "Спрей"
        POWDER = "powder", "Порошок"

    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    form = models.CharField(max_length=20, choices=Form.choices)
    dosage_per_unit = models.CharField(max_length=100, blank=True, null=True) #необязательное
    unit = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    #Добавим проверку что значения неотрицательные:
    total_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    remaining_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    low_stock_threshold = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    track_stock = models.BooleanField(default=True)
    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=50)

    #время на фронте хранится в миллисекундах (Date.now()) поэтому пусть тут и далле будет просто число
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medication"
        verbose_name_plural = "Medications"


class MedicationSchedule(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Ежедневно"
        EVERY_OTHER_DAY = "every_other_day", "Через день"
        SPECIFIC_DAYS = "specific_days", "Определённые дни недели"
        SPECIFIC_DATES = "specific_dates", "Определённые даты"

    class MealRelation(models.TextChoices):
        BEFORE_MEAL = "before_meal", "До еды"
        AFTER_MEAL = "after_meal", "После еды"
        WITH_MEAL = "with_meal", "Во время еды"
        NO_RELATION = "no_relation", "Не связано с едой"

    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='schedules')
    frequency = models.CharField(max_length=30, choices=Frequency.choices)
    days = models.JSONField(default=list, blank=True, null=True)  # массив чисел 1-7 (понедельник–воскресенье)
    dates = models.JSONField(default=list, blank=True, null=True)  # массив строк YYYY-MM-DD
    times = models.JSONField(default=list)  # массив объектов: { time: "HH:MM", dosage: "value", unit: "мг" }
    meal_relation = models.CharField(max_length=30, choices=MealRelation.choices)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    #добавлен валидатор чтоб больше 0
    duration_days = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)]
    )
    #снова меняем на миллисекунды
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()

    def __str__(self):
        return f"{self.medication.name} ({self.start_date})"

    class Meta:
        verbose_name = "Medication Schedule"
        verbose_name_plural = "Medication Schedules"

class MedicationIntake(models.Model):
    class Status(models.TextChoices):
        TAKEN = "taken", "Принято"
        MISSED = "missed", "Пропущено"
        PENDING = "pending", "Ожидается"

    id = models.CharField(max_length=20, primary_key=True)
    scheduleId = models.CharField()
    medicationId = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    scheduled_time = models.CharField( #используем charfield как во фронте
        max_length=5,
        validators=[RegexValidator(r'^\d{2}:\d{2}$', "Time must be in HH:MM format.")]
    )
    scheduled_date = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{4}-\d{2}-\d{2}$', "Date must be in YYYY-MM-DD format.")]
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    taken_at = models.BigIntegerField(blank=True, null=True)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()

    # Дублируем поля для быстрого доступа
    medication_name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    meal_relation = models.CharField(max_length=30, choices=MedicationSchedule.MealRelation.choices)
    dosage_per_unit = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    dosage_by_time = models.CharField(max_length=20, validators=[MinLengthValidator(1)])
    unit = models.CharField(max_length=20, validators=[MinLengthValidator(1)])
    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.medication_name} at {self.scheduled_time} on {self.scheduled_date}"

    class Meta:
        verbose_name = "Medication Intake"
        verbose_name_plural = "Medication Intakes"


class NotificationSettings(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    medicationRemindersEnabled = models.BooleanField(default=True)
    minutesBeforeScheduledTime = models.IntegerField(default=15)
    lowStockRemindersEnabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.user.email}"

    def save(self, *args, **kwargs):
        # Устанавливаем id равным user.id перед сохранением
        if not self.id and self.user_id:  # Проверяем, что id ещё не установлен
            self.id = str(self.user_id)  # Преобразуем user_id в строку, так как id — CharField
        super().save(*args, **kwargs)

    def clean(self):
        # Проверяем, что id соответствует user_id
        if self.id and self.user_id and self.id != str(self.user_id):
            raise ValidationError("ID must match the associated user's ID.")

    class Meta:
        verbose_name = "Notification Settings"
        verbose_name_plural = "Notification Settings"