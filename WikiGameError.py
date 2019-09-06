class WikiGameError(Exception):
    """Make my own Error"""
    def __init__(self, message):
        super(WikiGameError, self).__init__(message)