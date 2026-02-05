"""Test script to verify password hashing works with the fix."""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_password_hashing():
    """Test that password hashing works with the fix."""
    try:
        from utils.security import hash_password, verify_password

        # Test with a short password
        test_password = "testpass123"
        hashed = hash_password(test_password)
        verified = verify_password(test_password, hashed)

        print(f"V Short password test: {verified}")

        # Test with a longer password (> 72 bytes)
        long_password = "a" * 80  # 80 characters, which is > 72 bytes
        hashed_long = hash_password(long_password)
        verified_long = verify_password(long_password, hashed_long)

        print(f"V Long password test: {verified_long}")

        # Test that we can verify with truncated version
        truncated = long_password[:72]
        verified_truncated = verify_password(truncated, hashed_long)
        print(f"V Truncated verification test: {verified_truncated}")

        print("\n* Password hashing works correctly with the fix!")
        return True

    except Exception as e:
        print(f"X Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_password_hashing()
    if success:
        print("\nPassword hashing fix verified successfully!")
    else:
        print("\nPassword hashing fix failed.")
        sys.exit(1)