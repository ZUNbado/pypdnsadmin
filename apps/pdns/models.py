from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    TYPES=(
        ('MASTER', 'Master'),
        ('SLAVE', 'Slave'),
        ('NATIVE', 'Native'),
    )
    name = models.CharField(max_length=255)
    master = models.CharField(max_length=128, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6,choices=TYPES)
    notified_serial = models.IntegerField(blank=True, null=True, default=1)
    account = models.CharField(max_length=40, blank=True, null=True)
    users = models.ManyToManyField(User, blank=True)

    class Meta:
        db_table = 'domains'
        unique_together = ('name',)

    def __unicode__(self): return u'%s' % self.name

    def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)
        soa, created = Record.objects.get_or_create(domain=self,type='SOA',name=self.name)
        if created:
            soa.ttl = 3600
            soa.content = u'%s ns@%s 1' % (self.name, self.name)
        else:
            soa.content = u'%s ns@%s %s' % (self.name, self.name, int(soa.content.split(' ')[2]) + 1)
        soa.save()


class DomainUsers(models.Model):
    domain = models.ForeignKey(Domain)
    user = models.ForeignKey(User)

class Record(models.Model):
    TYPES=(
            ('A','A'),
            ('CNAME','CNAME'),
            ('MX','MX'),
            ('NS','NS'),
            ('PTR','PTR'),
            ('SOA','SOA'),
            ('SRV','SRV'),
            ('TXT','TXT'),
            )

    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True, choices=TYPES)
    content = models.CharField(max_length=64000, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    change_date = models.IntegerField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    ordername = models.CharField(max_length=255, blank=True, null=True)
    auth = models.BooleanField(default=True)

    class Meta:
        db_table = 'records'
        index_together = [
                [ 'name', 'type' ],
                [ 'domain' ],
                [ 'domain', 'ordername' ],
                ]

    def save(self, *args, **kwargs):
        super(Record, self).save(*args, **kwargs)
        if self.type != 'SOA':
            self.domain.save()



class UserLimit(models.Model):
    user = models.OneToOneField(User)
    max_domain = models.IntegerField(default=10)
    max_template = models.IntegerField(default=10)

class DomainTemplate(models.Model):
    name = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    description = models.TextField()

    def __unicode__(self): return u'%s' % self.name

class DomainTemplateUsers(models.Model):
    domain = models.ForeignKey(Domain)
    user = models.ForeignKey(User)

class RecordTemplate(models.Model):
    TYPES=(
            ('A','A'),
            ('CNAME','CNAME'),
            ('MX','MX'),
            ('NS','NS'),
            ('PTR','PTR'),
            ('SOA','SOA'),
            ('SRV','SRV'),
            ('TXT','TXT'),
            )

    template = models.ForeignKey(DomainTemplate)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True, choices=TYPES)
    content = models.CharField(max_length=64000, blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)

# PDNS STUFF, not used yet
class SuperMaster(models.Model):
    ip = models.CharField(max_length=64)
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)

    class Meta:
        db_table = 'supermasters'
        unique_together = ( ( 'ip', 'nameserver' ), )

class Comment(models.Model):
    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    modified_at = models.IntegerField()
    account = models.CharField(max_length=40)
    comment = models.CharField(max_length=64000)

    class Meta:
        db_table = 'comments'
        index_together = [
                [ 'domain' ],
                [ 'name', 'type' ],
                [ 'domain', 'modified_at' ],
                ]

class DomainMetaData(models.Model):
    domain = models.ForeignKey(Domain)
    kind = models.CharField(max_length=32)
    content = models.TextField()

    class Meta:
        db_table = 'domainmetadata'
        index_together = [ [ 'domain', 'kind' ], ]

class CriptoKey(models.Model):
    domain = models.ForeignKey(Domain)
    flags = models.IntegerField()
    active = models.BooleanField(default=True)
    content = models.TextField()

    class Meta:
        db_table = 'cryptokeys'
        index_together = [ 'domain' ]

class TsigKey(models.Model):
    name = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=50)
    secret = models.CharField(max_length=255)

    class Meta:
        db_table = 'tsigkeys'
        index_together = [ [ 'name', 'algorithm' ] ]
