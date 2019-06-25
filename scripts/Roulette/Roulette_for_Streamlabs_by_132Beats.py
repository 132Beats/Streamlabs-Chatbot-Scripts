import clr
import sys
import json
import os
import ctypes
import codecs
import sqlite3

ScriptName = "Roulette Minigame"
Website = "https://github.com/132Beats"
Description = "Roulette Minigame for Streamlabs Chatbot"
Creator = "132Beats"
Version = "0.9.0"

configFile = "config.json"
settings = {}

def ScriptToggled(state):
	return

def Init():
	global settings

	path = os.path.dirname(__file__)
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"command": "!roulette",
			"permission": "Everyone",
			"rewardZero": 14,
			"rewardColor": 2,
			"emoteWon" : "VoteYea",
			"emoteLost" : "VoteNay",
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 60,
			"onCooldown": "$command ist noch für $cd Sekunden auf Cooldown Kollege!",
			"rollTimer": 60,
			"responseNotEnoughPoints": "$user du hast nur $points $currency",
			"responseWon": "$user hat richtig gestzt! $won und gewinnt $reward $currency",
			"responseLost": "$user hat verkackt $lost und verliert seinen Einsatz von $reward $currency n"
		}
	droptables()

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)
		if data.GetParamCount() <= 2:
			if data.GetParam(1) == 'info':
				outputMessage = settings["infomessage"]
			elif data.GetParam(1) == 'cooldown':
				outputMessage = settings["cooldowninfo"]
			else:
				outputMessage = settings["infomessage"]
		elif data.GetParamCount() > 3:
			outputMessage = settings["tooManyArguments"]
		else:
			if !Parent.HasPermission(data.User, settings["permission"], ""):
				outputMessage = settings["noPermission"]
			else:
				if Parent.IsOnCooldown(ScriptName, settings["command"]):
					cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
					outputMessage = settings["onCooldown"]
				else:
					if data.GetParam(1) != settings["black"] and data.GetParam(1) != settings["red"] and data.GetParam(1) != settings["zero"]:
						outputMessage = settings["cannotIdentifyColor"]
					else:
						if data.GetParam(2) == "all":
							costs = points
							numberidentified = true
						elif data.GetParam(2) == "max":
							costs = settings["maxEntry"]
							numberidentified = true
						else:
							try:
								costs = int(data.GetParam(2))
								if costs == 0:
									outputMessage = settings["cannotIdentifyNumberOfEntry"]
									numberidentified = false
								else:
									numberidentified = true
							except:
								outputMessage = settings["cannotIdentifyNumberOfEntry"]
								numberidentified = false

						if numberidentified:
							if costs > points:
								outputMessage = settings["responseNotEnoughPoints"]
							elif costs > settings["maxEntry"]
								outputMessage = settings["tooMuchEntry"]
							else:
								connection = sqlite3.connect("dicebets.db")
								cursor = connection.cursor()
								sql_command = """INSERT INTO dicebets(dbuserId,target,amount) VALUES (puser,ptarget,pamount);"""
								sql_command = sql_command.format(puser=userId,ptarget=data.GetParam(1),pamount=data.GetParam(2))
								cursor.execute(sql_command)
								connection.commit()
								connection.close()
								Parent.RemovePoints(userId, username, costs)







				
				#WIP
		userId = data.User			
		username = data.UserName

		if settings["useCustomCosts"] and (data.GetParamCount() == 3):
			try: 
				costs = int(data.GetParam(2))
			except:
				if data.GetParam(2) == 'all': 
					costs = points

		if (costs > Parent.GetPoints(userId)) or (costs < 1):
			outputMessage = settings["responseNotEnoughPoints"]
		elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"])):
			if settings["useCooldownMessages"]:
				cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
				cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
				outputMessage = settings["onCooldown"]
			else:
				outputMessage = ""
		else:
			Parent.RemovePoints(userId, username, costs)

			coin = Parent.GetRandom(0, 15)
			reward = ""

			if coin == 0:
				outputMessage = (settings["responseWon"])
				reward = costs * settings["reward"]
				Parent.AddPoints(userId, username, int(reward))
			else:
				outputMessage = settings["responseLost"]
				reward = costs

			outputMessage = outputMessage.replace("$reward", str(reward))

			if settings["useCooldown"]:
				Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
				Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])

		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$won", settings["emoteWon"])
		outputMessage = outputMessage.replace("$lost", settings["emoteLost"])
		outputMessage = outputMessage.replace("$currency", Parent.GetCurrencyName())
		outputMessage = outputMessage.replace("$command", settings["command"])

		Parent.SendStreamMessage(outputMessage)
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def Tick():
	return

def dropTables():
	connection = sqlite3.connect("dicebets.db")
	cursor = connection.cursor()
	cursor.execute("""DROP TABLE IF EXISTS dicebets""")
	sql_command = """
	CREATE TABLE dicebets ( 
	id INT NOT NULL AUTO_INCREMENT,
	dbuserId CHAR(32),
	target INT, 
	amount INT,
	PRIMARY KEY (id) );"""
	cursor.execute(sql_command)
	connection.commit()
	connection.close()
	return