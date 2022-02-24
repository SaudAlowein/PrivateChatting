from django.db import models
from django.conf import settings
from django.utils import timezone
from chat.utils import find_or_create_private_chat

# Create your models here.
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            chat = find_or_create_private_chat(self.user, account)
            if not chat.is_active:
                chat.is_active = True
                chat.save()

    def remove_friend(self, account):
        """Remove a friend"""

        if account in self.friends.all():
            self.friends.remove(account)
            chat = find_or_create_private_chat(self.user, account)
            if chat.is_active:
                chat.is_active = False
                chat.save()

    def unfriend(self, removee):
        """Initiate the action if unfrending someone"""

        remover_friends_list = self # person terminating the friendship
        remover_friends_list.remove_friend(removee) # removes the friend from the friends list
        # removes the user who intiated the removing process from the removee's friends list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """Is this a friend"""

        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """A friend request consists of two parts
        1- SENDER
        2- Receiver"""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """Accept a friend request. Updates the friends list of both the sender and receiver."""

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """Decline a friend request. It is declined by setting the is_active field to False"""

        self.is_active = False
        self.save()

    def cancel(self):
        """Sender cancels the sent friend request. It is done by setting the is_active field to false"""
        self.is_active = False
        self.save()