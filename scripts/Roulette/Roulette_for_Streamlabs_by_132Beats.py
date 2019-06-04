import clr
import sys
import json
import os
import ctypes
import codecs

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

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)

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