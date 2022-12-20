from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



 class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)


    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRate = 0
        pRate += post_rating.get('postRating')

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRate = 0
        cRate += comment_rating.get('commentRating')

        self.authorRating = pRate * 3 + cRate
        self.save()




class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)



 class Post(models.Model):

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
         (NEWS, 'Новость'),
         (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()



    def preview(self):
        return self.text[0:124] + '...'


 class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



 class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.author.username

    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()

