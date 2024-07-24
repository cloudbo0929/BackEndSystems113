# Generated by Django 5.1 on 2024-09-14 14:46

import backendApp.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ActionType",
            fields=[
                ("action_type_id", models.AutoField(primary_key=True, serialize=False)),
                ("action_type_name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="MealOrderTimeSlot",
            fields=[
                ("timeSlot_id", models.AutoField(primary_key=True, serialize=False)),
                ("timeSlot_name", models.CharField(max_length=3)),
                ("startTime", models.TimeField(default="00:00")),
                ("deadlineTime", models.TimeField(default="00:00")),
                ("endTimes", models.TimeField(default="00:00")),
            ],
        ),
        migrations.CreateModel(
            name="MedicineDemandState",
            fields=[
                (
                    "medicineDemandState_code",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("medicineState_name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Notify",
            fields=[
                ("notify_id", models.AutoField(primary_key=True, serialize=False)),
                ("notify_message", models.CharField(max_length=1000)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderState",
            fields=[
                (
                    "order_state_code",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("order_state_name", models.CharField(max_length=10)),
                ("order_state_html_style", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("patient_id", models.AutoField(primary_key=True, serialize=False)),
                ("patient_name", models.CharField(max_length=45)),
                ("patient_birth", models.DateField()),
                ("patient_number", models.CharField(max_length=10)),
                ("patient_idcard", models.CharField(max_length=10)),
                (
                    "line_notify",
                    models.CharField(blank=True, max_length=45, null=True, unique=True),
                ),
                (
                    "line_id",
                    models.CharField(blank=True, max_length=45, null=True, unique=True),
                ),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                ("purchase_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sides",
            fields=[
                ("sides_id", models.AutoField(primary_key=True, serialize=False)),
                ("sides_name", models.CharField(max_length=45)),
                ("sides_unit", models.CharField(max_length=45)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("supplier_id", models.AutoField(primary_key=True, serialize=False)),
                ("supplier_name", models.CharField(max_length=45)),
                (
                    "supplier_number",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("line_notify", models.CharField(blank=True, max_length=45, null=True)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                ("vehicle_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleStatus",
            fields=[
                (
                    "vehicle_status_code",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("vehicle_status_name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="MainCourse",
            fields=[
                ("course_id", models.AutoField(primary_key=True, serialize=False)),
                ("course_name", models.CharField(max_length=45)),
                ("course_price", models.IntegerField()),
                (
                    "course_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=backendApp.models.course_image_upload_to,
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "timeSlot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.mealordertimeslot",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicineDemand",
            fields=[
                (
                    "medicineDemand_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("patient_demand", models.CharField(max_length=300)),
                ("review_time", models.DateTimeField(blank=True, null=True)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "medicineDemandState",
                    models.ForeignKey(
                        db_column="medicineDemandState_code",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.medicinedemandstate",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChatLogs",
            fields=[
                ("chatLog_id", models.AutoField(primary_key=True, serialize=False)),
                ("patient_message", models.CharField(max_length=1000)),
                ("response_message", models.CharField(max_length=1000)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bed",
            fields=[
                ("bed_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "bed_number",
                    models.CharField(blank=True, max_length=5, null=True, unique=True),
                ),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PatientNotifys",
            fields=[
                (
                    "patientNotifys_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("is_read", models.BooleanField(default=False)),
                (
                    "notify",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.notify",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QRCodePoint",
            fields=[
                ("qr_id", models.AutoField(primary_key=True, serialize=False)),
                ("location_name", models.CharField(max_length=100)),
                (
                    "action_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.actiontype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("order_id", models.AutoField(primary_key=True, serialize=False)),
                ("order_quantity", models.IntegerField()),
                ("order_time", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        db_column="course_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.maincourse",
                    ),
                ),
                (
                    "order_state",
                    models.ForeignKey(
                        db_column="order_state_code",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.orderstate",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.patient",
                    ),
                ),
                (
                    "delivery_location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.qrcodepoint",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RfidCard",
            fields=[
                (
                    "rfidCard_code",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseDetail",
            fields=[
                (
                    "purchase_detail_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("purchase_quantity", models.IntegerField()),
                ("purchase_date", models.DateTimeField()),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        db_column="purchase_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.purchase",
                    ),
                ),
                (
                    "sides",
                    models.ForeignKey(
                        db_column="sides_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.sides",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourseSides",
            fields=[
                ("coursesides_id", models.AutoField(primary_key=True, serialize=False)),
                ("quantity", models.IntegerField()),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "course",
                    models.ForeignKey(
                        db_column="course_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_sides",
                        to="backendApp.maincourse",
                    ),
                ),
                (
                    "sides",
                    models.ForeignKey(
                        db_column="sides_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.sides",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StopPoint",
            fields=[
                ("stop_point_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "qr_point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.qrcodepoint",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="purchase",
            name="supplier",
            field=models.ForeignKey(
                db_column="supplier_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="backendApp.supplier",
            ),
        ),
        migrations.CreateModel(
            name="TurnPoint",
            fields=[
                ("turn_point_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "qr_point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.qrcodepoint",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RouteCondition",
            fields=[
                (
                    "route_condition_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "stop_point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.stoppoint",
                    ),
                ),
                (
                    "turn_point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backendApp.turnpoint",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryAssignment",
            fields=[
                ("assignment_id", models.AutoField(primary_key=True, serialize=False)),
                ("assigned_time", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_assignments",
                        to="backendApp.order",
                    ),
                ),
                (
                    "current_location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backendApp.qrcodepoint",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_assignments",
                        to="backendApp.vehicle",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="vehicle",
            name="vehicle_status",
            field=models.ForeignKey(
                db_column="vehicle_status_code",
                on_delete=django.db.models.deletion.CASCADE,
                to="backendApp.vehiclestatus",
            ),
        ),
    ]
