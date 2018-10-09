import django_tables2 as tables
from .models import User


class GPUserTable(tables.Table):
    chkbox = tables.CheckBoxColumn(attrs={'id': 'check_all'}, accessor="email")

    class Meta:
        attrs = {
            'class': 'table table-striped table-bordered table-hover',
            'id': 'usersTable'
        }
        model = User
        fields = ('chkbox', 'username', 'email', 'userprofilebase.generalpracticeuser.role')
        template_name = 'django_tables2/semantic.html'

class ClientUserTable(tables.Table):
    chkbox = tables.CheckBoxColumn(attrs={'id': 'check_all'}, accessor="email")

    class Meta:
        attrs = {
            'class': 'table table-striped table-bordered table-hover',
            'id': 'usersTable'
        }
        model = User
        fields = ('chkbox', 'username', 'email', 'userprofilebase.clientuser.role')
        template_name = 'django_tables2/semantic.html'