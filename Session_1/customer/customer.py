class Customer:
    """
    A Customer class representing a customer with basic information and credit account functionality.
    
    This class manages customer data including name, email, phone, and optional credit account
    with balance tracking and modification capabilities.
    
    Attributes:
        name (str): The customer's full name
        email (str): The customer's email address
        phone (str): The customer's phone number
        credit (float, optional): The customer's credit balance (only exists after creating credit account)
    """
    
    def __init__(self, name, email, phone):
        """
        Initialize a new Customer instance.
        
        Args:
            name (str): The customer's full name
            email (str): The customer's email address
            phone (str): The customer's phone number
        """
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        """
        Return a string representation of the Customer.
        
        Returns:
            str: A formatted string containing name, email, and phone
        """
        return f"{self.name} - {self.email} - {self.phone}"

    def has_credit_account(self):
        """
        Check if the customer has a credit account.
        
        Returns:
            bool: True if the customer has a credit account, False otherwise
        """
        return hasattr(self, 'credit')

    def create_credit_account(self):
        """
        Create a new credit account for the customer with zero balance.
        
        If the customer already has a credit account, this method will not create
        a new one and will return False.
        
        Returns:
            bool: True if credit account was created successfully, False if customer
                  already has a credit account
        """
        if self.has_credit_account():
            print("Customer already has a credit account")
            return False
        else:
            self.credit = 0
            print("Credit account created")
            return True

    def modify_credit(self, amount: float):
        """
        Modify the customer's credit balance by adding the specified amount.
        
        This method can add or subtract credit (use negative amounts to subtract).
        The customer must have a credit account before this method can be used.
        
        Args:
            amount (float): The amount to add to the credit balance. Use negative
                          values to subtract from the balance.
        
        Returns:
            bool: True if credit was modified successfully, False if customer
                  does not have a credit account
        """
        if self.has_credit_account():
            self.credit += amount
            print(f"Credit modified by {amount} to {self.credit}")
            return True
        else:
            print("Customer does not have a credit account")
            return False
