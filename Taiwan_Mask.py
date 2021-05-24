import json
import requests
import time
import discord
from discord.ext import commands
import re

url = 'https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json'

count = 0

bot = commands.Bot(command_prefix = '!')

phone = ''
phoneb = False

async def getjson():
	try:
		r = requests.get(url)
		maskjson = json.loads(str(r.text))
		return maskjson
	except Exception as e:
		print(e)

async def fetchjson(ctx,keyword):
	global phone,phoneb
	data = await getjson()
	fetchone = data['features']
	for x in range(count,len(fetchone)):
		name = fetchone[x]['properties']['name']
		address = fetchone[x]['properties']['address'].replace('臺','台')
		adult = fetchone[x]['properties']['mask_adult']
		child = fetchone[x]['properties']['mask_child']
		lat = fetchone[x]['geometry']['coordinates'][1]
		lng = fetchone[x]['geometry']['coordinates'][0]
		try:
			phone = fetchone[x]['properties']['phone']
			phoneb = True
		except:
			phoneb = False
		try:
			if keyword in address:
				if adult != 0 or child != 0:
					await sendembed(ctx,name,address,adult,child,lat,lng)
					time.sleep(3)
					if adult == 0 and child == 0:
						await sendnostock(ctx)

		except Exception as e:
			print(e)

async def sendembed(ctx,name,address,adult,child,lat,lng):
	if phoneb == True:
		embed = discord.Embed(title = name,description = '地址：{}\n電話：{}\n成人口罩：{}, 兒童口罩：{}\n[**點我打開地圖**](http://maps.google.com/?q={},{})\n:mask: :mask: :mask: :mask: :mask: '.format(address,phone,adult,child,lat,lng))
	else:
		embed = discord.Embed(title = name,description = '地址：{}\n成人口罩：{}, 兒童口罩：{}\n[**點我打開地圖**](http://maps.google.com/?q={},{})\n:mask: :mask: :mask: :mask: :mask: '.format(address,adult,child,lat,lng))
	embed.set_footer(text = '口罩查詢機器人 by JiouHao')
	await ctx.send(embed=embed)

async def sendnostock(ctx):
	await ctx.send('**:thinking: 沒有任何一家有口罩庫存,請隔天再嘗試,謝謝!!:thinking: **')

@bot.event
async def on_ready():
	print('{} ------- Hello!!'.format(bot.user.name))


@bot.command()
async def 口罩(ctx,keyword):
	await ctx.send('**:face_with_monocle: 正在查找關鍵字中的藥局or衛生所,請耐心等候:face_with_monocle: **')
	await ctx.send('**:eye:  搜尋中   :regional_indicator_s: :regional_indicator_e: :regional_indicator_a: :regional_indicator_r: :regional_indicator_c: :regional_indicator_h: :regional_indicator_i: :regional_indicator_n: :regional_indicator_g:  :eye: **')
	try:
		await fetchjson(ctx,keyword)
		await ctx.send(':partying_face: `已搜索完畢,Thanks!!` **如無顯示結果,請更改地址關鍵字,謝謝**:partying_face:')
	except Exception as e:
		await ctx.send('**:thinking: 找不到附近有口罩的診所或衛生局,請更改關鍵字:thinking: **')

bot.run('BOT TOKEN HERE')
