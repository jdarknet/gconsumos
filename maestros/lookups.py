__author__ = 'julian'


from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from maestros.models import *

class TercerosLookup(LookupChannel):

    model = Terceros

    def get_query(self,q,request):
        return Terceros.objects.filter(Q(descripcion__icontains=q)).order_by('descripcion')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(obj.descripcion))
