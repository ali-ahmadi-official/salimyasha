from django.db import models

class About(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان درباره ما')
    content = models.TextField(verbose_name='محتوای درباره ما')

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'
    
    def __str__(self):
        return 'محتوای صفحه درباره ما'

class DemonstrationComment(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    comment = models.TextField(verbose_name='محتوای نظر')

    class Meta:
        verbose_name = 'نظر نمایشی'
        verbose_name_plural = 'نظرات نمایشی'
    
    def __str__(self):
        return f'نظر نمایشی {self.full_name}'

class ComprehensiveRule(models.Model):
    article = models.CharField(max_length=500, verbose_name='ماده')

    class Meta:
        verbose_name = 'قانون جامع'
        verbose_name_plural = 'قوانین جامع'
    
    def __str__(self):
        return self.article

class AppointmentCancellationRule(models.Model):
    article = models.CharField(max_length=500, verbose_name='ماده')

    class Meta:
        verbose_name = 'قانون لغو نوبت یا مشاوره'
        verbose_name_plural = 'قوانین لغو نوبت یا مشاوره'
    
    def __str__(self):
        return self.article

class DoctorRule(models.Model):
    article = models.CharField(max_length=500, verbose_name='ماده')

    class Meta:
        verbose_name = 'قانون دکترها'
        verbose_name_plural = 'قوانین دکترها'
    
    def __str__(self):
        return self.article

class PatientRule(models.Model):
    article = models.CharField(max_length=500, verbose_name='ماده')

    class Meta:
        verbose_name = 'قانون بیماران'
        verbose_name_plural = 'قوانین بیماران'
    
    def __str__(self):
        return self.article

class ParagraphComprehensiveRule(models.Model):
    comprehensive_rule = models.ForeignKey(ComprehensiveRule, on_delete=models.CASCADE, related_name='pcr')
    content = models.TextField(verbose_name='پاراگراف قانون')

    class Meta:
        verbose_name = 'پاراگراف قانون جامع'
        verbose_name_plural = 'پاراگراف های قوانین جامع'
    
    def __str__(self):
        return 'پاراگراف قانون جامع'

class ParagraphAppointmentCancellationRule(models.Model):
    appointment_cancellation_rule = models.ForeignKey(AppointmentCancellationRule, on_delete=models.CASCADE, related_name='pacr')
    content = models.TextField(verbose_name='پاراگراف قانون')

    class Meta:
        verbose_name = 'پاراگراف قانون لغو نوبت یا مشاوره'
        verbose_name_plural = 'پاراگراف های قوانین لغو نوبت یا مشاوره'
    
    def __str__(self):
        return 'پاراگراف قانون لغو نوبت'

class ParagraphDoctorRule(models.Model):
    doctor_rule = models.ForeignKey(DoctorRule, on_delete=models.CASCADE, related_name='pdr')
    content = models.TextField(verbose_name='پاراگراف قانون')

    class Meta:
        verbose_name = 'پاراگراف قانون دکترها'
        verbose_name_plural = 'پاراگراف های قوانین دکترها'
    
    def __str__(self):
        return 'پاراگراف قانون دکترها'

class ParagraphPatientRule(models.Model):
    patient_rule = models.ForeignKey(PatientRule, on_delete=models.CASCADE, related_name='ppr')
    content = models.TextField(verbose_name='پاراگراف قانون')

    class Meta:
        verbose_name = 'پاراگراف قانون بیماران'
        verbose_name_plural = 'پاراگراف های قوانین بیماران'
    
    def __str__(self):
        return 'پاراگراف قانون بیماران'

class QuestionAnswer(models.Model):
    audience_choices = [
        ('بیمار', 'بیمار'),
        ('دکتر', 'دکتر'),
    ]
    audience = models.CharField(max_length=20, choices=audience_choices, verbose_name='سوال برای')
    question = models.TextField(verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ')

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
    
    def __str__(self):
        return f'پرسش و پاسخ شماره {self.id}'