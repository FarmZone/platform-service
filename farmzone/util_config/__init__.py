import logging
import os
import re
from django.conf import settings
from uuid import uuid4
import string
from random import choice, randint
from enum import unique as unique_enum, Enum
logger = logging.getLogger(__name__)


def underscorify(s, to_upper=True):
    """ Utility method to replace all non-word characters from the given string
    and join multi-word string with underscore.

    :param s: String which needs to be formatted
    :param to_upper: whether you want the final result in upper case or lowercase
    :return: Formatted String
    """
    if not s:
        return s
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single underscore
    s = re.sub(r"\s+", '_', s)

    return s.upper() if to_upper else s.lower()


def password_generator():
    """Utility to generate passwords for auto generated accounts
    :return: String
    """
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(characters) for x in range(randint(8, 16)))
    return password


def generateUUID():
    """Utility to generate UUID for django models

    :return: String
    """
    return str(uuid4())


def current_environment():
    env = os.environ.get('CURRENT_ENV')
    if not env:
        env = os.environ['DJANGO_SETTINGS_MODULE'].split('.')[-1]
    return env.lower()


def is_current_settings(settings):
    current_env = current_environment()
    return current_env == settings.strip().lower()


def generate_public_s3_access_url(file_path, bucket_name=None, region=None):
    if not file_path:
        return ''
    """Utility method to generate public URL for assets stored in S3
    :param file_path: file path name against which we will get the assets
    :param bucket_name: Bucket Name which has the asset
    :param region: Region which has the bucket
    :return: String which can be used to fetch the URL
    """
    if not bucket_name:
        bucket_name = settings.AWS_STORAGE_PUBLIC_BUCKET_NAME

    if not region:
        region = settings.AWS_REGION

    return "https://s3-{0}.amazonaws.com/{1}/{2}".format(region, bucket_name, file_path)


@unique_enum
class ModelEnum(Enum):
    @classmethod
    def get_values(cls):
        return [(s.name, s.value) for s in cls]

    @classmethod
    def as_map(cls, default_value=None, key_to_lower=False, value_as_none=False):
        key = lambda s: s.name.lower() if key_to_lower else s.name
        value = lambda s: default_value if (default_value is not None or value_as_none) else s.value
        return {key(s): value(s) for s in cls}

    @classmethod
    def as_list(cls, key=None):
        return [s.name if not key else {key: s.name} for s in cls]

    @classmethod
    def values(cls):
        return [s.value for s in cls]

    @classmethod
    def get_member(cls, member_name, is_comparision_case_sensitive=False):
        try:
            if is_comparision_case_sensitive:
                return [s for s in cls if s.value == member_name][0]
            else:
                return [s for s in cls if s.value.lower() == member_name.lower()][0]
        except IndexError as ex:
            raise Exception('\"{0}\" is not a member of the ModelEnum: {1}.'.format(member_name, cls.__name__))    \
                    .with_traceback(ex.__traceback__)


CustomEnum = ModelEnum


