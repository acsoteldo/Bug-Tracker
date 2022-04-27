from django.conf import settings
from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify

# from django.contrib.auth.models import User
from django.urls import reverse
from markdown2 import markdown
from taggit.managers import TaggableManager

from .utils import replace_links

LINK_PATTERNS = getattr(settings, "LINK_PATTERNS", None)

# for markdown2 (<h1> becomes <h3>)
DEMOTE_HEADERS = 2


class TicketManager(models.Manager):
    def get_queryset(self):
        # return self.filter(active=True)
        return super(TicketManager, self).get_queryset().filter(active=True)


class CommentManager(models.Manager):
  
    def get_queryset(self):
        # return self.filter(private=False)
        return super(CommentManager, self).get_queryset().filter(private=False)


class Application(models.Model):
 
    id = models.AutoField(primary_key=True)
    application = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
   
        self.slug = slugify(self.application)
        super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return self.application


class Ticket(models.Model):
 
    TICKET_STATUS_CHOICES = [
        ("new", "New"),
        ("accepted", "Accepted"),
        ("assigned", "Assigned"),
        ("re-opened", "Re-Opened"),
        ("closed", "Closed"),
        ("duplicate", "Closed - Duplicate"),
        ("split", "Closed - Split"),
    ]

    TICKET_TYPE_CHOICES = [
        ("feature", "Feature Request"),
        ("bug", "Bug Report"),
        ("task", "Task"),
    ]

    TICKET_PRIORITY_CHOICES = [
        (1, "Critical"),
        (2, "High"),
        (3, "Normal"),
        (4, "Low"),
        (5, "Very Low"),
    ]

    id = models.AutoField(primary_key=True)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        on_delete=models.CASCADE,
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="submitted_tickets",
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=TICKET_STATUS_CHOICES, default=True, db_index=True
    )
    ticket_type = models.CharField(
        max_length=10, choices=TICKET_TYPE_CHOICES, default=True, db_index=True
    )
    title = models.CharField(max_length=80)
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    priority = models.IntegerField(choices=TICKET_PRIORITY_CHOICES, db_index=True)
    created_on = models.DateTimeField("date created", auto_now_add=True)
    updated_on = models.DateTimeField("date updated", auto_now=True)
    votes = models.IntegerField(default=0)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    tags = TaggableManager(blank=True)

    all_tickets = models.Manager()
    objects = TicketManager()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        name = self.description.split("\n", 1)[0]
        name = name[:30]
        return name

    def name(self):
        name = self.description.split("\n", 1)[0]
        name = name[:60]
        return name

    def get_absolute_url(self):
        url = reverse("tickets:ticket_detail", kwargs={"pk": self.id})
        return url

    def save(self, *args, **kwargs):
        self.description_html = markdown(
            self.description, extras={"demote-headers": DEMOTE_HEADERS}
        )
        self.description_html = replace_links(
            self.description_html, link_patterns=LINK_PATTERNS
        )

        super(Ticket, self).save(*args, **kwargs)

    def is_closed(self):
        """a boolean method to indicate if this ticket is open or
        closed.  Makes templating much simpler.
        """
        if self.status in ("closed", "duplicate", "split"):
            return True
        else:
            return False

class FollowUp(models.Model):

    ACTION_CHOICES = [
        ("no_action", "No Action"),
        ("closed", "Closed"),
        ("re-opened", "Re-Opened"),
        ("split", "Split"),
    ]

    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField("date created", auto_now_add=True)
    comment = models.TextField()

    comment_html = models.TextField(editable=False, blank=True)
    # closed = models.BooleanField(default=False)

    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, default="no_action", db_index=True
    )
    private = models.BooleanField(default=False)

    objects = CommentManager()
    all_comments = models.Manager()

    def save(self, *args, **kwargs):
        self.comment_html = markdown(
            self.comment, extras={"demote-headers": DEMOTE_HEADERS}
        )
        self.comment_html = replace_links(
            self.comment_html, link_patterns=LINK_PATTERNS
        )

        super(FollowUp, self).save(*args, **kwargs)


class TicketAdmin(admin.ModelAdmin):
    date_heirarchy = "created_on"
    list_filter = ("status",)
    list_display = ("id", "name", "status", "assigned_to")
    search_field = ["description"]
