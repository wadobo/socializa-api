from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry


class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s')
    position = models.PointField(null=True, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, email, password):
        user = User.objects.create_user(email, email, password)
        user.save()
        player = cls(user=user)
        player.save()
        return player

    def set_position(self, lon=None, lat=None):
        if lon is None and lat is None:
            self.position = None
        else:
            self.position = GEOSGeometry('POINT({0} {1})'.format(lon, lat))
        self.save()

    def get_position(self):
        return self.position.coords if self.pos else '(None, None)'

    def __str__(self):
        return self.user.username


class PlayerCharacter(Character):
    pass


class NonPlayerCharacter(Character):
    pass
