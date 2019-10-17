class messagebody:
    """A template message format that can be used for simpler communication between processes."""

    def __init__(self, target_id, sender_id, message):
        self.target_id = target_id
        self.sender_id = sender_id
        self.message = message

