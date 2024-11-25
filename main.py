
from effective_mobile_interview.core.application import start_app
from tests.insert_test_data import insert_test_data

if __name__ == "__main__":
    insert_test_data() # После первого запуска закоментируйте
    start_app()