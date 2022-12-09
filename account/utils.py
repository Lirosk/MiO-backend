class RedirectsForEmails:
    container = {}

    @classmethod
    def set_redirect_url(cls, email, redirect_to):
        cls.container[email] = redirect_to
    
    @classmethod
    def get_redirect_url(cls, email):
        return cls.container.get(email)