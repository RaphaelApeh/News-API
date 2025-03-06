
class DisAllowAuthMixin:
    def get_authenticators(self):
        if self.request.method == "GET":
            self.authentication_classes = []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()
