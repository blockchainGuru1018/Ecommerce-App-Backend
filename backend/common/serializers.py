from fcm_django.models import FCMDevice
from django.core.mail import send_mail


def Following_Notification(followed, follower, pk):
    available = followed.push_notification_enabled
    devices = FCMDevice.objects.filter(user=followed)
    if devices and available:
        for device in devices:
            if pk == 0:
                device.send_message(title="Unfollowing", body=follower.name + " unfollowed You",
                                    data={"followed_id": follower.id})
            else:
                device.send_message(title="Following", body=follower.name + " followed You",
                                    data={"followed_id": follower.id})
    else:
        pass


def Following_mail(followed, follower, pk):
    available = followed.email_notification_enabled
    if available:
        if pk == 0:
            send_mail(
                'Unfollowing',
                follower.name + ' unfollowed You',
                'no-reply@unboxxen.com',
                [followed.email]
            )
        else:
            send_mail(
                'Following',
                follower.name + ' followed You',
                'no-reply@unboxxen.com',
                [followed.email]
            )
    else:
        pass


def Favorite_Notification(seller, buyer, pk, id):
    available = seller.push_notification_enabled
    devices = FCMDevice.objects.filter(user=seller)
    if devices and available:
        for device in devices:
            if pk == 1:
                device.send_message(title="Favorite", body=buyer.name + " favorite Your Product",
                                    data={"favorite_id": id})
            else:
                device.send_message(title="Unfavorite", body=buyer.name + " unfavorite Your Product",
                                    data={"favorite_id": id})
    else:
        pass


def Favorite_mail(seller, buyer, pk):
    available = seller.email_notification_enabled
    if available:
        if pk == 1:
            send_mail(
                'Favorite',
                buyer.name + " favorite Your Product",
                'no-reply@unboxxen.com',
                [seller.email]
            )
        else:
            send_mail(
                'Unfavorite',
                buyer.name + " unfavorite Your Product",
                'no-reply@unboxxen.com',
                [seller.email]
            )
    else:
        pass


def ProductCheckout_Notification(seller, buyer, product, label_url):
    available = seller.push_notification_enabled
    devices = FCMDevice.objects.filter(user=seller)
    if devices and available:
        for device in devices:
            device.send_message(title=product.title, body=" Your Product was sold by " + buyer.name +
                                                             " carrier will be arrived here soon." + label_url,
                                data={"checkout_id": product.id})
    else:
        pass


def ProductCheckout_mail(seller, buyer, productname, label_url):
    available = seller.email_notification_enabled
    if available:
        send_mail(
            productname,
            'Your Product was buyed by ' + buyer.name + '. carrier will be arrived here soon.' + label_url,
            'no-reply@unboxxen.com',
            [seller.email]
        )
    else:
        pass


def Confirm_Notification(seller, buyer, product):
    available = seller.push_notification_enabled
    devices = FCMDevice.objects.filter(user=seller)
    if devices and available:
        for device in devices:
            device.send_message(title=product.title, body=buyer.name + " paid for your product",
                                data={"confirm_id": product.id})
    else:
        pass


def Confirm_mail(seller, buyer, productname):
    available = seller.email_notification_enabled
    if available:
        send_mail(
            productname,
            buyer.name + ' paid for your product.',
            'no-reply@unboxxen.com',
            [seller.email]
        )
    else:
        pass


def ProductArrive_Notification(buyer, product):
    available = buyer.push_notification_enabled

    devices = FCMDevice.objects.filter(user=buyer)
    if devices and available:
        for device in devices:
            device.send_message(title=product.title, body=" Product arrived.", data={"arrive_id": product.id})
    else:
        pass


def ProductArrive_mail(buyer, productname):
    available = buyer.email_notification_enabled
    if available:
        send_mail(
            productname,
            'Product arrived.',
            'no-reply@unboxxen.com',
            [buyer.email]
        )
    else:
        pass


def ItemRequest_Notification(seller, buyer, Item):
    available = seller.push_notification_enabled

    devices = FCMDevice.objects.filter(user=seller)
    if devices and available:
        for device in devices:
            device.send_message(title="You have a item request",
                                body=buyer.name + " has sent you an item request," + Item.title +
                                      ",      Offer:" + str(Item.price) + "$",
                                data={"product_id": Item.id})
    else:
        pass


def ItemRequest_mail(seller, buyer, Item):
    available = seller.email_notification_enabled
    if available:
        send_mail(
            'You have a item request',
            buyer.name + ' has sent you an item request,' + Item.title + ',      Offer:' + str(Item.price) + '$',
            'no-reply@unboxxen.com',
            [seller.email]
        )
    else:
        pass


def Accept_Notification(seller, buyer, id):
    available = buyer.push_notification_enabled

    devices = FCMDevice.objects.filter(user=buyer)
    if devices and available:
        for device in devices:
            device.send_message(title="Your Item Request Accepted",
                                body=seller.name + ", has fulfilled your item request!",
                                data={"accept_id": id})
    else:
        pass


def Accept_mail(seller, buyer):
    available = buyer.email_notification_enabled
    if available:
        send_mail(
            'Your Item Request Accepted',
            seller.name + ', has fulfilled your item request!',
            'no-reply@unboxxen.com',
            [buyer.email]
        )
    else:
        pass


def serialize_featuring(product, is_favorite):
    return {
        "product_id": product.id,
        "title": product.title,
        "price": product.price,
        "currency": product.currency,
        "time": product.time,
        "favorite": is_favorite,
    }


