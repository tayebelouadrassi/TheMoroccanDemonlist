from django.db import models
from player.models import Player
from level.models import ClassicLevel, PlatformerLevel
from django.core.validators import MaxValueValidator
from datetime import timedelta
import uuid

# Create your models here.

class RecordSubmission(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Approved', 'Approved'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    record_link = models.URLField()
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        abstract = True

class ClassicRecordSubmission(RecordSubmission):
    level = models.ForeignKey(ClassicLevel, on_delete=models.CASCADE)
    record_percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name = "Classic Record Submission"
        verbose_name_plural = "Classic Record Submissions"

class PlatformerRecordSubmission(RecordSubmission):
    level = models.ForeignKey(PlatformerLevel, on_delete=models.CASCADE)
    record_time = models.DurationField()

    class Meta:
        verbose_name = "Platformer Record Submission"
        verbose_name_plural = "Platformer Record Submissions"