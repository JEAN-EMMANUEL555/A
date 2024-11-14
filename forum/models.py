from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Modèle UserProfile pour étendre le modèle utilisateur par défaut


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',
                                        blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Modèle Post pour les publications des utilisateurs


class Post(models.Model):
    title = models.CharField(max_length=255, default="Sans titre")
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.user.username} on {self.created_at}"

# Modèle Commentaire pour les commentaires sous chaque post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.created_at}"

# Modèle Like pour enregistrer les "J'aime" pour les posts et les commentaires


class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(
          Post, on_delete=models.CASCADE, related_name='likes', null=True,
          blank=True
        )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post', 'comment')

    def __str__(self):
        target = self.post if self.post else self.comment
        return f"Like by {self.user.user.username} on {target}"
