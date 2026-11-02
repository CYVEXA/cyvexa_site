from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Workshop', 'Workshop'),
        ('Webinar', 'Webinar'),
        ('Training Program', 'Training Program'),
        ('Celebration', 'Celebration'),
        ('Conference', 'Conference'),
        ('Meetup', 'Meetup'),
    ]

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time_info = models.CharField(max_length=100, default='7:00 PM – 8:30 PM IST', blank=True)

    location = models.CharField(max_length=200, default='Online', blank=True)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='online', blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='Workshop', blank=True)
    tags = models.CharField(max_length=255, default='', blank=True, help_text="Comma-separated tags e.g. Cybersecurity, Zero Trust, Threat Detection")
    registration_link = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return self.title

    @property
    def status(self):
        from django.utils import timezone
        today = timezone.now().date()
        if self.start_date > today:
            return 'Upcoming'
        elif self.end_date and self.end_date < today:
            return 'Completed'
        elif not self.end_date and self.start_date < today:
            return 'Completed'
        else:
            return 'Ongoing'

    @property
    def display_location(self):
        loc = (self.location or 'Online').strip()
        m = (self.mode or ('online' if 'online' in loc.lower() else 'offline')).strip().lower()
        if m in loc.lower():
            return loc
        return f"{loc} · {m}"

    @property
    def tag_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        # Smart contextual fallback tags based on title and event_type
        t = self.title.lower()
        if 'marketing' in t or 'seo' in t:
            return ['Digital Marketing', 'SEO', 'Google Ads', 'Strategy', 'Growth']
        elif 'iot' in t or 'edge' in t or 'sensor' in t:
            return ['IoT', 'Edge Computing', 'Sensors', 'Embedded', 'Hardware']
        elif 'security' in t or 'cyber' in t or 'threat' in t:
            return ['Cybersecurity', 'Zero Trust', 'Threat Detection', 'InfoSec']
        elif 'vapt' in t or 'penetration' in t or 'hacking' in t:
            return ['Ethical Hacking', 'VAPT', 'Network Security']
        elif 'women' in t or 'celebration' in t:
            return ['Celebration', 'Culture', 'Community']
        elif 'factory' in t or 'manufacturing' in t:
            return ['Smart Factory', 'Industry 4.0', 'Automation']
        elif 'bootcamp' in t or 'web' in t:
            return ['Web Dev', 'Frontend', 'Backend', 'Fullstack']
        elif 'ai' in t or 'machine learning' in t:
            return ['AI', 'Machine Learning', 'Data Science']
        return [self.event_type or 'Workshop', 'Tech']

    @property
    def primary_tags(self):
        # returns first 3 tags
        return self.tag_list[:3]

    @property
    def extra_tags_count(self):
        total = len(self.tag_list)
        return total - 3 if total > 3 else 0