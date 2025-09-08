from customer import Customer

def main():
    print("=" * 60)
    print("CUSTOMER CLASS TEST SCRIPT")
    print("=" * 60)
    
    # Test 1: Create a new customer
    print("\n1. CREATING A NEW CUSTOMER")
    print("-" * 30)
    customer = Customer("John Doe", "john.doe@example.com", "1234567890")
    print(f"Created customer: {customer}")
    
    # Test 2: Check if customer has credit account (should be False initially)
    print("\n2. CHECKING CREDIT ACCOUNT STATUS")
    print("-" * 30)
    has_credit = customer.has_credit_account()
    print(f"Customer has credit account: {has_credit}")
    
    # Test 3: Try to modify credit without having an account (should fail)
    print("\n3. ATTEMPTING TO MODIFY CREDIT WITHOUT ACCOUNT")
    print("-" * 30)
    result = customer.modify_credit(100)
    print(f"Modify credit result: {result}")
    
    # Test 4: Create a credit account
    print("\n4. CREATING CREDIT ACCOUNT")
    print("-" * 30)
    create_result = customer.create_credit_account()
    print(f"Create credit account result: {create_result}")
    
    # Test 5: Check credit account status again (should be True now)
    print("\n5. CHECKING CREDIT ACCOUNT STATUS AFTER CREATION")
    print("-" * 30)
    has_credit = customer.has_credit_account()
    print(f"Customer has credit account: {has_credit}")
    
    # Test 6: Modify credit (should work now)
    print("\n6. MODIFYING CREDIT (ADDING 100)")
    print("-" * 30)
    result = customer.modify_credit(100)
    print(f"Modify credit result: {result}")
    print(f"Current credit balance: {customer.credit}")
    
    # Test 7: Add more credit
    print("\n7. ADDING MORE CREDIT (50)")
    print("-" * 30)
    result = customer.modify_credit(50)
    print(f"Modify credit result: {result}")
    print(f"Current credit balance: {customer.credit}")
    
    # Test 8: Subtract credit (negative amount)
    print("\n8. SUBTRACTING CREDIT (-25)")
    print("-" * 30)
    result = customer.modify_credit(-25)
    print(f"Modify credit result: {result}")
    print(f"Current credit balance: {customer.credit}")
    
    # Test 9: Create another customer to test multiple instances
    print("\n9. TESTING MULTIPLE CUSTOMER INSTANCES")
    print("-" * 30)
    customer2 = Customer("Jane Smith", "jane.smith@example.com", "0987654321")
    print(f"Created second customer: {customer2}")
    print(f"Second customer has credit account: {customer2.has_credit_account()}")
    
    # Test 10: Test edge case - modify credit on customer without account
    print("\n10. TESTING EDGE CASE - MODIFY CREDIT ON CUSTOMER WITHOUT ACCOUNT")
    print("-" * 30)
    result = customer2.modify_credit(200)
    print(f"Modify credit result: {result}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()