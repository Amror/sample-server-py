class User:
    """A class that represents a website user"""

    def __init__(self,
                username,
                email,
                creation_date,
                ratings):
        self.username = username
        self.email = email
        self.creation_date = creation_date
        self.ratings = ratings

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.creation_date}, {self.ratings})'