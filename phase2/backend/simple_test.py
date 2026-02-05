"""Simple test to verify the app can be imported and runs"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        from main import app
        print("V Main app imported successfully")

        from database import get_session, engine
        print("V Database components imported successfully")

        from models.user import User, UserCreate, UserRead
        print("V User models imported successfully")

        from models.task import Task, TaskCreate, TaskRead, TaskUpdate
        print("V Task models imported successfully")

        from utils.security import hash_password, verify_password
        print("V Security utilities imported successfully")

        from utils.auth import create_access_token
        print("V Auth utilities imported successfully")

        from services.user_service import UserService
        print("V User service imported successfully")

        from services.task_service import TaskService
        print("V Task service imported successfully")

        from api.auth import router as auth_router
        print("V Auth router imported successfully")

        from api.tasks import router as tasks_router
        print("V Tasks router imported successfully")

        print("\n* All modules imported successfully!")
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