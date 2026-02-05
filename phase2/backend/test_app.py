"""Simple test to verify the app can be imported and runs"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        from main import app
        from database import get_session, engine
        from models.user import User, UserCreate, UserRead
        from models.task import Task, TaskCreate, TaskRead, TaskUpdate
        from utils.security import hash_password, verify_password
        from utils.auth import create_access_token
        from services.user_service import UserService
        from services.task_service import TaskService
        from api.auth import router as auth_router
        from api.tasks import router as tasks_router

        print("V All modules imported successfully")

        # Test basic functionality
        test_password = "testpass123"  # Shorter password to comply with bcrypt limits
        hashed = hash_password(test_password)
        assert verify_password(test_password, hashed), "Password hashing/verification failed"
        print("V Password hashing works correctly")

        # Test token creation
        token = create_access_token({"sub": "test_user"})
        assert isinstance(token, str) and len(token) > 0, "Token creation failed"
        print("V JWT token creation works correctly")

        print("\n* All basic functionality tests passed!")
        return True

    except Exception as e:
        print(f"X Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nThe backend application structure is working correctly!")
    else:
        print("\nThere are issues with the backend application structure.")
        sys.exit(1)