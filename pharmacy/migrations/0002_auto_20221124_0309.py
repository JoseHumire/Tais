# Generated by Django 3.2.6 on 2022-11-24 00:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Medicamento'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'AdminHOD')], default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='descripcion'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_imprint',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='codigo'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_pic',
            field=models.ImageField(blank=True, default='images2.png', null=True, upload_to='', verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_shape',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='forma'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='drug_strength',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='potencia'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='actualizado'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='manufacture',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='fabricante'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='cantidad'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='marca de tiempo'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='valid_from',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='valido desde'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='valid_to',
            field=models.DateTimeField(null=True, verbose_name='valido hasta'),
        ),
    ]
