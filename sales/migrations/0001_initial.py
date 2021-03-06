# Generated by Django 4.0 on 2022-01-01 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('manufacturing_cost', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Manufacturing Cost')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255, verbose_name='Display name')),
            ],
            options={
                'verbose_name': 'Article Category',
                'verbose_name_plural': 'Article Categories',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('unit_selling_price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Unit selling price')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='sales.article', verbose_name='Article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='users.user', verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='sales.articlecategory', verbose_name='Category'),
        ),
    ]
