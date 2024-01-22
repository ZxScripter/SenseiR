# main_bot.py
from pyrogram import Client as app, filters
from helper.maindb import MaintenanceManager

# Use the maintenance_manager instance
maintenance_manager = MaintenanceManager()

# Wrapper for commands affected by maintenance mode
maintenance_check_wrapper = maintenance_manager.maintenance_mode_check

ADMIN = 6299128233

@app.on_message(filters.private & filters.command("maintenance"))
async def maintenance_command(client, message):
    user_id = message.from_user.id

    if user_id == ADMIN:  # Replace YOUR_ADMIN_USER_ID with the actual admin user ID
        action = message.text.split("/maintenance", 1)[1].strip().lower()

        if action == "on":
            maintenance_manager.turn_on_maintenance()
            await message.reply_text("Maintenance mode is ON")
        elif action == "off":
            maintenance_manager.turn_off_maintenance()
            await message.reply_text("Maintenance mode is OFF")
        else:
            await message.reply_text("Invalid action. Please use '/maintenance on' or '/maintenance off'.")
    else:
        await message.reply_text("You are not authorized to use this command.")
