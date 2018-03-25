import logging
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings
from farmzone import util_config as utils
from storages.backends.s3boto3 import S3Boto3Storage
from farmzone.util_config import ModelEnum, generateUUID, password_generator, underscorify
logger = logging.getLogger(__name__)


class PhoneType(ModelEnum):
    MOBILE = "Mobile"
    LANDLINE = "Landline"


def upload_orig_image_path(instance, file):
    return "user/orig/{id}/{file}".format(id=instance.id, file=file)


def upload_thumb_image_path(instance, file):
    return "user/thumb/{id}/{file}".format(id=instance.id, file=file)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimestampedModel):
    full_name = models.CharField(max_length=128, null=True)
    img_orig = models.ImageField(upload_to=upload_orig_image_path, null=True, blank=True,
                                 storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))
    img_thumb = models.ImageField(upload_to=upload_thumb_image_path, null=True, blank=True,
                                  storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))
    is_admin = models.BooleanField(default=False)
    #reset_password = models.BooleanField(default=True, )

    class Meta:
        db_table = "users"
        ordering = ('full_name', )

    def __str__(self):
        return "{0}#{1}".format(self.display_name(), self.id)

    def get_img_orig(self):
        if self.img_orig.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_orig.name)
        return str(self.img_orig.name) if self.img_orig.name else ''

    def get_img_thumb(self):
        if self.img_thumb.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_thumb.name)
        return str(self.img_thumb.name) if self.img_thumb.name else ''

    def save(self, *args, **kwargs):
        if not self.full_name and (self.first_name, self.last_name):
            self.full_name = "{0} {1}".format(self.first_name, self.last_name)
        elif self.full_name:
            name = self.full_name.strip().split()
            self.first_name = name[0] if name else ""
            self.last_name = name[-1] if len(name) > 1 else ""

        if not self.username:
            self.username = generateUUID()

        if not self.password:
            self.password = password_generator(),
        super(User, self).save(*args, **kwargs)

    def get_phone_number(self):
        record = PhoneNumber.get_primary_contact(self)
        if record:
            return record.phone_number

    def display_name(self):
        return self.full_name or self.first_name

    @classmethod
    def create_user(cls, user_name, first_name=None, last_name=None):
        logger.info("Creating new user entry")
        return User.objects.create(first_name=first_name, last_name=last_name, full_name=str(user_name))


class UserRoles(Group, TimestampedModel):
    alias_name = models.CharField(max_length=64)

    class Meta:
        db_table = "user_roles"
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

    def __str__(self):
        return "{0}: {1}".format(self.name, self.alias_name)


class PhoneNumber(TimestampedModel):
    """
    Model to hold phone numbers
    """
    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    type = models.CharField(max_length=15, choices=PhoneType.get_values(), default=PhoneType.MOBILE.value)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

    def update_phone_number(self, new_number):
        self.phone_number = new_number
        self.is_active = True
        self.save()

    @staticmethod
    def is_record_exists(phone_number):
        if PhoneNumber.objects.filter(phone_number=phone_number).exists():
            return True
        else:
            return False

    @staticmethod
    def get_primary_contact(user, raise_404=True, error_response=None):
        primary_contact = PhoneNumber.objects.filter(user=user, is_active=True, is_primary=True).first()
        if not primary_contact:
            logger.warning("User {user_id} didn't have any phone_number marked as primary "
                           "falling back to return first number".format(user_id=user.id))
            primary_contact = PhoneNumber.objects.filter(user=user, is_active=True).first()

        logger.info("Contact for the user: {0} is {1}".format(user, primary_contact))
        return primary_contact

    @classmethod
    def create_phone_number(cls, user, mobile_number, is_active=False, is_primary=True, type=PhoneType.MOBILE.value):
        logger.info("Creating new PhoneNumber entry for the mobile number {0} "
                    "for the new userId: {1}".format(mobile_number, user.id))
        PhoneNumber.objects.create(user=user,
                                   phone_number=mobile_number,
                                   is_active=is_active,
                                   is_primary=is_primary,
                                   type=type)

    class Meta:
        db_table = "phone_numbers"
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"


class AppConfiguration(TimestampedModel):
    key = models.CharField(max_length=56, unique=True)
    value = models.CharField(max_length=56)

    class Meta:
        db_table = "app_configurations"

    @classmethod
    def get_config(cls, key, default_value=None):
        config_value = AppConfiguration.objects.filter(key=key).values_list('value', flat=True).first()
        if config_value:
            return config_value
        logger.warn('No such key defined in app configuration. '
                    'Key - {0}. Returning default value: {1}'.format(key, default_value))
        return default_value

    @classmethod
    def get_config_in_batch(cls, keys_with_default_values):
        """
        :param keys_with_default_values: Mapping of keys with their default values.
                                         If you do not wanna pass a default value wrt a key, passing None is mandatory.
        :return: Mapping of requested keys with the db_value or default_value passed in as a parameter.
        """
        config_values = AppConfiguration.objects.filter(key__in=keys_with_default_values.keys()).values('value', 'key')
        resultant_config = dict()

        for config in config_values:
            resultant_config[config['key']] = config['value']

        for key, default_value in keys_with_default_values.items():
            if key not in resultant_config:
                resultant_config[key] = default_value
                logger.warn('No such key defined in app configuration. '
                            'Key - {0}. Returning default value: {1}'.format(key, default_value))
        return resultant_config

    def save(self, *args, **kwargs):
        # Convert the name to Caps separated by underscores
        self.key = underscorify(self.key)
        super().save(*args, **kwargs)


def get_app_configurations():
    configurations = AppConfiguration.objects.all()
    config_dict = {}
    for config in configurations:
        config_dict[config.key] = config.value
    return config_dict
