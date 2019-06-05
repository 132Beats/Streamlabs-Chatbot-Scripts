import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Dice Minigame mit MaxEinsatz"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Dice Minigame mit MaxEinsatz for Streamlabs Bot"
Creator = "Bare7a und 132Beats"
Version = "1.2.8.1"

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
			"command": "!dice",
			"permission": "Everyone",
			"useCustomCosts" : True,
			"costs": 10,
			"maxcost": 3000,
			"reward11": 0,
			"reward12": 2,
			"reward13": 2,
			"reward14": 3,
			"reward15": 3,
			"reward16": 4,
			"reward17": 5,
			"reward18": 10,
			"useCooldown": True,
			"useCooldownMessages": True,
			"cooldown": 0,
			"onCooldown": "$user, $command ist noch auf Cooldown fuer $cd Minuten!",
			"userCooldown": 120,
			"onUserCooldown": "$user, $command ist fuer dich immernoch auf Cooldown fuer $cd Minuten!",
			"prefix": "[Dice] ",
			"responseNotEnoughPoints": "$user du hast nur $points $currency.",
			"responseWon": "$user wuerfelt: $dices Eine $dicesSum, du gewinnst $reward $currency!",
			"responseLost": "$user wuerfelt: $dices Eine $dicesSum, du verlierst deinen Einsatz und hast nur noch $newpointsafterloss $currency.",
			"tooMuchEinsatz": "$user Bruder, so viel Einsatz ist nicht drin",
			"cooldownCheck": "Der Cooldown von $command ist $userCooldown Sekunden.",
			"infomessage": "Bei $command wuerfelt mal 3 Wuerfel, je hoeher die Augenzahlen, desto mehr Gewinn!"
		}

def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() == settings["command"] and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		outputMessage += settings["prefix"]
		userId = data.User			
		username = data.UserName
		points = Parent.GetPoints(userId)

		if settings["useCustomCosts"] and (data.GetParamCount() == 2):
			try:
				costs = int(data.GetParam(1))
			except:
				if data.GetParam(1) == 'all': 
					costs = points
				else:
					costs = settings["costs"] 
		else:
			costs = settings["costs"]

		if data.GetParam(1) == 'cooldown':
			outputMessage += settings["cooldownCheck"]
		elif data.GetParam(1) == 'info':
			outputMessage += settings["infomessage"]
		elif costs > settings["maxcost"]:
			outputMessage += settings["tooMuchEinsatz"]
		else:
			if (costs > Parent.GetPoints(userId)) or (costs < 1):
				outputMessage += settings["responseNotEnoughPoints"]
			elif settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, settings["command"]) or Parent.IsOnUserCooldown(ScriptName, settings["command"], userId)):
				if settings["useCooldownMessages"]:
					if Parent.GetCooldownDuration(ScriptName, settings["command"]) > Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId):
						cdi = Parent.GetCooldownDuration(ScriptName, settings["command"])
						cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
						outputMessage += settings["onCooldown"]
					else:
						cdi = Parent.GetUserCooldownDuration(ScriptName, settings["command"], userId)
						cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2) 
						outputMessage += settings["onUserCooldown"]
					outputMessage = outputMessage.replace("$cd", cd)
				else:
					outputMessage = ""
			else:
				Parent.RemovePoints(userId, username, costs)

				dice1 = Parent.GetRandom(1, 7)
				dice2 = Parent.GetRandom(1, 7)
				dice3 = Parent.GetRandom(1, 7)
				dices = "[" + str(dice1) + "] [" + str(dice2) +"] [" + str(dice3) + "]"
				dicesSum = dice1 + dice2 + dice3
				reward = ""

				if dicesSum < 11:
					outputMessage += settings["responseLost"]
					reward = costs
				elif dicesSum == 11:
					if settings["reward11"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward11"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 12:
					if settings["reward12"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward12"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 13:
					if settings["reward13"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward13"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 14:
					if settings["reward14"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward14"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 15:
					if settings["reward15"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward15"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 16:
					if settings["reward16"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward16"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 17:
					if settings["reward17"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward17"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs
				elif dicesSum == 18:
					if settings["reward18"] > 0:
						outputMessage += (settings["responseWon"])
						reward = costs * settings["reward18"]
						Parent.AddPoints(userId, username, int(reward))
					else:
						outputMessage += settings["responseLost"]
						reward = costs



				outputMessage = outputMessage.replace("$dice1", str(dice1))
				outputMessage = outputMessage.replace("$dice2", str(dice2))
				outputMessage = outputMessage.replace("$dice3", str(dice3))
				outputMessage = outputMessage.replace("$dicesSum", str(dicesSum))
				outputMessage = outputMessage.replace("$dices", str(dices))
				outputMessage = outputMessage.replace("$reward", str(reward))

				if settings["useCooldown"]:
					Parent.AddUserCooldown(ScriptName, settings["command"], userId, settings["userCooldown"])
					Parent.AddCooldown(ScriptName, settings["command"], settings["cooldown"])
		
		outputMessage = outputMessage.replace("$cost", str(costs))
		outputMessage = outputMessage.replace("$userCooldown", str(settings["userCooldown"]))
		outputMessage = outputMessage.replace("$user", username)
		outputMessage = outputMessage.replace("$points", str(points))
		outputMessage = outputMessage.replace("$newpointsafterloss", str(points-costs))
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
