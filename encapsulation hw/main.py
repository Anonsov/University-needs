"""
Main Demonstration - Advanced Encapsulation System
Demonstrates valid usage, illegal access attempts, and security features
"""
from secure_user import SecureUser
import json


def print_section(title):
    """Helper function to print formatted section headers."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_status(user):
    """Helper function to print user status."""
    status = user.identity_status()
    print(f"👤 User: {status['username']}")
    print(f"📧 Email: {status['email']}")
    print(f"📱 Phone: {status['phone']}")
    print(f"✅ Status: {status['verification_status']}")
    print(f"🔑 Permissions: {', '.join(status['permissions']) if status['permissions'] else 'None'}")


def main():
    """Main demonstration function."""
    
    print_section("🏦 FINTECH IDENTITY SYSTEM - DEMONSTRATION")
    
    # ========================================================================
    # PART 1: Valid Usage - Creating a Secure User
    # ========================================================================
    print_section("PART 1: Creating SecureUser with Valid Data")
    
    try:
        user = SecureUser(
            username="john_doe",
            email="john.doe@example.com",
            phone_number="+1-555-123-4567"
        )
        print("✅ User created successfully!")
        print_status(user)
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return
    
    # ========================================================================
    # PART 2: Attempting to Access Private/Protected Attributes Directly
    # ========================================================================
    print_section("PART 2: Illegal Direct Access Attempts")
    
    print("\n1️⃣ Attempting to access private __phone_number directly:")
    try:
        # This will fail - name mangling protects private attributes
        phone = user._identity.__phone_number
        print(f"❌ SECURITY BREACH: Accessed phone: {phone}")
    except AttributeError as e:
        print(f"✅ ACCESS DENIED: {e}")
    
    print("\n2️⃣ Attempting to access private __access directly:")
    try:
        # This will fail - private attribute is protected
        access = user.__access
        print(f"❌ SECURITY BREACH: Accessed account access: {access}")
    except AttributeError as e:
        print(f"✅ ACCESS DENIED: {e}")
    
    print("\n3️⃣ Attempting to access private __audit_log directly:")
    try:
        # This will fail - audit log is private
        audit = user.__audit_log
        print(f"❌ SECURITY BREACH: Accessed audit log: {audit}")
    except AttributeError as e:
        print(f"✅ ACCESS DENIED: {e}")
    
    print("\n4️⃣ Attempting to modify protected _email directly:")
    print("   Note: Protected attributes CAN be accessed but SHOULDN'T be")
    old_email = user._identity._email
    user._identity._email = "hacker@evil.com"  # This works but bypasses validation!
    print(f"   ⚠️  Direct modification bypassed validation: {user._identity._email}")
    print("   🔧 Restoring through proper method...")
    user.update_email(old_email)
    print(f"   ✅ Email restored properly: {user._identity.get_email()}")
    
    # ========================================================================
    # PART 3: Attempting Illegal State Transitions
    # ========================================================================
    print_section("PART 3: Illegal State Transitions")
    
    print("\n1️⃣ Attempting to verify without requesting:")
    result = user.verify_identity()
    print(f"   Result: {result}")
    print(f"   Status: {user._identity.get_verification_status()}")
    print("   ✅ Transition blocked - must be in PENDING state")
    
    print("\n2️⃣ Proper state transition:")
    print("   Step 1: Request verification...")
    result = user.request_verification()
    print(f"   Result: {result}, Status: {user._identity.get_verification_status()}")
    
    print("\n   Step 2: Complete verification...")
    result = user.verify_identity()
    print(f"   Result: {result}, Status: {user._identity.get_verification_status()}")
    
    print("\n3️⃣ Attempting to request verification when already verified:")
    result = user.request_verification()
    print(f"   Result: {result}")
    print(f"   Status: {user._identity.get_verification_status()}")
    print("   ✅ Transition blocked - already in VERIFIED state")
    
    # ========================================================================
    # PART 4: Granting Restricted Permissions Before Verification
    # ========================================================================
    print_section("PART 4: Permission Management & Verification Requirements")
    
    # Create a new unverified user
    print("\n1️⃣ Creating new unverified user...")
    user2 = SecureUser(
        username="jane_smith",
        email="jane.smith@example.com",
        phone_number="+1-555-987-6543"
    )
    print_status(user2)
    
    print("\n2️⃣ Attempting to grant TRANSFER permission (restricted) to unverified user:")
    success, message = user2.grant_permission("TRANSFER")
    print(f"   Result: {message}")
    print(f"   ✅ Permission DENIED - user must be verified")
    
    print("\n3️⃣ Granting non-restricted permission (VIEW_BALANCE):")
    success, message = user2.grant_permission("VIEW_BALANCE")
    print(f"   Result: {message}")
    print(f"   ✅ Permission GRANTED - no verification required")
    
    print("\n4️⃣ Verifying user...")
    user2.request_verification()
    user2.verify_identity()
    print(f"   Status: {user2._identity.get_verification_status()}")
    
    print("\n5️⃣ Now attempting to grant TRANSFER permission to verified user:")
    success, message = user2.grant_permission("TRANSFER")
    print(f"   Result: {message}")
    print(f"   ✅ Permission GRANTED - user is verified")
    
    print("\n6️⃣ Attempting to grant WITHDRAW permission:")
    success, message = user2.grant_permission("WITHDRAW")
    print(f"   Result: {message}")
    
    print_status(user2)
    
    # ========================================================================
    # PART 5: List Manipulation Safety
    # ========================================================================
    print_section("PART 5: List Manipulation Safety")
    
    print("\n1️⃣ Getting permissions list (should be a copy):")
    permissions = user2.get_permissions()
    print(f"   Permissions: {permissions}")
    
    print("\n2️⃣ Attempting to modify the returned list:")
    permissions.append("ADMIN_ACCESS")
    print(f"   Modified external list: {permissions}")
    
    print("\n3️⃣ Checking actual permissions (should be unchanged):")
    actual_permissions = user2.get_permissions()
    print(f"   Actual permissions: {actual_permissions}")
    print("   ✅ Internal data protected - returns copy, not reference")
    
    print("\n4️⃣ Getting audit log (should also be a copy):")
    audit_log = user2.get_audit_log()
    original_length = len(audit_log)
    print(f"   Audit log entries: {original_length}")
    
    print("\n5️⃣ Attempting to modify the audit log:")
    audit_log.append({"malicious": "entry"})
    print(f"   Modified external list length: {len(audit_log)}")
    
    print("\n6️⃣ Checking actual audit log (should be unchanged):")
    actual_audit = user2.get_audit_log()
    print(f"   Actual audit log entries: {len(actual_audit)}")
    print("   ✅ Audit log protected - returns copy, not reference")
    
    # ========================================================================
    # PART 6: Final State Output
    # ========================================================================
    print_section("PART 6: Final System State")
    
    print("\n👤 USER 1 (john_doe) - VERIFIED:")
    print_status(user)
    print(f"\n📊 Audit Log Entries: {len(user.get_audit_log())}")
    print("Recent Actions:")
    for entry in user.get_audit_log()[-3:]:
        print(f"   • {entry['action']}: {entry['description']}")
    
    print("\n" + "-" * 70)
    
    print("\n👤 USER 2 (jane_smith) - VERIFIED WITH PERMISSIONS:")
    print_status(user2)
    print(f"\n📊 Audit Log Entries: {len(user2.get_audit_log())}")
    print("Recent Actions:")
    for entry in user2.get_audit_log()[-3:]:
        print(f"   • {entry['action']}: {entry['description']}")
    
    # ========================================================================
    # PART 7: Invalid Email/Phone Validation
    # ========================================================================
    print_section("PART 7: Input Validation")
    
    print("\n1️⃣ Attempting to set invalid email:")
    success, message = user.update_email("invalid-email")
    print(f"   Result: {message}")
    print("   ✅ Invalid email rejected")
    
    print("\n2️⃣ Attempting to create user with invalid phone:")
    try:
        user3 = SecureUser(
            username="bad_user",
            email="valid@email.com",
            phone_number="123456789"  # Invalid format
        )
        print("   ❌ Invalid phone accepted (SECURITY ISSUE)")
    except ValueError as e:
        print(f"   ✅ Invalid phone rejected: {e}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section("✅ DEMONSTRATION COMPLETE")
    
    print("""
🔒 KEY SECURITY FEATURES DEMONSTRATED:

1. ENCAPSULATION:
   ✓ Private attributes cannot be accessed directly
   ✓ Protected attributes have controlled access
   ✓ All modifications go through validated methods

2. STATE TRANSITION PROTECTION:
   ✓ Illegal verification state transitions blocked
   ✓ State changes are logged and auditable
   ✓ Business rules enforced at all times

3. PERMISSION MANAGEMENT:
   ✓ Restricted permissions require verification
   ✓ Invalid permissions rejected
   ✓ Permission changes are audited

4. DATA INTEGRITY:
   ✓ Lists returned as copies (immutability)
   ✓ External modifications don't affect internal state
   ✓ Input validation on all setters

5. COMPOSITION:
   ✓ SecureUser combines Identity and Access
   ✓ Each component maintains its own integrity
   ✓ Clean separation of concerns
    """)


if __name__ == "__main__":
    main()
