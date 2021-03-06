from django.db import models

from django.conf import settings

from opencomap.apps.backend.models.choice import STATUS_TYPES
from decorators import check_status
from managers import Manager


class Project(models.Model):
    """
    Stores a single project. Extends `Authenticatable`.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    isprivate = models.BooleanField(default=False)
    everyonecontributes = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(default=STATUS_TYPES['ACTIVE'])
    admins = models.OneToOneField(
        'backend.UserGroup', related_name='admingroup'
    )
    contributors = models.OneToOneField(
        'backend.UserGroup', related_name='contributorgroup'
    )

    objects = Manager()

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name + ', ' + self.description

    @check_status
    def update(
            self, name=None, description=None, status=None, isprivate=None,
            everyonecontributes=None):
        """
        Updates a project. Checks if the status is of ACTIVE or INACTIVE
        otherwise raises ValidationError.
        """

        if (name):
            self.name = name
        if (description):
            self.description = description
        if (status is not None):
            self.status = status
        if (isprivate is not None):
            self.isprivate = isprivate
        if (everyonecontributes is not None):
            self.everyonecontributes = everyonecontributes

        self.save()

    def delete(self):
        """
        Removes the project from the listing of all projects by setting its
        status to `DELETED`.
        """
        self.status = STATUS_TYPES['DELETED']
        self.save()

    def isViewable(self, user):
        """
        Checks if the user is allowed to view the project.
        """
        can_view = (
            (self.admins.isMember(user)) or
            (
                (not self.isprivate or self.contributors.isMember(user))
                and self.status != STATUS_TYPES['INACTIVE']
            )
        )

        if not can_view:
            for view in self.view_set.all():
                if view.isViewable(user):
                    can_view = True

        return can_view
