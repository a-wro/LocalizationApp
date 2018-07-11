from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class UserEntry(models.Model):
    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Entries'

    date = models.DateField(auto_now_add=True)
    zip = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]{2}-[0-9]{3}$', message='Zip code has format xx-xxx')])
    email = models.EmailField(unique=True) #EmailValidator
    name = models.CharField(max_length=50, validators=[RegexValidator(r'^([^\d!@#$%^&*])+$', message='Enter letters and/or spaces')])

    def __str__(self):
        return self.zip

    

    #override
    def save(self, *args, **kwargs):    
        super(UserEntry, self).save(*args, **kwargs)
        try: 
            query = ZipCodeCounter.objects.get(zip_code=self.zip)
            query.counter += 1
            query.save()
        except:
            z = ZipCodeCounter.objects.create(zip_code=self.zip)
            z.save()
    

class ZipCodeCounter(models.Model):
    zip_code = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]{2}-[0-9]{3}$', message='Zip code has format xx-xxx')])
    counter = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}: {}'.format(self.zip_code, self.counter)

