import random
from translate import Translator
translate = ""
coin = ["heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails", "heads", "tails"]
languages = ["English", "German", "Spanish", "Italian", "Japanese"]
bot = {
    "!! about" : "about_bot: wElComE to tHE cHaT RoOoOoOoOoM, try the command '!! help' :)",
    "!! help" : "help_bot: Here are some commands to help you :) -- '!! help' '!! about' '!! funtranslate <message>' '!! coinFlip'",
    "!! coinflip" : "coinflip_bot: You flipped a " + random.choice(coin) + "!",
    "!! funtranslate" : "funtranslate_bot: " + Translator(to_lang=random.choice(languages)).translate("Enter a message to be translated!")
}

class Chatbot():
    def __init__(self, command):
        if command == "!! coinflip":
            bot["!! coinflip"] = "coinflip_bot: You flipped a " + random.choice(coin) + "!"
    
        self.command = command
    
    def getcommand(self):
        if self.command.startswith("!! funtranslate "):
            translate = self.command.replace("!! funtranslate ", "", 1)
            return Chatbot.funtranslate(translate)
            
        if self.command.startswith("!!") and self.command not in bot:
            return bot.get("!! help")
        return bot.get(self.command)
    
    def checkcommand(self):
        if self.command.startswith("!!") and self.command not in bot:
            return True
        return self.command in bot or self.command.startswith("!! funtranslate")
    
    def funtranslate(self):
        translator = Translator(to_lang=random.choice(languages))
        translation = "funtranslate_bot: " + translator.translate(self)
        return translation