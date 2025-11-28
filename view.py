class View:

    def show_message(self, message):
        print(message)

    def get_input(self, input_message):
        return input(input_message)

    def show_users(self, results):
        if not results:
            self.show_message("No users found.")
            return

        self.show_message("\n--- Users ---")
        for result in results:
            print(
                f"User ID: {result[0]}\nFirst Name: {result[1]}\nLast Name: {result[2]}\nEmail: {result[3]}\nPhone: {result[4]}\nRegistration Date: {result[5]}\n")

    def show_workouts(self, results):
        if not results:
            self.show_message("No workouts found.")
            return

        self.show_message("\n--- Workout Types ---")
        for result in results:
            print(f"Workout ID: {result[0]}\nWorkout Type: {result[1]}\n")

    def show_user_workouts(self, results):
        if not results:
            self.show_message("No user workouts found.")
            return

        self.show_message("\n--- User Workouts ---")
        for result in results:
            print(
                f"User Workout ID: {result[0]}\nUser ID: {result[1]}\nWorkout ID: {result[2]}\nDate: {result[3]}\nTime: {result[4]}\n")

    def show_health_metrics(self, results):
        if not results:
            self.show_message("No health metrics found.")
            return

        self.show_message("\n--- Health Metrics ---")
        for result in results:
            print(
                f"Metrics ID: {result[0]}\nUser Workout ID: {result[5]}\nSteps: {result[1]}\nPulse: {result[2]}\nCalories: {result[3]}\nMeasurement Date: {result[4]}\n")

    def show_friendships(self, results):
        if not results:
            self.show_message("No friendships found.")
            return

        self.show_message("\n--- Friendships ---")
        for result in results:
            print(
                f"Friendship PK ID: {result[0]}\nUser 1 ID: {result[1]}\nUser 2 ID: {result[2]}\nStatus: {result[3]}\nDate: {result[4]}\n")

    # -----------------------------------------------------------------
    # Data Display Methods (для складного пошуку Завдання 3)
    # -----------------------------------------------------------------

    def show_workouts_by_username(self, results):
        if not results:
            self.show_message("No workouts found for that user name.")
            return

        self.show_message("\n--- Workouts Found (by User Name) ---")
        for result in results:
            print(f"User: {result[0]} {result[1]}\nWorkout: {result[2]}\nDate: {result[3]}\nTime: {result[4]}\n")

    def show_users_by_pulse(self, results):
        if not results:
            self.show_message("No users found with pulse greater than that value.")
            return

        self.show_message("\n--- Users Found (by Pulse Rate) ---")
        for result in results:
            print(f"User ID: {result[0]}\nName: {result[1]} {result[2]}\nRecorded Pulse: {result[3]} BPM\n")

    def show_workout_counts(self, results):
        if not results:
            self.show_message("No users found to count.")
            return

        self.show_message("\n--- Total Workouts per User ---")
        for result in results:
            print(f"User ID: {result[0]}\nName: {result[1]} {result[2]}\nTotal Workouts: {result[3]}\n")