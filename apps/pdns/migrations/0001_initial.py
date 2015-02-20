# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=10)),
                ('modified_at', models.IntegerField()),
                ('account', models.CharField(max_length=40)),
                ('comment', models.CharField(max_length=64000)),
            ],
            options={
                'db_table': 'comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CriptoKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flags', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'cryptokeys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('master', models.CharField(max_length=128, null=True, blank=True)),
                ('last_check', models.IntegerField(null=True, blank=True)),
                ('type', models.CharField(max_length=6, choices=[(b'MASTER', b'Master'), (b'SLAVE', b'Slave'), (b'NATIVE', b'Native')])),
                ('notified_serial', models.IntegerField(default=1, null=True, blank=True)),
                ('account', models.CharField(max_length=40, null=True, blank=True)),
            ],
            options={
                'db_table': 'domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=32)),
                ('content', models.TextField()),
                ('domain', models.ForeignKey(to='pdns.Domain')),
            ],
            options={
                'db_table': 'domainmetadata',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('public', models.BooleanField(default=False)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainTemplateUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.ForeignKey(to='pdns.Domain')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.ForeignKey(to='pdns.Domain')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'A', b'A'), (b'CNAME', b'CNAME'), (b'MX', b'MX'), (b'NS', b'NS'), (b'PTR', b'PTR'), (b'SOA', b'SOA'), (b'SRV', b'SRV'), (b'TXT', b'TXT')])),
                ('content', models.CharField(max_length=64000, null=True, blank=True)),
                ('ttl', models.IntegerField(null=True, blank=True)),
                ('prio', models.IntegerField(null=True, blank=True)),
                ('change_date', models.IntegerField(null=True, blank=True)),
                ('disabled', models.BooleanField(default=False)),
                ('ordername', models.CharField(max_length=255, null=True, blank=True)),
                ('auth', models.BooleanField(default=True)),
                ('domain', models.ForeignKey(to='pdns.Domain')),
            ],
            options={
                'db_table': 'records',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecordTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'A', b'A'), (b'CNAME', b'CNAME'), (b'MX', b'MX'), (b'NS', b'NS'), (b'PTR', b'PTR'), (b'SOA', b'SOA'), (b'SRV', b'SRV'), (b'TXT', b'TXT')])),
                ('content', models.CharField(max_length=64000, null=True, blank=True)),
                ('prio', models.IntegerField(null=True, blank=True)),
                ('ttl', models.IntegerField(null=True, blank=True)),
                ('template', models.ForeignKey(to='pdns.DomainTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuperMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64)),
                ('nameserver', models.CharField(max_length=255)),
                ('account', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'supermasters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TsigKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('algorithm', models.CharField(max_length=50)),
                ('secret', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tsigkeys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLimit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_domain', models.IntegerField(default=10)),
                ('max_template', models.IntegerField(default=10)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='tsigkey',
            index_together=set([('name', 'algorithm')]),
        ),
        migrations.AlterUniqueTogether(
            name='supermaster',
            unique_together=set([('ip', 'nameserver')]),
        ),
        migrations.AlterIndexTogether(
            name='record',
            index_together=set([('domain',), ('name', 'type'), ('domain', 'ordername')]),
        ),
        migrations.AlterIndexTogether(
            name='domainmetadata',
            index_together=set([('domain', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='domain',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='criptokey',
            name='domain',
            field=models.ForeignKey(to='pdns.Domain'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='criptokey',
            index_together=set([('domain',)]),
        ),
        migrations.AddField(
            model_name='comment',
            name='domain',
            field=models.ForeignKey(to='pdns.Domain'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='comment',
            index_together=set([('domain',), ('name', 'type'), ('domain', 'modified_at')]),
        ),
    ]
