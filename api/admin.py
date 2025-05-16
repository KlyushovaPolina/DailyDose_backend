from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Medication, MedicationSchedule, MedicationIntake, NotificationSettings

# Кастомизация админки для модели User
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'photoUrl')
    search_fields = ('id', 'email', 'username')

# Кастомизация админки для модели Medication
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'form', 'unit', 'totalQuantity', 'remainingQuantity', 'track_stock', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'instructions')


# Кастомизация админки для модели MedicationSchedule
class MedicationScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medication', 'frequency', 'start_date', 'end_date', 'created_at', 'updated_at')
    search_fields = ('id', 'medication__name')

# Кастомизация админки для модели MedicationIntake
class MedicationIntakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'scheduleId', 'medicationId', 'scheduled_date', 'scheduled_time', 'status', 'taken_at', 'created_at', 'updated_at')
    search_fields = ('id',)

# Кастомизация админки для модели NotificationSettings
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'medicationRemindersEnabled', 'minutesBeforeScheduledTime', 'lowStockRemindersEnabled')
    search_fields = ('id', 'user__email')

# Регистрация моделей в админке
admin.site.register(User, CustomUserAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(MedicationSchedule, MedicationScheduleAdmin)
admin.site.register(MedicationIntake, MedicationIntakeAdmin)
admin.site.register(NotificationSettings, NotificationSettingsAdmin)