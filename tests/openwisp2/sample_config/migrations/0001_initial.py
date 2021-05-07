# Generated by Django 3.0.7 on 2020-06-27 11:16
import collections
import re
import uuid

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
import swapper
import taggit.managers
from django.conf import settings
from django.db import migrations, models

import openwisp_controller.config.base.template
import openwisp_users.mixins
import openwisp_utils.base
import openwisp_utils.utils
from openwisp_controller.config import settings as app_settings
from openwisp_controller.config.base.template import default_auto_cert


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        swapper.dependency('openwisp_users', 'Organization'),
        ('sample_pki', '0002_default_group_permissions'),
        swapper.dependency('openwisp_ipam', 'Subnet'),
        swapper.dependency('openwisp_ipam', 'Ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                (
                    'backend',
                    models.CharField(
                        choices=[
                            ('netjsonconfig.OpenWrt', 'OpenWRT'),
                            ('netjsonconfig.OpenWisp', 'OpenWISP Firmware 1.x'),
                        ],
                        help_text=(
                            'Select <a href="http://netjsonconfig.openwisp.org/en/'
                            'stable/" target="_blank">netjsonconfig</a> backend'
                        ),
                        max_length=128,
                        verbose_name='backend',
                    ),
                ),
                (
                    'config',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'ensure_ascii': False, 'indent': 4},
                        help_text='configuration in NetJSON DeviceConfiguration format',
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='configuration',
                    ),
                ),
                (
                    'status',
                    model_utils.fields.StatusField(
                        choices=[
                            ('modified', 'modified'),
                            ('applied', 'applied'),
                            ('error', 'error'),
                        ],
                        default='modified',
                        help_text=(
                            '"modified" means the configuration is not applied yet; \n'
                            '"applied" means the configuration is applied successfully;'
                            ' \n'
                            '"error" means the configuration caused issues '
                            'and it was rolled back;'
                        ),
                        max_length=100,
                        no_check_for_status=True,
                        verbose_name='configuration status',
                    ),
                ),
                (
                    'context',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'ensure_ascii': False, 'indent': 4},
                        help_text=(
                            'Additional <a href="http://netjsonconfig.openwisp.org'
                            '/en/stable/general/basics.html#context" target="_blank">'
                            'context (configuration variables)</a> in JSON format'
                        ),
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'verbose_name': 'configuration',
                'verbose_name_plural': 'configurations',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedTemplate',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'object_id',
                    models.UUIDField(db_index=True, verbose_name='object ID'),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'content_type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='sample_config_taggedtemplate_tagged_items',
                        to='contenttypes.contenttype',
                        verbose_name='content type',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Tagged item',
                'verbose_name_plural': 'Tags',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TemplateTag',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=100, unique=True, verbose_name='name'),
                ),
                (
                    'slug',
                    models.SlugField(max_length=100, unique=True, verbose_name='slug'),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vpn',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                (
                    'config',
                    jsonfield.fields.JSONField(
                        default=dict,
                        dump_kwargs={'ensure_ascii': False, 'indent': 4},
                        help_text='configuration in NetJSON DeviceConfiguration format',
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='configuration',
                    ),
                ),
                (
                    'host',
                    models.CharField(
                        help_text='VPN server hostname or ip address', max_length=64
                    ),
                ),
                (
                    'key',
                    openwisp_utils.base.KeyField(
                        db_index=True,
                        default=openwisp_utils.utils.get_random_key,
                        help_text=None,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[^\\s/\\.]+$'),
                                code='invalid',
                                message=(
                                    'This value must not contain spaces, '
                                    'dots or slashes.'
                                ),
                            )
                        ],
                    ),
                ),
                (
                    'backend',
                    models.CharField(
                        choices=[
                            ('openwisp_controller.vpn_backends.OpenVpn', 'OpenVPN'),
                            ('openwisp_controller.vpn_backends.Wireguard', 'WireGuard'),
                            (
                                'openwisp_controller.vpn_backends.VxlanWireguard',
                                'VXLAN over WireGuard',
                            ),
                        ],
                        help_text='Select VPN configuration backend',
                        max_length=128,
                        verbose_name='VPN backend',
                    ),
                ),
                ('notes', models.TextField(blank=True)),
                ('dh', models.TextField(blank=True)),
                ('public_key', models.CharField(blank=True, max_length=44)),
                ('private_key', models.CharField(blank=True, max_length=44)),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'ca',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_pki.ca',
                        verbose_name='Certification Authority',
                    ),
                ),
                (
                    'cert',
                    models.ForeignKey(
                        blank=True,
                        help_text='leave blank to create automatically',
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_pki.cert',
                        verbose_name='x509 Certificate',
                    ),
                ),
                (
                    'ip',
                    models.ForeignKey(
                        blank=True,
                        help_text=(
                            'Internal IP address of the VPN '
                            'server interface, if applicable'
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.OPENWISP_IPAM_IPADDRESS_MODEL,
                        verbose_name='Internal IP',
                    ),
                ),
                (
                    'organization',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=swapper.get_model_name('openwisp_users', 'Organization'),
                        verbose_name='organization',
                    ),
                ),
                (
                    'subnet',
                    models.ForeignKey(
                        blank=True,
                        help_text=(
                            'Subnet IP addresses used by VPN clients, if applicable'
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.OPENWISP_IPAM_SUBNET_MODEL,
                        verbose_name='Subnet',
                    ),
                ),
                (
                    'auth_token',
                    models.CharField(
                        blank=True,
                        help_text=(
                            'Authentication token for triggering "Webhook Endpoint"'
                        ),
                        max_length=128,
                        null=True,
                        verbose_name='Webhook AuthToken',
                    ),
                ),
                (
                    'webhook_endpoint',
                    models.CharField(
                        blank=True,
                        help_text=(
                            'Webhook to trigger for updating server configuration '
                            '(e.g. https://openwisp2.mydomain.com:8081/trigger-update)'
                        ),
                        max_length=128,
                        null=True,
                        verbose_name='Webhook Endpoint',
                    ),
                ),
            ],
            options={
                'verbose_name': 'VPN server',
                'verbose_name_plural': 'VPN servers',
                'abstract': False,
            },
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VpnClient',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('auto_cert', models.BooleanField(default=False)),
                ('public_key', models.CharField(blank=True, max_length=44)),
                ('private_key', models.CharField(blank=True, max_length=44)),
                (
                    'vni',
                    models.PositiveIntegerField(
                        blank=True,
                        db_index=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(16777216),
                        ],
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'cert',
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_pki.cert',
                    ),
                ),
                (
                    'config',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_config.config',
                    ),
                ),
                (
                    'ip',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='openwisp_ipam.ipaddress',
                    ),
                ),
                (
                    'vpn',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_config.vpn',
                    ),
                ),
            ],
            options={
                'verbose_name': 'VPN client',
                'verbose_name_plural': 'VPN clients',
                'abstract': False,
                'unique_together': {('vpn', 'vni'), ('config', 'vpn')},
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                (
                    'backend',
                    models.CharField(
                        choices=[
                            ('netjsonconfig.OpenWrt', 'OpenWRT'),
                            ('netjsonconfig.OpenWisp', 'OpenWISP Firmware 1.x'),
                        ],
                        help_text=(
                            'Select <a href="http://netjsonconfig.openwisp.org/en/'
                            'stable/" target="_blank">netjsonconfig</a> backend'
                        ),
                        max_length=128,
                        verbose_name='backend',
                    ),
                ),
                (
                    'config',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'ensure_ascii': False, 'indent': 4},
                        help_text='configuration in NetJSON DeviceConfiguration format',
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='configuration',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[('generic', 'Generic'), ('vpn', 'VPN-client')],
                        db_index=True,
                        default='generic',
                        help_text=(
                            'template type, determines which features are available'
                        ),
                        max_length=16,
                        verbose_name='type',
                    ),
                ),
                (
                    'default',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text=(
                            'whether new configurations will have this '
                            'template enabled by default'
                        ),
                        verbose_name='enabled by default',
                    ),
                ),
                (
                    'required',
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text=(
                            'if checked, will force the assignment of this template to '
                            'all the devices of the organization (if no organization '
                            'is selected, it will be required for every device '
                            'in the system)'
                        ),
                        verbose_name='required',
                    ),
                ),
                (
                    'auto_cert',
                    models.BooleanField(
                        db_index=True,
                        default=default_auto_cert,
                        help_text=(
                            'whether tunnel specific configuration (cryptographic '
                            'keys, ip addresses, etc) should be automatically '
                            'generated and managed behind the scenes for each '
                            'configuration using this template, valid only for '
                            'the VPN type'
                        ),
                        verbose_name='automatic tunnel provisioning',
                    ),
                ),
                (
                    'default_values',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'ensure_ascii': False, 'indent': 4},
                        help_text=(
                            'A dictionary containing the default values for the '
                            'variables used by this template; these default variables '
                            'will be used during schema validation.'
                        ),
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='Default Values',
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'organization',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=swapper.get_model_name('openwisp_users', 'Organization'),
                        verbose_name='organization',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=(
                            'A comma-separated list of template tags, may be used '
                            'to ease auto configuration with specific settings '
                            '(eg: 4G, mesh, WDS, VPN, ecc.)'
                        ),
                        through='sample_config.TaggedTemplate',
                        to='sample_config.TemplateTag',
                        verbose_name='Tags',
                    ),
                ),
                (
                    'vpn',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='sample_config.vpn',
                        verbose_name='VPN',
                    ),
                ),
            ],
            options={
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
                'abstract': False,
                'unique_together': {('organization', 'name')},
            },
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.AddField(
            model_name='taggedtemplate',
            name='tag',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sample_config_taggedtemplate_items',
                to='sample_config.templatetag',
            ),
        ),
        migrations.CreateModel(
            name='OrganizationConfigSettings',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'registration_enabled',
                    models.BooleanField(
                        default=True,
                        help_text=(
                            'Whether automatic registration of '
                            'devices is enabled or not'
                        ),
                        verbose_name='auto-registration enabled',
                    ),
                ),
                (
                    'shared_secret',
                    openwisp_utils.base.KeyField(
                        db_index=True,
                        default=openwisp_utils.utils.get_random_key,
                        help_text='used for automatic registration of devices',
                        max_length=32,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[^\\s/\\.]+$'),
                                code='invalid',
                                message=(
                                    'This value must not contain spaces, '
                                    'dots or slashes.'
                                ),
                            )
                        ],
                        verbose_name='shared secret',
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'organization',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='config_settings',
                        to=swapper.get_model_name('openwisp_users', 'Organization'),
                        verbose_name='organization',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Configuration management settings',
                'verbose_name_plural': 'Configuration management settings',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        db_index=True,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile(
                                    '^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}'
                                    '[a-zA-Z0-9])(\\.([a-zA-Z0-9]|[a-zA-Z0-9]'
                                    '[a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9]))*$|^'
                                    '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
                                ),
                                code='invalid',
                                message=(
                                    'Must be either a valid hostname or mac address.'
                                ),
                            )
                        ],
                        help_text=('must be either a valid hostname or mac address'),
                    ),
                ),
                (
                    'mac_address',
                    models.CharField(
                        db_index=True,
                        help_text='primary mac address',
                        max_length=17,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'),
                                code='invalid',
                                message='Must be a valid mac address.',
                            )
                        ],
                    ),
                ),
                (
                    'key',
                    openwisp_utils.base.KeyField(
                        blank=True,
                        db_index=True,
                        default=None,
                        help_text='unique device key',
                        max_length=64,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[^\\s/\\.]+$'),
                                code='invalid',
                                message=(
                                    'This value must not contain spaces, '
                                    'dots or slashes.'
                                ),
                            )
                        ],
                    ),
                ),
                (
                    'model',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text='device model and manufacturer',
                        max_length=64,
                    ),
                ),
                (
                    'os',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text='operating system identifier',
                        max_length=128,
                        verbose_name='operating system',
                    ),
                ),
                (
                    'system',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        help_text='system on chip or CPU info',
                        max_length=128,
                        verbose_name='SOC / CPU',
                    ),
                ),
                ('notes', models.TextField(blank=True, help_text='internal notes')),
                (
                    'last_ip',
                    models.GenericIPAddressField(
                        blank=True,
                        db_index=True,
                        help_text=(
                            'indicates the IP address logged from the last '
                            'request coming from the device'
                        ),
                        null=True,
                    ),
                ),
                (
                    'management_ip',
                    models.GenericIPAddressField(
                        blank=True,
                        db_index=True,
                        help_text=(
                            'ip address of the management interface, if available'
                        ),
                        null=True,
                    ),
                ),
                (
                    'hardware_id',
                    models.CharField(
                        blank=True,
                        help_text='Serial number of this device',
                        max_length=32,
                        null=True,
                        verbose_name='Serial number',
                    ),
                ),
                ('details', models.CharField(blank=True, max_length=64, null=True)),
                (
                    'organization',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=swapper.get_model_name('openwisp_users', 'Organization'),
                        verbose_name='organization',
                    ),
                ),
            ],
            options={
                'abstract': False,
                'unique_together': {
                    ('mac_address', 'organization'),
                    ('hardware_id', 'organization'),
                },
                'verbose_name': app_settings.DEVICE_VERBOSE_NAME[0],
                'verbose_name_plural': app_settings.DEVICE_VERBOSE_NAME[1],
            },
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.AddField(
            model_name='config',
            name='device',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to='sample_config.device'
            ),
        ),
        migrations.AddField(
            model_name='config',
            name='templates',
            field=openwisp_controller.config.sortedm2m.fields.SortedManyToManyField(
                blank=True,
                help_text='configuration templates, applied from first to last',
                related_name='config_relations',
                to='sample_config.Template',
                verbose_name='templates',
            ),
        ),
        migrations.AddField(
            model_name='config',
            name='vpn',
            field=models.ManyToManyField(
                blank=True,
                related_name='vpn_relations',
                through='sample_config.VpnClient',
                to='sample_config.Vpn',
            ),
        ),
    ]
