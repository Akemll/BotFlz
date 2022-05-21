import discord, asyncio
from discord.ext import commands

cargos = [971183487858147358, 971183487858147360, 971183487858147359]
bot = commands.Bot(command_prefix="!", help_command=None)
db = db["Bot2"]


async def text(conteudo):
        texto = ""
        contar = 0
        for e in conteudo:
            if contar != 0:
                texto += f" {e}"
            else:
                texto = e
            contar += 1
        return texto


@bot.event
async def on_ready():
    print("tou on")

@bot.event
async def on_member_join(ctx):
    try:
        cargo = discord.utils.get(ctx.guild.roles, id="")
        await ctx.add_roles(cargo)
    except Exception as erro:
        print(erro)

@commands.has_permissions(administrator=True)
@bot.command()
async def cda(ctx, user:discord.Member, *arg):
    if ctx.author.id == user.id:
        return
    else:
        argumentos = await text(arg)



@commands.has_permissions(administrator=True)
@bot.command()
async def ban(ctx, user:discord.Member, *arg):
    if user.id == ctx.author.id:
        return
    try:
        argumentos = await text(arg)
        await user.ban(reason=argumentos)
        mensagem = await ctx.send(":white_check_mark: | **Usuário banido com sucesso!**")
        await asyncio.sleep(5)
        await mensagem.delete()
    except Exception:
        pass

@ban.error
async def ban_error(ctx, erro):
    mensagem = await ctx.send(":x: | Ocorreu um erro na execução do comando, verifique se o utilizou certo.")
    await asyncio.sleep(4)
    await mensagem.delete()

@commands.has_permissions(administrator=True)
@bot.command()
async def adv(ctx, user:discord.Member):
    global cargos
    if ctx.author.id == user.id:
        return
    if not db.adv.find_one({"Usuário": user.id}):
        db.adv.insert_one({"Usuário": user.id, "Adv": 0})
    dados = db.adv.find_one({"Usuário": user.id})
    if dados["Adv"] != 3:
        dados["Adv"] += 1
        try:
            cargo = discord.utils.get(ctx.author.guild.roles, id=cargos[(dados["Adv"] - 1)])
            await user.add_roles(cargo)
            await ctx.send(f":white_check_mark: | {ctx.author.mention} o usuário foi advertido com sucesso.")
        except Exception as erro:
            print(erro)
    else:
        await ctx.send(f":x: | {ctx.author.mention} esse usuário já tem o máximo de advertência(3)")

@ban.error
async def adv_error(ctx, erro):
    mensagem = await ctx.send(":x: | Ocorreu um erro na execução do comando, verifique se o utilizou certo.")
    await asyncio.sleep(4)
    await mensagem.delete()
