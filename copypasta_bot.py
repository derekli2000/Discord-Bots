import tensorflow as tf
import numpy as np
import time

tf.enable_eager_execution()
gen_copy_model = tf.keras.models.load_model('copypasta_model_dropout_vary.h5')
gen_tifu_model = tf.keras.models.load_model('tifu_model_dropout_vary.h5')

def gen_copy(start_string, size):

    text = open('/Users/derekli/Desktop/Code/Discord Bots/copypastabody.txt', 'rb').read().decode(encoding='utf-8')
    vocab = sorted(set(text))

    # Creating a mapping from unique characters to indices
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    text_as_int = np.array([char2idx[c] for c in text])

    sizes = {
        'small': 100,
        'medium': 150,
        'large': 200
    }

    return generate_text(gen_copy_model, start_string , sizes[size], idx2char, char2idx)

def gen_tifu(start_string, size):

    text = open('/Users/derekli/Desktop/Code/Discord Bots/tifu.txt', 'rb').read().decode(encoding='utf-8')
    vocab = sorted(set(text))

    # Creating a mapping from unique characters to indices
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    text_as_int = np.array([char2idx[c] for c in text])
    
    sizes = {
        'small': 200,
        'medium': 350,
        'large': 500
    }

    return generate_text(gen_tifu_model, start_string , sizes[size], idx2char, char2idx)

def generate_text(model, start_string, size, idx2char, char2idx):

    # Number of characters to generate
    num_generate = size

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):

        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        # We pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
        
        if i+1 >= num_generate and idx2char[predicted_id] != " ":
            num_generate += 1

    return (start_string + ''.join(text_generated))

# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from hyperlink import URL

load_dotenv()
TOKEN = os.getenv('DISCORD_COPYBOT_TOKEN')
GUILD = os.getenv('DISCORD_COPYBOT_GUILD')

client = discord.Client()

# 2
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.command(name='gencopy')
async def gencopy(ctx, start_string: str, size: str ='large'):
    
    response = gen_copy(start_string + " " , size)
    await ctx.send(response)

@bot.command(name='gentifu')
async def gentifu(ctx, start_string: str, size: str ='medium'):
    
    response = gen_tifu(start_string + " " , size)
    await ctx.send(response)

@bot.command(name='help')
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = discord.Color.blue()
    )

    embed.set_author(name="Help")
    embed.add_field(name="!gencopy", value="<string> (optional)<small, medium, large>", inline=False)
    embed.add_field(name="!gentifu", value="<string> (optional)<small, medium, large>", inline=False)

    await ctx.send(author, embed=embed)
bot.run(TOKEN)


# print(generate_text(new_model, start_string=u"hello ",size='large'))