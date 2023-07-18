from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.telegram import TelegramBot  # create this file and class
from app.models import ButtonUsage 



@csrf_exempt
def handle_update(request):
    update = TelegramBot.parse_webhook_data(request.body)
    message = update.message

    if message.text == '/start':
        # Create and send the keyboard with the three buttons
        buttons = [
            {'text': 'Stupid', 'callback_data': 'stupid'},
            {'text': 'Fat', 'callback_data': 'fat'},
            {'text': 'Dumb', 'callback_data': 'dumb'}
        ]
        TelegramBot.send_keyboard(message.chat.id, 'Choose a category:', buttons)

    return HttpResponse()

def get_joke_by_button(button_data):
    # Implement your logic to retrieve and return the appropriate joke based on the button clicked
    if button_data == "stupid":
        return "Why did the scarecrow win an award? Because he was outstanding in his field!"
    elif button_data == "fat":
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif button_data == "dumb":
        return "Why don't skeletons fight each other? They don't have the guts!"
    else:
        return "No joke found for the selected button."
    
def handle_callback_query(request):
    callback_query = TelegramBot.parse_callback_query(request.body)
    message = callback_query.message
    user = message.from_user
    # Get the button data from the callback query
    button_data = callback_query.data

    # Update button usage count in the database
    button_usage, created = ButtonUsage.objects.get_or_create(user=user, button_type=button_data)
    button_usage.count += 1
    button_usage.save()

    # Send the appropriate joke based on the button clicked
    joke = get_joke_by_button(button_data)  # Implement this function to return the joke based on the button
    TelegramBot.send_message(message.chat.id, joke)

    return HttpResponse()


def button_usage_statistics(request):
    button_usage_stats = ButtonUsage.objects.all()
    return render(request, 'button_usage_statistics.html', {'button_usage_stats': button_usage_stats})

