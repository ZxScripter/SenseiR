# maintenance.py

import os

class MaintenanceManager:
    def turn_on_maintenance(self):
        # Create a file named ".maintenance" to indicate maintenance mode
        with open(".maintenance", "w") as maintenance_file:
            maintenance_file.write("Maintenance mode is ON")

    def turn_off_maintenance(self):
        # Remove the ".maintenance" file to turn off maintenance mode
        if os.path.exists(".maintenance"):
            os.remove(".maintenance")

    def is_maintenance_on(self):
        # Check if the ".maintenance" file exists
        return os.path.exists(".maintenance")

    # Wrapper function to check maintenance mode
    def maintenance_mode_check(self, func):
        def wrapper(client, message, *args, **kwargs):
            if self.is_maintenance_on():
                message.reply_text("Bot is currently under maintenance. Please try again later.")
                return
            return func(client, message, *args, **kwargs)
        return wrapper
