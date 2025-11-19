"""
Example Test Cases for the Fintech Identity System
Run these to verify the system works correctly
"""

from secure_user import SecureUser


def test_basic_creation():
    """Test 1: Basic user creation"""
    print("TEST 1: Basic User Creation")
    print("-" * 50)
    
    user = SecureUser("alice", "alice@example.com", "+1-555-111-2222")
    status = user.identity_status()
    
    assert status['username'] == "alice"
    assert status['email'] == "alice@example.com"
    assert status['phone'] == "+1-555-111-2222"
    assert status['verification_status'] == "UNVERIFIED"
    assert len(status['permissions']) == 0
    
    print("✅ User created successfully")
    print(f"   Username: {status['username']}")
    print(f"   Status: {status['verification_status']}")
    print()


def test_invalid_email():
    """Test 2: Invalid email rejection"""
    print("TEST 2: Invalid Email Rejection")
    print("-" * 50)
    
    try:
        user = SecureUser("bob", "invalid-email", "+1-555-222-3333")
        print("❌ FAILED: Invalid email was accepted")
    except ValueError as e:
        print(f"✅ Invalid email rejected: {e}")
    print()


def test_invalid_phone():
    """Test 3: Invalid phone rejection"""
    print("TEST 3: Invalid Phone Rejection")
    print("-" * 50)
    
    try:
        user = SecureUser("charlie", "charlie@example.com", "123456789")
        print("❌ FAILED: Invalid phone was accepted")
    except ValueError as e:
        print(f"✅ Invalid phone rejected: {e}")
    print()


def test_verification_workflow():
    """Test 4: Verification state transitions"""
    print("TEST 4: Verification Workflow")
    print("-" * 50)
    
    user = SecureUser("diana", "diana@example.com", "+1-555-333-4444")
    
    # Initial state
    assert user._identity.get_verification_status() == "UNVERIFIED"
    print("✅ Initial state: UNVERIFIED")
    
    # Request verification
    result = user.request_verification()
    assert result == True
    assert user._identity.get_verification_status() == "PENDING"
    print("✅ After request: PENDING")
    
    # Complete verification
    result = user.verify_identity()
    assert result == True
    assert user._identity.get_verification_status() == "VERIFIED"
    print("✅ After verify: VERIFIED")
    print()


def test_invalid_state_transition():
    """Test 5: Invalid state transitions"""
    print("TEST 5: Invalid State Transitions")
    print("-" * 50)
    
    user = SecureUser("eve", "eve@example.com", "+1-555-444-5555")
    
    # Try to verify without requesting
    result = user.verify_identity()
    assert result == False
    assert user._identity.get_verification_status() == "UNVERIFIED"
    print("✅ Cannot verify from UNVERIFIED state")
    
    # Verify properly
    user.request_verification()
    user.verify_identity()
    
    # Try to request again after verified
    result = user.request_verification()
    assert result == False
    assert user._identity.get_verification_status() == "VERIFIED"
    print("✅ Cannot request from VERIFIED state")
    print()


def test_permission_without_verification():
    """Test 6: Restricted permissions require verification"""
    print("TEST 6: Permission Restrictions")
    print("-" * 50)
    
    user = SecureUser("frank", "frank@example.com", "+1-555-555-6666")
    
    # Try to grant TRANSFER (restricted) without verification
    success, message = user.grant_permission("TRANSFER")
    assert success == False
    assert "must be VERIFIED" in message
    print(f"✅ TRANSFER denied without verification: {message}")
    
    # Grant VIEW_BALANCE (non-restricted)
    success, message = user.grant_permission("VIEW_BALANCE")
    assert success == True
    print(f"✅ VIEW_BALANCE granted: {message}")
    
    # Verify user
    user.request_verification()
    user.verify_identity()
    
    # Now grant TRANSFER
    success, message = user.grant_permission("TRANSFER")
    assert success == True
    print(f"✅ TRANSFER granted after verification: {message}")
    print()


def test_list_copy_safety():
    """Test 7: Defensive copying prevents external modification"""
    print("TEST 7: List Copy Safety")
    print("-" * 50)
    
    user = SecureUser("grace", "grace@example.com", "+1-555-666-7777")
    user.request_verification()
    user.verify_identity()
    user.grant_permission("TRANSFER")
    user.grant_permission("WITHDRAW")
    
    # Get permissions
    perms = user.get_permissions()
    original_length = len(perms)
    print(f"   Original permissions: {perms}")
    
    # Try to modify external list
    perms.append("ADMIN_ACCESS")
    perms.append("ROOT_ACCESS")
    print(f"   Modified external list: {perms}")
    
    # Check actual permissions
    actual_perms = user.get_permissions()
    assert len(actual_perms) == original_length
    assert "ADMIN_ACCESS" not in actual_perms
    assert "ROOT_ACCESS" not in actual_perms
    print(f"   Actual permissions unchanged: {actual_perms}")
    print("✅ Internal data protected from external modification")
    print()


def test_audit_log_copy_safety():
    """Test 8: Audit log copy safety"""
    print("TEST 8: Audit Log Copy Safety")
    print("-" * 50)
    
    user = SecureUser("henry", "henry@example.com", "+1-555-777-8888")
    
    # Get audit log
    audit = user.get_audit_log()
    original_length = len(audit)
    print(f"   Original audit entries: {original_length}")
    
    # Try to modify external list
    audit.append({"malicious": "entry"})
    audit.append({"fake": "data"})
    print(f"   Modified external list: {len(audit)} entries")
    
    # Check actual audit log
    actual_audit = user.get_audit_log()
    assert len(actual_audit) == original_length
    print(f"   Actual audit log unchanged: {len(actual_audit)} entries")
    print("✅ Audit log protected from tampering")
    print()


def test_private_attribute_access():
    """Test 9: Private attributes cannot be accessed"""
    print("TEST 9: Private Attribute Access")
    print("-" * 50)
    
    user = SecureUser("iris", "iris@example.com", "+1-555-888-9999")
    
    # Try to access private __phone_number
    try:
        phone = user._identity.__phone_number
        print("❌ SECURITY BREACH: Accessed private __phone_number")
    except AttributeError:
        print("✅ Cannot access __phone_number (private)")
    
    # Try to access private __access
    try:
        access = user.__access
        print("❌ SECURITY BREACH: Accessed private __access")
    except AttributeError:
        print("✅ Cannot access __access (private)")
    
    # Try to access private __audit_log
    try:
        audit = user.__audit_log
        print("❌ SECURITY BREACH: Accessed private __audit_log")
    except AttributeError:
        print("✅ Cannot access __audit_log (private)")
    
    print()


def test_email_update():
    """Test 10: Email update with validation"""
    print("TEST 10: Email Update with Validation")
    print("-" * 50)
    
    user = SecureUser("jack", "jack@example.com", "+1-555-999-0000")
    
    # Update to valid email
    success, message = user.update_email("jack.new@example.com")
    assert success == True
    assert user._identity.get_email() == "jack.new@example.com"
    print(f"✅ Valid email update: {message}")
    
    # Try to update to invalid email
    success, message = user.update_email("invalid-email")
    assert success == False
    assert user._identity.get_email() == "jack.new@example.com"  # Unchanged
    print(f"✅ Invalid email rejected: {message}")
    print()


def test_permission_revocation():
    """Test 11: Permission revocation"""
    print("TEST 11: Permission Revocation")
    print("-" * 50)
    
    user = SecureUser("kate", "kate@example.com", "+1-555-000-1111")
    user.request_verification()
    user.verify_identity()
    
    # Grant permissions
    user.grant_permission("TRANSFER")
    user.grant_permission("WITHDRAW")
    assert user.has_permission("TRANSFER")
    assert user.has_permission("WITHDRAW")
    print("✅ Permissions granted: TRANSFER, WITHDRAW")
    
    # Revoke TRANSFER
    success, message = user.revoke_permission("TRANSFER")
    assert success == True
    assert not user.has_permission("TRANSFER")
    assert user.has_permission("WITHDRAW")
    print(f"✅ {message}")
    
    # Try to revoke non-existent permission
    success, message = user.revoke_permission("FAKE_PERMISSION")
    assert success == False
    print(f"✅ {message}")
    print()


def test_duplicate_permission():
    """Test 12: Duplicate permission handling"""
    print("TEST 12: Duplicate Permission Handling")
    print("-" * 50)
    
    user = SecureUser("leo", "leo@example.com", "+1-555-111-2222")
    
    # Grant VIEW_BALANCE
    success, message = user.grant_permission("VIEW_BALANCE")
    assert success == True
    print(f"✅ First grant: {message}")
    
    # Try to grant again
    success, message = user.grant_permission("VIEW_BALANCE")
    assert success == False
    assert "already granted" in message
    print(f"✅ Duplicate rejected: {message}")
    print()


def test_invalid_permission():
    """Test 13: Invalid permission handling"""
    print("TEST 13: Invalid Permission Handling")
    print("-" * 50)
    
    user = SecureUser("mia", "mia@example.com", "+1-555-222-3333")
    
    # Try to grant invalid permission
    success, message = user.grant_permission("DELETE_DATABASE")
    assert success == False
    assert "Invalid permission" in message
    print(f"✅ {message}")
    print()


def run_all_tests():
    """Run all test cases"""
    print("=" * 70)
    print("  RUNNING ALL TEST CASES")
    print("=" * 70)
    print()
    
    test_basic_creation()
    test_invalid_email()
    test_invalid_phone()
    test_verification_workflow()
    test_invalid_state_transition()
    test_permission_without_verification()
    test_list_copy_safety()
    test_audit_log_copy_safety()
    test_private_attribute_access()
    test_email_update()
    test_permission_revocation()
    test_duplicate_permission()
    test_invalid_permission()
    
    print("=" * 70)
    print("  ALL TESTS PASSED ✅")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
