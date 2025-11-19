# 🚀 Quick Reference Guide

## Installation & Running

```bash
cd "encapsulation hw"
python main.py              # Full demonstration
python test_cases.py        # Run all tests
python index.py             # Single-file version
```

---

## Usage Examples

### Creating a User
```python
from secure_user import SecureUser

user = SecureUser(
    username="john_doe",
    email="john@example.com",
    phone_number="+1-555-123-4567"
)
```

### Verification Workflow
```python
# Check status
status = user._identity.get_verification_status()  # "UNVERIFIED"

# Request verification
user.request_verification()  # UNVERIFIED → PENDING

# Complete verification
user.verify_identity()  # PENDING → VERIFIED
```

### Granting Permissions
```python
# Non-restricted permission (no verification required)
success, msg = user.grant_permission("VIEW_BALANCE")

# Restricted permission (requires verification)
success, msg = user.grant_permission("TRANSFER")
# Returns: (False, "Cannot grant 'TRANSFER' - user must be VERIFIED")

# After verification
user.request_verification()
user.verify_identity()
success, msg = user.grant_permission("TRANSFER")
# Returns: (True, "Permission granted: TRANSFER")
```

### Checking Permissions
```python
# Check single permission
has_it = user.has_permission("TRANSFER")  # True/False

# Get all permissions (returns a copy)
perms = user.get_permissions()  # ['VIEW_BALANCE', 'TRANSFER']
```

### Revoking Permissions
```python
success, msg = user.revoke_permission("TRANSFER")
# Returns: (True, "Permission revoked: TRANSFER")
```

### Updating Email
```python
success, msg = user.update_email("new@example.com")
# Returns: (True, "Email updated successfully")

success, msg = user.update_email("invalid")
# Returns: (False, "Invalid email format: invalid")
```

### Getting User Status
```python
status = user.identity_status()
# Returns: {
#     'username': 'john_doe',
#     'email': 'john@example.com',
#     'phone': '+1-555-123-4567',
#     'verification_status': 'VERIFIED',
#     'permissions': ['VIEW_BALANCE', 'TRANSFER']
# }
```

### Accessing Audit Log
```python
audit = user.get_audit_log()  # Returns a copy
# Each entry contains:
# {
#     'timestamp': '2025-11-19T10:30:45.123456',
#     'action': 'GRANT_PERMISSION',
#     'description': 'Attempted to grant...',
#     'success': True,
#     'user': 'john_doe',
#     'verification_status': 'VERIFIED'
# }
```

---

## Access Levels

| Attribute | Access Level | Example | Protection |
|-----------|-------------|---------|------------|
| `username` | Public | `user._identity.username` | None (direct access) |
| `_email` | Protected | `user._identity._email` | Convention (discouraged) |
| `__phone_number` | Private | ❌ Not accessible | Name mangling |
| `__access` | Private | ❌ Not accessible | Name mangling |
| `__audit_log` | Private | ❌ Not accessible | Name mangling |

---

## Permissions

### Non-Restricted (No verification required)
- `VIEW_BALANCE`
- `VIEW_TRANSACTIONS`
- `DEPOSIT`
- `UPDATE_PROFILE`

### Restricted (Verification required)
- `TRANSFER` ⚠️
- `WITHDRAW` ⚠️

---

## Validation Rules

### Email Format
✅ `user@example.com`  
✅ `john.doe@company.co.uk`  
❌ `invalid-email`  
❌ `user@`  
❌ `@example.com`  

Pattern: `name@domain.extension`

### Phone Format
✅ `+1-555-123-4567`  
✅ `+998-90-123-4567`  
✅ `+44-20-1234-5678`  
❌ `123456789`  
❌ `555-1234`  
❌ `+1 555 123 4567`  

Pattern: `+XXX-XXX-XXXX-XXXXX`

---

## State Transitions

```
UNVERIFIED → PENDING → VERIFIED
```

### Valid Transitions
✅ `UNVERIFIED` → `PENDING` (via `request_verification()`)  
✅ `PENDING` → `VERIFIED` (via `verify()`)  

### Invalid Transitions (Blocked)
❌ `UNVERIFIED` → `VERIFIED` (must go through PENDING)  
❌ `VERIFIED` → `PENDING` (cannot reverse)  
❌ `VERIFIED` → `UNVERIFIED` (cannot reverse)  

---

## Common Patterns

### Full User Setup
```python
# Create user
user = SecureUser("alice", "alice@example.com", "+1-555-111-2222")

# Verify identity
user.request_verification()
user.verify_identity()

# Grant permissions
user.grant_permission("VIEW_BALANCE")
user.grant_permission("TRANSFER")
user.grant_permission("WITHDRAW")

# Check status
print(user.identity_status())
```

### Safe List Access
```python
# ✅ CORRECT: Get copy
perms = user.get_permissions()
perms.append("ADMIN")  # Modifies copy only
actual = user.get_permissions()  # Unchanged

# ❌ WRONG: Try to get reference
# perms = user.__access.__permissions  # AttributeError!
```

### Error Handling
```python
try:
    user = SecureUser("bob", "invalid-email", "+1-555-222-3333")
except ValueError as e:
    print(f"Invalid input: {e}")

success, msg = user.grant_permission("TRANSFER")
if not success:
    print(f"Permission denied: {msg}")
```

---

## Debugging Tips

### Check Verification Status
```python
status = user._identity.get_verification_status()
print(f"Current status: {status}")
```

### View State History
```python
history = user._identity.get_state_history()
for entry in history:
    print(f"{entry['timestamp']}: {entry['action']}")
```

### Check Permission History
```python
# Note: This requires accessing internal _SecureUser__access
# Better to use audit log instead
audit = user.get_audit_log()
for entry in audit:
    if 'PERMISSION' in entry['action']:
        print(entry['description'])
```

### View Full Audit Trail
```python
audit = user.get_audit_log()
for i, entry in enumerate(audit, 1):
    print(f"{i}. [{entry['timestamp']}]")
    print(f"   Action: {entry['action']}")
    print(f"   Description: {entry['description']}")
    print(f"   Success: {entry['success']}")
```

---

## Testing Checklist

- [ ] User creation with valid data
- [ ] Invalid email rejection
- [ ] Invalid phone rejection
- [ ] Verification workflow
- [ ] Invalid state transitions blocked
- [ ] Restricted permissions without verification denied
- [ ] Restricted permissions with verification granted
- [ ] List copy safety (permissions)
- [ ] List copy safety (audit log)
- [ ] Private attribute access blocked
- [ ] Email update with validation
- [ ] Permission revocation
- [ ] Duplicate permission handling
- [ ] Invalid permission handling

Run `python test_cases.py` to verify all ✅

---

## File Structure

```
encapsulation hw/
├── user_identity.py      # UserIdentity class
├── account_access.py     # AccountAccess class
├── secure_user.py        # SecureUser class (composition)
├── main.py              # Comprehensive demo
├── index.py             # All-in-one version
├── test_cases.py        # Automated tests
├── README.md            # Full documentation
├── EXPLANATION.md       # Design explanations
├── ARCHITECTURE.md      # System diagrams
├── SUMMARY.md           # Assignment completion
└── QUICK_REFERENCE.md   # This file
```

---

## Key Concepts

### 1. Encapsulation
Hiding internal state and requiring all interaction through methods.

### 2. Defensive Copying
Returning copies of mutable data structures to prevent external modification.

### 3. Composition
Building complex objects from simpler, independent components.

### 4. State Machines
Enforcing valid state transitions through controlled methods.

### 5. Validation
Checking all inputs before accepting them.

### 6. Audit Logging
Recording all significant actions for security and debugging.

---

## Need Help?

- **Full documentation**: See `README.md`
- **Design rationale**: See `EXPLANATION.md`
- **Visual diagrams**: See `ARCHITECTURE.md`
- **Run examples**: `python main.py`
- **Run tests**: `python test_cases.py`
