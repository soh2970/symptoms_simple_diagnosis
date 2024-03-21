from health_app_interface import HealthAppInterface
from user_data import UserData

if __name__ == "__main__":
    data_instance = UserData('user', 'pass', 25, 170, 70)
    app = HealthAppInterface()
    app.run(data_instance)
