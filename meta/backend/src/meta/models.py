from django.db import models


class SMSCode(models.Model):
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=20)

    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.phone, self.code)


class User(models.Model):
    uid = models.CharField(max_length=42, primary_key=True)

    phone = models.CharField(max_length=20, default='')

    name = models.CharField(max_length=100)
    password_hex = models.CharField(max_length=100)

    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    def wechat_user(self):
        return WechatUser.objects.filter(user=self, status=0).first()
    
    def display_name(self):
        return self.name.encode('utf-8').decode('raw_unicode_escape')


class WechatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    union_id = models.CharField(max_length=100, default='')

    nickname = models.CharField(max_length=200, default='')
    head_img = models.CharField(max_length=1000, default='')

    gender = models.IntegerField()
    language = models.CharField(max_length=100, default='')

    country = models.CharField(max_length=100, default='')
    province = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')

    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)


class MiniappUser(models.Model):
    wechat_user = models.ForeignKey(WechatUser, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=100, primary_key=True)


class MiniappTicket(models.Model):
    code = models.CharField(max_length=100)
    union_id = models.CharField(max_length=100)
    open_id = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100)


class Token(models.Model):
    token = models.CharField(max_length=42)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.IntegerField(default=0)

    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)


class PublicAccountUser(models.Model):
    wechat_user = models.ForeignKey(WechatUser, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=100, primary_key=True)


class AccessToken(models.Model):
    appid = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=100, default='')
    access_token = models.CharField(max_length=200, default='')
    expire_time = models.FloatField(default=0)

    openid = models.CharField(max_length=100, default='')
    unionid = models.CharField(max_length=100, default='')


class PublicAccountTicket(models.Model):
    access_token = models.CharField(max_length=200)
    jsapi_ticket = models.CharField(max_length=200)

    expire_time = models.FloatField(default=0)


class Product(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    name = models.CharField(max_length=100)
    price = models.FloatField()

    company = models.CharField(max_length=100)
    category = models.CharField(max_length=100)


class Order(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    price = models.FloatField()


class Payment(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()

