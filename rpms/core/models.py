from django.db import models
from django.contrib.auth.models import User


TYPE_CHOICES = [
    ('journal', 'Journal'),
    ('conference', 'Conference'),
    ('book', 'Book'),
    ('book_chapter', 'Book Chapter'),
]

INDEXED_CHOICES = [
    ('SCOPUS', 'SCOPUS'),
    ('WOS', 'WOS'),
    ('WOS-SCI', 'WOS-SCI'),
    ('WOS-ESCI', 'WOS-ESCI'),
]

QUARTILE_CHOICES = [
    ('Q1', 'Q1'),
    ('Q2', 'Q2'),
    ('Q3', 'Q3'),
    ('Q4', 'Q4'),
]

YEAR_CHOICES = [(y, str(y)) for y in range(2018, 2025)]


class Faculty(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name


class Publication(models.Model):
    sl_no = models.AutoField(primary_key=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE,
        related_name='publications'
    )
    faculty_name = models.CharField(max_length=200, help_text='Name of the faculty')
    title = models.CharField(max_length=500, help_text='Title of the paper')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES,
        default='journal', help_text='Publication type'
    )
    journal_conference = models.CharField(
        max_length=500, help_text='Name of the Journal/Conference'
    )
    page_no = models.CharField(max_length=100, blank=True, help_text='Page number')
    vol_issue = models.CharField(max_length=100, blank=True, help_text='Vol.No/Issue No')
    year = models.IntegerField(help_text='Publication year (2018-2024)')
    doi = models.CharField(max_length=300, blank=True, help_text='DOI identifier')
    indexed = models.CharField(
        max_length=20, choices=INDEXED_CHOICES,
        help_text='Indexing type'
    )
    quartile = models.CharField(
        max_length=5, choices=QUARTILE_CHOICES,
        blank=True, help_text='Journal quartile'
    )
    pdf_file = models.FileField(
        upload_to='publications/', blank=True, null=True,
        help_text='Upload PDF file'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-created_at']

    def __str__(self):
        return f"{self.sl_no}. {self.title}"

    def doi_url(self):
        if self.doi:
            if self.doi.startswith('http'):
                return self.doi
            return f"https://doi.org/{self.doi}"
        return ''