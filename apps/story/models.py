from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Project(models.Model):
    title = models.CharField(max_length=255)
    fk_organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE, blank=True, related_name="org_projects")

    def __str__(self):
        return '%s' % self.title

class Story(models.Model):
    fk_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="versions", null=True)
    title = models.CharField(max_length=255)
    # url = models.URLField()
    description = models.TextField(null=True)
    number_of_votes = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, related_name='stories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_git_versioning = models.BooleanField(default=True, null=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return '%s' % self.title

class Vote(models.Model):
    story = models.ForeignKey(Story, related_name='votes', on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.story.number_of_votes = self.story.number_of_votes + 1
        self.story.save()

        super(Vote, self).save(*args, **kwargs)

class Comment(models.Model):
    story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)

    body = models.TextField()

    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']