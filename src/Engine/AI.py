import random
import numpy as np
import Engine.constants as const
from Engine.Board import Board
from Engine.Player import Player

class AI:

    def __init__(self):
        self.qtable = dict()
        self.playerTurn = const.RED

    def getQTableValue(self, state, playerTurn, action):
        stateStr = str(state)
        playerTurnStr = str(playerTurn)

        stateDic = self.qtable.get(stateStr)

        if stateDic:
            playerTurnDic = stateDic.get(playerTurnStr)
            if playerTurnDic:
                reward = playerTurnDic.get(action)
                if reward:
                    return reward
        return 0

    def getQTableMaxValue(self, state, playerTurn):
        stateStr = str(state)
        playerTurnStr = str(playerTurn)

        stateDic = self.qtable.get(stateStr)

        if stateDic:
            playerTurnDic = stateDic.get(playerTurnStr)
            if playerTurnDic:
                maxReward = playerTurnDic[max(playerTurnDic, key=playerTurnDic.get)]
                return maxReward
        return 0

    def getQTableMaxValueActionTraining(self, state, playerTurn, board):
        stateStr = str(state)
        playerTurnStr = str(playerTurn)

        stateDic = self.qtable.get(stateStr)

        if stateDic:
            playerTurnDic = stateDic.get(playerTurnStr)
            if playerTurnDic:
                maxAction = max(playerTurnDic, key=playerTurnDic.get)
                return maxAction
        return board.randomMove(playerTurn)

    def getQTableMaxValueAction(self, state, playerTurn, board):
        stateStr = str(state)
        playerTurnStr = str(playerTurn)

        stateDic = self.qtable.get(stateStr)

        if stateDic:
            playerTurnDic = stateDic.get(playerTurnStr)
            if playerTurnDic:
                maxAction = max(playerTurnDic, key=playerTurnDic.get)
                return maxAction
        return board.bestMove(playerTurn)

    def setNewValueQTable(self, state, playerTurn, action, newValue):
        stateStr = str(state)
        playerTurnStr = str(playerTurn)

        if self.qtable.get(stateStr):
            if self.qtable[stateStr].get(playerTurnStr):
                self.qtable[stateStr][playerTurnStr][action] = newValue
                return

        self.qtable[stateStr] = {playerTurnStr: {action: newValue}}

    def getNextPlayerTurn(self):
        if self.playerTurn == const.RED:
            return const.WHITE
        else:
            return const.RED

    def training(self):
        # Hyperparametros
        alpha = 0.1
        gamma = 0.7
        epsilon = 0.1

        #tabuleiro do jogo
        board = Board(
            Player('RED', const.RED),
            Player('BRANCO', const.WHITE),
            None
        )

        for i in range(0, const.NUM_ITERATION):
            state = board.resetBoard()
            done = False
            self.playerTurn = const.RED

            while not done:
                if random.uniform(0, 1) < epsilon or self.playerTurn == const.RED:
                    action = board.randomMove(self.playerTurn)  # Explora o tabuleiro
                else:
                    action = self.getQTableMaxValueActionTraining(state, self.playerTurn, board)  # Exploit os valores aprendidos

                nextState, reward, done = board.moveAI(action, self)

                oldValue = self.getQTableValue(state, self.playerTurn, action)
                nextMax = self.getQTableMaxValue(state, self.playerTurn)

                newValue = (1 - alpha) * oldValue + alpha * (reward + gamma * nextMax)
                self.setNewValueQTable(state, self.playerTurn, action, newValue)

                state = nextState
                self.playerTurn = self.getNextPlayerTurn()
