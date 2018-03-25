from ajax_select import register, LookupChannel
from .models import User


@register('users')
class UserLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return self.model.objects\
            .filter(full_name__istartswith=q)[:20]

    def get_objects(self, ids):
        return self.model.objects\
            .filter(id__in=ids)
