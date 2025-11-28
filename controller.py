from model import Model
from view import View
import datetime
import re


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        if self.model.session is None:
            self.running = False
        else:
            self.running = True

    # ========== ГОЛОВНЕ МЕНЮ ==========

    def run(self):
        while self.running:
            choice = self.show_main_menu_and_get_choice()

            if choice == 1:
                self.handle_show_menu()
            elif choice == 2:
                self.handle_add_menu()
            elif choice == 3:
                self.handle_update_menu()
            elif choice == 4:
                self.handle_delete_menu()
            elif choice == 5:
                self.handle_randomize_menu()
            elif choice == 6:
                self.handle_search_menu()
            elif choice == 0:
                self.running = False

        self.model.close_connection()
        self.view.show_message("\nGoodbye!")

    def show_main_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Fitness App Main Menu ---")
            self.view.show_message("1. Show all data (Task 1)")
            self.view.show_message("2. Add data (Task 1)")
            self.view.show_message("3. Update data (Task 1)")
            self.view.show_message("4. Delete data (Task 1)")
            self.view.show_message("5. Generate random data (Task 2)")
            self.view.show_message("6. Search data (Task 3)")
            self.view.show_message("0. Quit")

            try:
                choice_str = self.view.get_input("\nEnter your choice: ")
                choice = int(choice_str)
                if 0 <= choice <= 6:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")

    # -----------------------------------------------------------------
    # 1. ПРОСТИЙ ПЕРЕГЛЯД (ЗАВДАННЯ 1) - 'Show data'
    # -----------------------------------------------------------------

    def handle_show_menu(self):
        while True:
            choice = self.show_show_menu_and_get_choice()
            if choice == 1:
                results = self.model.get_all_users()
                self.view.show_users(results)
            elif choice == 2:
                results = self.model.get_all_workouts()
                self.view.show_workouts(results)
            elif choice == 3:
                results = self.model.get_all_user_workouts()
                self.view.show_user_workouts(results)
            elif choice == 4:
                results = self.model.get_all_health_metrics()
                self.view.show_health_metrics(results)
            elif choice == 5:
                results = self.model.get_all_friendships()
                self.view.show_friendships(results)
            elif choice == 0:
                break

    def show_show_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Show All Data (Task 1) ---")
            self.view.show_message("1. Show All Users")
            self.view.show_message("2. Show All Workouts")
            self.view.show_message("3. Show All User Workouts")
            self.view.show_message("4. Show All Health Metrics")
            self.view.show_message("5. Show All Friendships")
            self.view.show_message("0. Back to Main Menu")
            try:
                choice = int(self.view.get_input("\nEnter your choice: "))
                if 0 <= choice <= 5:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")

    # -----------------------------------------------------------------
    # 2. ДОДАВАННЯ (ЗАВДАННЯ 1) - 'Add data'
    # -----------------------------------------------------------------

    def handle_add_menu(self):
        while True:
            choice = self.show_add_menu_and_get_choice()
            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.add_workout()
            elif choice == 3:
                self.add_user_workout()
            elif choice == 4:
                self.add_health_metric()
            elif choice == 5:
                self.add_friendship()
            elif choice == 0:
                break

    def show_add_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Add data (Task 1) ---")
            self.view.show_message("1. Add User")
            self.view.show_message("2. Add Workout")
            self.view.show_message("3. Add User Workout")
            self.view.show_message("4. Add Health Metric")
            self.view.show_message("5. Add Friendship")
            self.view.show_message("0. Back to Main Menu")
            try:
                choice = int(self.view.get_input("\nEnter your choice: "))
                if 0 <= choice <= 5:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")


    def add_user(self):
        try:
            first_name = self.view.get_input("Enter first name: ")
            last_name = self.view.get_input("Enter last name: ")
            email = self.view.get_input("Enter email: ")
            phone = self.view.get_input("Enter phone (e.g., +380991234567): ")
            date_registration = self.view.get_input("Enter registration datetime (YYYY-MM-DD HH:MM:SS+TZ): ")

            if not all([first_name, last_name, email, date_registration]):
                self.view.show_message("Error: Required fields (name, email, date) cannot be empty.")
                return
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                self.view.show_message("Error: Invalid email format.")
                return
            if phone and not re.match(r"^\+?\d{10,13}$", phone):
                self.view.show_message("Error: Invalid phone format. Must be 10-13 digits, optionally starting with +.")
                return
            if not self._validate_timestamptz(date_registration):
                return

            self.model.add_user(first_name, last_name, email, phone, date_registration)
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def add_workout(self):
        try:
            type_workout = self.view.get_input("Enter workout type (e.g., 'Running', 'Yoga'): ")
            if not type_workout:
                self.view.show_message("Error: Field cannot be empty.")
                return
            self.model.add_workout(type_workout)
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def add_user_workout(self):
        try:
            user_id = int(self.view.get_input("Enter user_id (must exist): "))
            workout_id = int(self.view.get_input("Enter workout_id (must exist): "))
            date = self.view.get_input("Enter date (YYYY-MM-DD): ")
            time = self.view.get_input("Enter time (HH:MM:SS+TZ, e.g., 14:30:00+02): ")

            if not self._validate_date(date): return
            if not self._validate_timetz(time): return

            self.model.add_user_workout(user_id, workout_id, date, time)
        except ValueError:
            self.view.show_message("Invalid input. ID must be a number.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def add_health_metric(self):
        try:
            user_workout_id = int(self.view.get_input("Enter user_workout_id (must exist and be unique): "))
            steps = int(self.view.get_input("Enter steps: "))
            pulse = int(self.view.get_input("Enter pulse: "))
            calories = int(self.view.get_input("Enter calories: "))
            measurement_date = self.view.get_input("Enter measurement datetime (YYYY-MM-DD HH:MM:SS+TZ): ")

            if not self._validate_timestamptz(measurement_date):
                return

            self.model.add_health_metric(user_workout_id, steps, pulse, calories, measurement_date)
        except ValueError:
            self.view.show_message("Invalid input. IDs, steps, pulse, and calories must be numbers.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def add_friendship(self):
        try:
            user_id1 = int(self.view.get_input("Enter user_id1 (must exist): "))
            user_id2 = int(self.view.get_input("Enter user_id2 (must exist): "))
            status = self.view.get_input("Enter status (e.g., 'pending', 'accepted'): ")
            date = self.view.get_input("Enter friendship date (YYYY-MM-DD): ")

            if user_id1 == user_id2:
                self.view.show_message("Error: User cannot be friends with themselves.")
                return
            if not status:
                self.view.show_message("Error: Status cannot be empty.")
                return
            if not self._validate_date(date):
                return

            self.model.add_friendship(user_id1, user_id2, status, date)
        except ValueError:
            self.view.show_message("Invalid input. IDs must be numbers.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    # -----------------------------------------------------------------
    # 3. ОНОВЛЕННЯ (ЗАВДАННЯ 1) - 'Update data'
    # -----------------------------------------------------------------

    def handle_update_menu(self):
        while True:
            choice = self.show_update_menu_and_get_choice()
            if choice == 1:
                self.update_user()
            elif choice == 2:
                self.update_workout()
            elif choice == 3:
                self.update_user_workout()
            elif choice == 4:
                self.update_health_metric()
            elif choice == 5:
                self.update_friendship()
            elif choice == 0:
                break

    def show_update_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Update data (Task 1) ---")
            self.view.show_message("1. Update User")
            self.view.show_message("2. Update Workout")
            self.view.show_message("3. Update User Workout")
            self.view.show_message("4. Update Health Metric")
            self.view.show_message("5. Update Friendship")
            self.view.show_message("0. Back to Main Menu")
            try:
                choice = int(self.view.get_input("\nEnter your choice: "))
                if 0 <= choice <= 5:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")

    def update_user(self):
        try:
            user_id = int(self.view.get_input("Enter User ID to update: "))
            first_name = self.view.get_input("Enter NEW first name: ")
            last_name = self.view.get_input("Enter NEW last name: ")
            email = self.view.get_input("Enter NEW email: ")
            phone = self.view.get_input("Enter NEW phone: ")

            if not first_name or not last_name or not email:
                self.view.show_message("Error: Fields cannot be empty.")
                return
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                self.view.show_message("Error: Invalid email format.")
                return
            if phone and not re.match(r"^\+?\d{10,13}$", phone):
                self.view.show_message("Error: Invalid phone format.")
                return

            self.model.update_user(user_id, first_name, last_name, email, phone)
        except ValueError:
            self.view.show_message("Invalid input. ID must be a number.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def update_workout(self):
        try:
            workout_id = int(self.view.get_input("Enter Workout ID to update: "))
            type_workout = self.view.get_input("Enter NEW workout type: ")
            if not type_workout:
                self.view.show_message("Error: Field cannot be empty.")
                return
            self.model.update_workout(workout_id, type_workout)
        except ValueError:
            self.view.show_message("Invalid input. ID must be a number.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def update_user_workout(self):
        try:
            user_workout_id = int(self.view.get_input("Enter User Workout ID to update: "))
            user_id = int(self.view.get_input("Enter NEW user_id (must exist): "))
            workout_id = int(self.view.get_input("Enter NEW workout_id (must exist): "))
            date = self.view.get_input("Enter NEW date (YYYY-MM-DD): ")
            # --- ОНОВЛЕНО ---
            time = self.view.get_input("Enter NEW time (HH:MM:SS+TZ, e.g., 14:30:00+02): ")

            if not self._validate_date(date): return
            if not self._validate_timetz(time): return

            self.model.update_user_workout(user_workout_id, user_id, workout_id, date, time)
        except ValueError:
            self.view.show_message("Invalid input. IDs must be numbers.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def update_health_metric(self):
        try:
            metrics_id = int(self.view.get_input("Enter Metrics ID to update: "))
            steps = int(self.view.get_input("Enter NEW steps: "))
            pulse = int(self.view.get_input("Enter NEW pulse: "))
            calories = int(self.view.get_input("Enter NEW calories: "))
            measurement_date = self.view.get_input("Enter NEW measurement datetime (YYYY-MM-DD HH:MM:SS+TZ): ")

            if not self._validate_timestamptz(measurement_date):
                return

            self.model.update_health_metric(metrics_id, steps, pulse, calories, measurement_date)
        except ValueError:
            self.view.show_message("Invalid input. IDs and values must be numbers.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def update_friendship(self):
        try:
            self.view.show_message("Updating friendship requires identifying the record by BOTH user IDs.")
            user_id1 = int(self.view.get_input("Enter user_id1 of the friendship: "))
            user_id2 = int(self.view.get_input("Enter user_id2 of the friendship: "))
            new_status = self.view.get_input("Enter NEW status (e.g., 'accepted'): ")

            if not new_status:
                self.view.show_message("Error: Status cannot be empty.")
                return

            self.model.update_friendship(user_id1, user_id2, new_status)
        except ValueError:
            self.view.show_message("Invalid input. IDs must be numbers.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

        # -----------------------------------------------------------------
        # 4. ВИДАЛЕННЯ (ЗАВДАННЯ 1) - 'Delete data'
        # -----------------------------------------------------------------
    def handle_delete_menu(self):
            while True:
                self.view.show_message("\n--- Delete data (Task 1) ---")
                self.view.show_message("Enter '0' to exit.")

                try:
                    table_name = self.view.get_input("Enter table_name to delete from: ")
                    if table_name == '0':
                        break

                    field = self.view.get_input(f"Enter field to delete by: ")
                    value = self.view.get_input(f"Enter {field} value to delete: ")

                    self.model.delete_data(table_name, field, value)

                except Exception as e:
                    self.view.show_message(f"An error occurred: {str(e)}")

    # -----------------------------------------------------------------
    # 5. ГЕНЕРАЦІЯ (ЗАВДАННЯ 2) - 'Generate data'
    # -----------------------------------------------------------------

    def handle_randomize_menu(self):
        while True:
            choice = self.show_randomize_menu_and_get_choice()
            if choice == 0: break
            try:
                count_str = self.view.get_input("Enter number of records to generate: ")
                count = int(count_str)
                if count <= 0:
                    self.view.show_message("Error: Number must be greater than 0.")
                    continue
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
                continue
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")
                continue

            if choice == 1:
                self.model.generate_users(count)
            elif choice == 2:
                self.model.generate_workouts(count)
            elif choice == 3:
                self.model.generate_user_workouts(count)
            elif choice == 4:
                self.model.generate_health_metrics(count)
            elif choice == 5:
                self.model.generate_friendships(count)

    def show_randomize_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Generate Random Data (Task 2) ---")
            self.view.show_message("1. Generate Users")
            self.view.show_message("2. Generate Workouts")
            self.view.show_message("3. Generate User Workouts (needs Users/Workouts)")
            self.view.show_message("4. Generate Health Metrics (needs User Workouts)")
            self.view.show_message("5. Generate Friendships (needs Users)")
            self.view.show_message("0. Back to Main Menu")
            try:
                choice = int(self.view.get_input("\nEnter your choice: "))
                if 0 <= choice <= 5:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")

    # -----------------------------------------------------------------
    # 6. ПОШУК (ЗАВДАННЯ 3) - 'Search data'
    # -----------------------------------------------------------------

    def handle_search_menu(self):
        while True:
            choice = self.show_search_menu_and_get_choice()
            if choice == 1:
                self.search_users()
            elif choice == 2:
                self.search_workouts()
            elif choice == 3:
                self.search_user_workouts()
            elif choice == 4:
                self.search_health_metrics()
            elif choice == 5:
                self.search_friendships()
            elif choice == 6:
                self.search_workouts_by_username()
            elif choice == 7:
                self.search_users_by_pulse()
            elif choice == 8:
                self.show_workout_counts()
            elif choice == 0:
                break

    def show_search_menu_and_get_choice(self):
        while True:
            self.view.show_message("\n--- Search data (Task 3) ---")
            self.view.show_message("--- Basic Search (1 Table) ---")
            self.view.show_message("1. Search Users")
            self.view.show_message("2. Search Workouts")
            self.view.show_message("3. Search User Workouts")
            self.view.show_message("4. Search Health Metrics")
            self.view.show_message("5. Search Friendships")
            self.view.show_message("--- Complex Search (JOIN / GROUP BY) ---")
            self.view.show_message("6. Find Workouts by User Name (JOIN)")
            self.view.show_message("7. Find Users by Pulse Rate (JOIN)")
            self.view.show_message("8. Show Workout Count per User (GROUP BY)")
            self.view.show_message("----------------------------------------")
            self.view.show_message("0. Back to Main Menu")
            try:
                choice = int(self.view.get_input("\nEnter your choice: "))
                if 0 <= choice <= 8:
                    return choice
                else:
                    self.view.show_message("Invalid choice. Try again.")
            except ValueError:
                self.view.show_message("Invalid input. Please enter a number.")
            except Exception as e:
                self.view.show_message(f"An error occurred: {e}")

    def search_users(self):
        try:
            choice = int(self.view.get_input(
                "Search Users by:\n1. User IDs (range)\n2. First Name (like)\n3. Last Name (like)\n4. Email (like)\n0. Back\nChoice: "))
        except ValueError:
            self.view.show_message("Invalid input. Try again.")
            return
        if choice == 1:
            start_id = self.view.get_input("Enter User ID to start with: ")
            end_id = self.view.get_input("Enter User ID to finish with: ")
            order_by = self.view.get_input("Enter field to order by (e.g., user_id): ")
            request = f"user user_id {start_id} {end_id} {order_by}"
            results = self.model.get_data_in_range(request)
            self.view.show_users(results)
        elif choice in [2, 3, 4]:
            if choice == 2:
                field = "first_name"; pattern = self.view.get_input("Enter First Name pattern (e.g., 'Vla%'): ")
            elif choice == 3:
                field = "last_name"; pattern = self.view.get_input("Enter Last Name pattern: ")
            elif choice == 4:
                field = "email"; pattern = self.view.get_input("Enter Email pattern (e.g., '%@gmail.com'): ")
            order_by = self.view.get_input("Enter field to order by (e.g., user_id): ")
            request = f"user {field} {pattern} {order_by}"
            results = self.model.get_data_by_field_like(request)
            self.view.show_users(results)
        elif choice == 0:
            pass
        else:
            self.view.show_message("Invalid choice.")

    def search_user_workouts(self):
        try:
            choice = int(
                self.view.get_input("Search User Workouts by:\n1. Date (range)\n2. User ID (range)\n0. Back\nChoice: "))
        except ValueError:
            self.view.show_message("Invalid input. Try again.")
            return
        if choice == 1:
            start_date = self.view.get_input("Enter start date (YYYY-MM-DD): ")
            end_date = self.view.get_input("Enter end date (YYYY-MM-DD): ")
            order_by = self.view.get_input("Enter field to order by (e.g., date): ")
            request = f"user_workout date '{start_date}' '{end_date}' {order_by}"
            results = self.model.get_data_in_range(request)
            self.view.show_user_workouts(results)
        elif choice == 2:
            start_id = self.view.get_input("Enter User ID to start with: ")
            end_id = self.view.get_input("Enter User ID to finish with: ")
            order_by = self.view.get_input("Enter field to order by (e.g., user_user_id): ")
            request = f"user_workout user_user_id {start_id} {end_id} {order_by}"
            results = self.model.get_data_in_range(request)
            self.view.show_user_workouts(results)
        elif choice == 0:
            pass
        else:
            self.view.show_message("Invalid choice.")

    def search_workouts(self):
        try:
            choice = int(self.view.get_input("Search Workouts by:\n1. Workout Type (like)\n0. Back\nChoice: "))
        except ValueError:
            self.view.show_message("Invalid input. Try again.")
            return
        if choice == 1:
            pattern = self.view.get_input("Enter Workout Type pattern (e.g., 'Run%'): ")
            order_by = self.view.get_input("Enter field to order by (e.g., workout_id): ")
            request = f"workout type_workout {pattern} {order_by}"
            results = self.model.get_data_by_field_like(request)
            self.view.show_workouts(results)
        elif choice == 0:
            pass
        else:
            self.view.show_message("Invalid choice.")

    def search_health_metrics(self):
        try:
            choice = int(self.view.get_input(
                "Search Health Metrics by:\n1. Steps (range)\n2. Pulse (range)\n3. Calories (range)\n0. Back\nChoice: "))
        except ValueError:
            self.view.show_message("Invalid input. Try again.")
            return
        field = ""
        if choice == 1:
            field = "steps"
        elif choice == 2:
            field = "pulse"
        elif choice == 3:
            field = "calories"
        elif choice == 0:
            return
        else:
            self.view.show_message("Invalid choice.")
            return
        start_val = self.view.get_input(f"Enter min {field}: ")
        end_val = self.view.get_input(f"Enter max {field}: ")
        order_by = self.view.get_input("Enter field to order by (e.g., metrics_id): ")
        request = f"\"health metrics\" {field} {start_val} {end_val} {order_by}"
        results = self.model.get_data_in_range(request)
        self.view.show_health_metrics(results)

    def search_friendships(self):
        try:
            choice = int(self.view.get_input("Search Friendships by:\n1. Status (like)\n0. Back\nChoice: "))
        except ValueError:
            self.view.show_message("Invalid input. Try again.")
            return
        if choice == 1:
            pattern = self.view.get_input("Enter Status pattern (e.g., 'accepted'): ")
            order_by = self.view.get_input("Enter field to order by (e.g., date): ")
            request = f"friendship status {pattern} {order_by}"
            results = self.model.get_data_by_field_like(request)
            self.view.show_friendships(results)
        elif choice == 0:
            pass
        else:
            self.view.show_message("Invalid choice.")

    # --- Складний пошук ---

    def search_workouts_by_username(self):
        try:
            pattern = self.view.get_input("Enter User First Name pattern (e.g., 'Vla%'): ")
            if not pattern:
                self.view.show_message("Error: Pattern cannot be empty.")
                return
            results = self.model.search_workouts_by_username(pattern)
            self.view.show_workouts_by_username(results)
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def search_users_by_pulse(self):
        try:
            min_pulse = int(self.view.get_input("Enter minimum pulse rate (e.g., 120): "))
            results = self.model.search_users_by_pulse(min_pulse)
            self.view.show_users_by_pulse(results)
        except ValueError:
            self.view.show_message("Invalid input. Pulse must be a number.")
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    def show_workout_counts(self):
        try:
            results = self.model.get_workout_counts_by_user()
            self.view.show_workout_counts(results)
        except Exception as e:
            self.view.show_message(f"An error occurred: {str(e)}")

    # -----------------------------------------------------------------
    # НОВЕ: Допоміжні функції валідації
    # -----------------------------------------------------------------

    def _validate_date(self, date_str):
        """Перевіряє формат YYYY-MM-DD та логічність дати."""
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            self.view.show_message("Error: Invalid date format. Please use YYYY-MM-DD.")
            return False
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            self.view.show_message("Error: Invalid date value (e.g., 2020-14-10 is not a real date).")
            return False

    def _validate_timetz(self, time_str):
        if not re.match(r"^\d{2}:\d{2}:\d{2}[+-]\d{2}(:\d{2})?$", time_str):
            self.view.show_message("Error: Invalid time format. Please use HH:MM:SS+TZ (e.g., 14:30:00+02).")
            return False
        try:
            datetime.datetime.strptime(time_str[:8], '%H:%M:%S')
            return True
        except ValueError:
            self.view.show_message("Error: Invalid time value (e.g., 25:00:00+02 is not a real time).")
            return False

    def _validate_timestamptz(self, datetime_str):
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[+-]\d{2}(:\d{2})?$", datetime_str):
            self.view.show_message("Error: Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS+TZ (e.g., ...+02).")
            return False
        try:
            datetime.datetime.strptime(datetime_str[:19], '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            self.view.show_message("Error: Invalid datetime value (e.g., 2020-14-10 ...).")
            return False

