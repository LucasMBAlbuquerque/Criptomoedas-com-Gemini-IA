from discord.ext import commands
from requests import Session
from decouple import config
import discord.embeds
import json
import locale
import google.generativeai as genai

class Crypto(commands.Cog):
    """ Preço de criptos usando Gemini IA """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def preco(self, ctx, coin, base=None):
        '''Comando para preço de cryptos'''
        try:
            # Configuração do modelo generativo
            token_gemini = config("TOKEN_GEMINI")
            genai.configure(api_key=token_gemini)
            generation_config = {
                "candidate_count": 1,
                "temperature": 1,
                "top_p": 0.8,
            }
            safety_setting = {
                "HARASSMENT": "BLOCK_NONE",
                "HATE": "BLOCK_NONE",
                "SEXUAL": "BLOCK_NONE",
                "DANGEROUS": "BLOCK_NONE",
            }
            url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


            if base == 'dolar' or base == 'usd' or base == None:
                base = 'USD'
            elif base == 'real' or base == 'brl':
                base = 'BRL'
            elif base == 'euro':
                base = 'EUR'
            else:
                base = base.upper()
            coin = str(coin)

            parameters = {
                'symbol':f'{coin}',
                'convert':f'{base}'
            }
            if len(coin) == 3:
                parameters = {
                    'symbol':f'{coin.upper()}',
                    'convert':f'{base}'
                }
            else:
                parameters = {
                    'slug':f'{coin.lower()}',
                    'convert':f'{base}'
                }
            
            TOKENCMK = config("CMK")
            headers ={
                'Accepts':'application/json',
                'X-CMC_PRO_API_KEY':TOKENCMK
            }
            session = Session()
            session.headers.update(headers)
            response = session.get(url, params=parameters)
            d = json.loads(response.text)
            idd = list(d['data'])
            nome = d['data'][idd[0]]['slug']
            simbolo = d['data'][idd[0]]['symbol'].lower()
            if d:
                model = genai.GenerativeModel(model_name='gemini-pro', generation_config=generation_config,safety_settings=safety_setting)
                chat = model.generate_content(f"Você é um bot que analisa dados de criptomoedas de uma API em json e retorna um resumo em um parágrafo sobre a requisição. No resumo deve conter apenas o nome da criptomoeda, seu preço, mudança na última hora, 24 horas e 7 dias e ranking em marketcap. Ao lado de cada porcentagem coloque um emoji que represente a emoção da variação de preço. Use apenas emojis de rosto. Destaque em negrito os pontos mais importantes. arredonde os resultados para 2 casas decimais: {d}")
                embed_cmk = discord.Embed(
                    title = 'Cripto Gemini',
                    url = 'https://github.com/LucasMBAlbuquerque',
                    description=chat.text,
                    color=discord.Color.blue()
                )
                embed_cmk.set_thumbnail(url=f'https://cryptologos.cc/logos/{nome}-{simbolo}-logo.png?')
                await ctx.send(embed=embed_cmk)
            else:
                await ctx.send(f'O par **{coin}/{base}** é inválido')        
        except Exception as error:    
            await ctx.send('Ocorreu um erro')  
            print(error)

async def setup(bot):
    await bot.add_cog(Crypto(bot))
