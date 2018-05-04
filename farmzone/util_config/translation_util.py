import i18n


def get_locale_based_template(key, locale):
    return i18n.t(key, locale=locale)
