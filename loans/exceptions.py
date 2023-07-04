class ImpossibleLoan(Exception):
    def __init__(self, message="Impossible to make loan due to late return"):
        self.message = message
