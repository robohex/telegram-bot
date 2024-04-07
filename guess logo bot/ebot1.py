import random

# Logo guessing bot class
class LogoGuessingBot:
    def __init__(self):
        self.logos = ["Google", "Apple", "Microsoft", "Amazon", "Facebook", "Tesla"]
    
    def guess(self):
        # Choose a random logo
        selected_logo = random.choice(self.logos)
        # Give the user some hints about the logo
        print("Welcome to the logo guessing game!")
        print("The logo name contains", len(selected_logo), "letters.")
        print("The first letter is:", selected_logo[0])
        print("The last letter is:", selected_logo[-1])
        print("Can you guess it?")

        guess = input("Enter your guess: ")

        # Check if the guess is correct
        if guess.lower() == selected_logo.lower():
            print("Congratulations! You guessed it right.")
        else:
            print("Sorry, you guessed it wrong. The correct answer is:", selected_logo)

# Start the bot
bot = LogoGuessingBot()
bot.guess()
