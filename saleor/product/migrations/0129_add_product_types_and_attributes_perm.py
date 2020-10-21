# Generated by Django 3.1 on 2020-10-16 09:16

from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def update_groups_with_manage_products_with_new_permission(apps, schema_editor):
    # force post signal as permissions are created in post migrate signals
    # related Django issue https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(2, False, "default")

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    product_type_and_attribute_permission = Permission.objects.filter(
        codename="manage_product_types_and_attributes",
        content_type__app_label="product",
    ).first()

    groups = Group.objects.filter(
        permissions__content_type__app_label="product",
        permissions__codename="manage_products",
    )
    for group in groups:
        group.permissions.add(product_type_and_attribute_permission)


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0128_update_publication_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="producttype",
            options={
                "ordering": ("slug",),
                "permissions": (
                    (
                        "manage_product_types_and_attributes",
                        "Manage product types and attributes.",
                    ),
                ),
            },
        ),
        migrations.RunPython(
            update_groups_with_manage_products_with_new_permission,
            migrations.RunPython.noop,
        ),
    ]