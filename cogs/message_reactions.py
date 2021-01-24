import discord
import math
import random
import re
from discord.ext import commands
import traceback


class Reaction(commands.Cog, name="message_reactions"):
    """Reacts to various chat messages with emotes or messages."""
    prefix = "react"
    
    def __init__(self, bot):
        self.bot = bot
        # This parses over a string and checks if it ONLY contains emoji.
        self.r_only_emoji = re.compile(
            r"^((?:<:.*?:)(\d*)(?:>)|[\s])*$")
        self.r_get_emoji = re.compile(r"(<:.*?:)(\d*)(>)")  # Finds a discord emoji in a string.

        # There must be at least this many messages since the last time the "good night" wishes triggered.
        self.sleep_counter = 20
        
        self.rc_furry = self.bot.Chance({
            # Very likely
            "🦊": 150,  # Fox
            "🐺": 150,  # Wolf
            
            # Common
            "🐱": 100,  # Cat face
            "🐈": 100,  # Cat
            "🐯": 100,  # Dog?
            "🦦": 75,  # Otter!
            "🐶": 75,  # Dog alt
            "🕊️": 75,  # Bird

            # Unlikely
            "🦝": 50,  # raccoon
            "🐈‍⬛": 50,  # Black cat
            "🦁": 50,  # lion?
            "🐹": 50,  # hamster
            "🐰": 50,  # rabbit
            "🐿": 50,  # Chipmunk
            "🦔": 50,  # Hedgehog
            "🦘": 50,  # Kangaroo
            "🐑": 50,  # Sheep
            "🐦": 50,  # Bird
            
            # Very unlikely
            "🐬": 40,  # Dolphin!
            "🦜": 40,  # Parrot
            "🦚": 30,  # Peacock
            "🐷": 35,  # pig?
            "🐄": 25,  # pig body.
            "🦒": 30,  # giraffe
            
            # Special
            "🐲": 20,  # Dragon face
            "🕷": 10,  # spider
            "🦂": 10,  # mosquito
            "🍌": 10,  # banana
            "🥝": 10,  # kiwi (the fruit)
            "🥥": 10,  # coconut (the fruit)
            "<:furry:772239467544576021>": 10,  # Custom Clyde gay emote
        })
        self.rc_goodnight = self.bot.Chance({
            "Sleep well!": 100,
            "Good night <3": 100,
            "Oyasuminasai!": 100,
            "Sweet dreams~": 100,
            "Gnight!": 100,
            
            "To the land of imagination with you!": 70,
            "bueno dormir :flag_es:": 70,
            "お休み！": 70,
            
            "https://www.youtube.com/watch?v=Udj-o2m39NA": 50,  # Go the fuck to sleep story
            "Nya uwu x3 s-sleep w-well~~~ kyaaah!": 50,  # gross gay furry
        })
        self.rc_minion = self.bot.Chance({
            "<:eld_eye:644875878177964052>": 1,
            "<:eld_happy:644875878416908336>": 1,
            "<:eld_minion:644875880094498826>": 1,
            "<:eld_sad:644876502957162506>": 1,
            "<:eld_unknown:644876503162552321>": 1,
        })

    @commands.Cog.listener()
    async def on_message(self, message):
        if not await self.bot.has_perm(message, message_on_fail=False): return
        self.sleep_counter -= 1
        msg = message.content.lower()

        try:
            if re.search(r"\bhot\b", msg):
                await message.add_reaction("<:bap:771864166294224906>")
        except:
            traceback.print_exc()
        
        try:
            if re.search(r"\bgay\b", msg):
                await message.add_reaction("🅾️")
                await message.add_reaction("🇼")
                await message.add_reaction("🅾")
        except:
            traceback.print_exc()
        
        try:
            if re.search(r"(\s|^)(\:c|\:<|>\:|\:\(|\)\:|\;w\;|\;v\;|\;-\;|\;\;|\:\'\(|\:\'c|\:CC|T_T|T-T)(\s|$)", msg):
                await message.add_reaction("<:sad:773036515189719046>")
        except:
            traceback.print_exc()
        
        try:
            if re.search(self.r_only_emoji, message.content):  # Message only contains emoji
                for match in re.findall(self.r_get_emoji, message.content):
                    val = "".join(match)
                    await message.add_reaction(val)
        except:
            traceback.print_exc()
        
        try:
            if re.search(r"(gnight|good night|sleep well)", msg) and self.sleep_counter <= 0:
                react = self.rc_goodnight.get_value()
                await message.channel.send(react)
                self.sleep_counter = 20
        except:
            traceback.print_exc()
        
        try:
            if re.search(r"(\s|\b|^)(f+u+r+(i+e+s+|y*))(\s|\b|$)",
                         msg):  # Match any f before u before r combination, with an optional y at the end. Essentially, any possibly way to spell "fur" or "furry".
                react = self.rc_furry.get_value()
                await message.add_reaction(react)
        except:
            traceback.print_exc()
        
        # Attempt to react to built-in emoji.
        # What I'm doing here is trying to "react" using the contents of the user's message.
        # It should only succeed if the user's message contains a single built in emoji.
        try:
            await message.add_reaction(message.content)
        except:
            pass
        
        try:
            if re.search(r"(hotel?)", msg):
                await message.channel.send("trivago.")
        except:
            traceback.print_exc()

        try:
            if re.search(r"(~)", msg):
                await message.add_reaction("<:tilde:802886844634759168>")
        except:
            traceback.print_exc()

        try:
            if re.search(r"(minion)", msg):
                await message.add_reaction(self.rc_minion.get_value())
        except:
            traceback.print_exc()

        try:
            # TODO: Add more variations of this word.
            if re.search(r"(quack)", msg):
                quack_file = discord.File("./attachments/quak.wav")
                await message.channel.send(file=quack_file)
        except:
            traceback.print_exc()
    
    @commands.command(name=f"{prefix}.chance")
    async def chance(self, ctx):
        """
        Returns the percentage chance of a given entry in rc_furry to be used as a reaction.
        Arguments:
            val: The emoji to check for.
        Example:
            c.react.chance val=":furry:"
            c.react.chance val=":parrot:"
        """
        if not await self.bot.has_perm(ctx): return
        char = self.bot.get_variable(ctx.message.content, key="val", type="str")
        try:
            chance = self.rc_furry.get_chance(char, weight=False) * 100
            await ctx.send(f"{chance}%")
        except ValueError:
            await ctx.send("Not a valid reaction!")

    # TODO: Command that removes reactions on the last message the user sent. So I can go "gr" at HB going "owo" and he runs away.
    
    def text_to_emoji(self, string):
        # TODO: This.
        # TODO: Display what HB believes it can say, and ask if that's okay.
        # IDEA: Maybe allow people to do this to a word of their choosing.
        # IDEA: Allow people to specify a message to react to with an ID?
        text_to_emoji_dict = {
            "a": ["🅰️"],
            "b": ["🅱️"],
            "c": ["©️,©"],
            "d": [],
            "e": [],
            "f": [],
            "g": [],
            "h": [],
            "i": [],
            "j": [],
            "k": [],
            "l": [],
            "m": [],
            "n": [],
            "o": [],
            "p": [],
            "q": [],
            "r": [],
            "s": [],
            "t": [],
            "u": [],
            "v": [],
            "w": [],
            "x": [],
            "y": [],
            "z": ["💤"],
            
        }
        pass


def setup(bot):
    bot.add_cog(Reaction(bot))
