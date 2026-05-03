import time


class User:
    def __init__(self, name):
        self.name = name
        self.request_times = []

    def remove_old_requests(self, window_size):
        current_time = time.time()
        self.request_times = [
            req_time for req_time in self.request_times
            if current_time - req_time < window_size
        ]

    def add_request(self):
        self.request_times.append(time.time())

    def get_request_count(self):
        return len(self.request_times)


class RateLimiter:
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size

    def allow_request(self, user):
        user.remove_old_requests(self.window_size)

        if user.get_request_count() < self.max_requests:
            user.add_request()
            return True
        return False


class RateLimiterSystem:
    def __init__(self):
        self.limiter = RateLimiter(3, 10)

    def run(self):
        print("=== Rate Limiter System ===")
        user_name = input("Enter your user name: ")
        user = User(user_name)

        while True:
            print("\n1. Send Request")
            print("2. Show Request Count")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                if self.limiter.allow_request(user):
                    print("Request accepted.")
                else:
                    print("Rate limit exceeded. Please wait before sending another request.")

            elif choice == "2":
                user.remove_old_requests(self.limiter.window_size)
                print(f"{user.name} has made {user.get_request_count()} request(s) in the current time window.")

            elif choice == "3":
                print("Exiting system.")
                break

            else:
                print("Invalid choice. Please try again.")


system = RateLimiterSystem()
system.run()