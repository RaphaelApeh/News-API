
class DisAllowAuthMixin:

    def get_permissions(self):
        if any([self.request.user.is_anonymous, self.request.method == "GET"]):
            self.permission_classes = []
        return super().get_permissions()
