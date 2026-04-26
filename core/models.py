from django.db import models
from django.contrib.auth.models import User

DESIGNATION_CHOICES = [
    ('professor', 'Professor'),
    ('associate_professor', 'Associate Professor'),
    ('assistant_professor', 'Assistant Professor'),
    ('lecturer', 'Lecturer'),
]

DEPARTMENT_CHOICES = [
    ('cs', 'Computer Science'),
    ('ec', 'Electronics'),
    ('me', 'Mechanical'),
    ('ce', 'Civil'),
    ('it', 'Information Technology'),
]

MONTH_CHOICES = [
    (1,'January'),(2,'February'),(3,'March'),(4,'April'),
    (5,'May'),(6,'June'),(7,'July'),(8,'August'),
    (9,'September'),(10,'October'),(11,'November'),(12,'December'),
]

TYPE_CHOICES = [
    ('journal', 'Journal'),
    ('conference', 'Conference'),
    ('book', 'Book'),
    ('book_chapter', 'Book Chapter'),
]


class Faculty(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(
        max_length=50, choices=DESIGNATION_CHOICES
    )
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES
    )
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.get_department_display()})"


class Publication(models.Model):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE,
        related_name='publications'
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=300)
    month = models.IntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    year = models.IntegerField()
    pages = models.CharField(max_length=50, blank=True)
    pdf_file = models.FileField(
        upload_to='publications/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Journal fields
    journal_name = models.CharField(max_length=300, blank=True)
    issn = models.CharField(max_length=50, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)

    # Conference fields
    conference_name = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=255, blank=True)
    conference_isbn = models.CharField(max_length=50, blank=True)

    # Book / Book Chapter fields
    book_name = models.CharField(max_length=300, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    book_isbn = models.CharField(max_length=50, blank=True)
    chapter_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"