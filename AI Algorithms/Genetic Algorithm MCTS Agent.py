# SOLVER CLASSES WHERE AGENT CODES GO
from helper import *
import random
import math


# Base class of agent (DO NOT TOUCH!)
class Agent:
    def getSolution(self, state, maxIterations):
        return []       # set of actions


#####       EXAMPLE AGENTS      #####

# Do Nothing Agent code - the laziest of the agents
class DoNothingAgent(Agent):
    def getSolution(self, state, maxIterations):
        if maxIterations == -1:     # RIP your machine if you remove this block
            return []

        #make idle action set
        nothActionSet = []
        for i in range(20):
            nothActionSet.append({"x":0,"y":0})

        return nothActionSet

# Random Agent code - completes random actions
class RandomAgent(Agent):
    def getSolution(self, state, maxIterations):

        #make random action set
        randActionSet = []
        for i in range(20):
            randActionSet.append(random.choice(directions))

        return randActionSet




#####    ASSIGNMENT 1 AGENTS    #####


# BFS Agent code
class BFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        
        # YOUR CODE HERE




        return []                       #remove me
        #return bestNode.getActions()   #uncomment me



# DFS Agent Code
class DFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None

        # YOUR CODE HERE




        return []                       #remove me
        #return bestNode.getActions()   #uncomment me



#####    ASSIGNMENT 2 AGENTS    #####



# AStar Agent Code
class AStarAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        balance = 1
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        Node.balance = balance

        #initialize priority queue
        queue = PriorityQueue()
        queue.put(Node(state.clone(), None, None))
        visited = set()

        while (iterations < maxIterations or maxIterations <= 0) and queue.qsize > 0:
            iterations += 1

            ## YOUR CODE HERE ##




        return bestNode.getActions()


# Hill Climber Agent code
class HillClimberAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        
        seqLen = 50            # maximum length of the sequences generated
        coinFlip = 0.5          # chance to mutate

        #initialize the first sequence (random movements)
        bestSeq = []
        for i in range(seqLen):
            bestSeq.append(random.choice(directions))

        #mutate the best sequence until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1
            
            ## YOUR CODE HERE ##




        #return the best sequence found
        return bestSeq  



#####    ASSIGNMENT 3 AGENTS    #####


# Genetic Algorithm code
class GeneticAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)

        iterations = 0
        seqLen = 50             # maximum length of the sequences generated
        popSize = 10            # size of the population to sample from
        parentRand = 0.5        # chance to select action from parent 1 (50/50)
        mutRand = 0.3           # chance to mutate offspring action

        bestSeq = []            #best sequence to use in case iterations max out

        #initialize the population with sequences of 50 actions (random movements)
        population = []
        for p in range(popSize):
            bestSeq = []
            for i in range(seqLen):
                bestSeq.append(random.choice(directions))
            population.append(bestSeq)
        

        #mutate until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1
            tempPop = []
            check = 0
            #1. evaluate the population
            for pop in population:
                bestSeq = []
                testState = state.clone()
                for act in pop:              
                    testState.update(act['x'], act['y'])
                    bestSeq.append(act)
                    if testState.checkWin():
                        check = 1
                        break
                if check == 1:
                    break
                ftness = getHeuristic(testState)
                tempPop.append([ftness, pop])

            if check == 1:
                break

            #2. sort the population by fitness (low to high)
            tempPop.sort(key = lambda x: x[0])

            #2.1 save bestSeq from best evaluated sequence
            bestSeq = tempPop[0][1]

            #3. generate probabilities for parent selection based on fitness
            dictionary = {
                1 : 0,
                2 : 0,
                3 : 0,
                4 : 0,
                5 : 0,
                6 : 1,
                7 : 1,
                8 : 1,
                9 : 1,
                10 : 2,
                11 : 2,
                12 : 2,
                13 : 3,
                14 : 3,
                15 : 4
            }
            #4. populate by crossover and mutation
            new_pop = []
            for i in range(int(popSize/2)):
                #4.1 select 2 parents sequences based on probabilities generated
                par1 = []
                par2 = []
                r1 = random.randint(1, 15)
                r2 = random.randint(1, 15)
                index1 = dictionary.get(r1)
                index2 = dictionary.get(r2)
                par1 = tempPop[index1][1]
                par2 = tempPop[index2][1]

                #4.2 make a child from the crossover of the two parent sequences
                offspring = []
                for i in range(len(par1)):
                    if random.random() < 0.5:
                        offspring.append(par1[i])
                    else:
                        offspring.append(par2[i])

                #4.3 mutate the child's actions
                for k in range(len(offspring)):
                    if random.random() < 0.3:
                        offspring[k] = random.choice(directions)

                #4.4 add the child to the new population
                new_pop.append(list(offspring))


            #5. add top half from last population (mu + lambda)
            for i in range(int(popSize/2)):
                new_pop.append(tempPop[i][1])


            #6. replace the old population with the new one
            population = list(new_pop)

        #return the best found sequence 
        return bestSeq

# MCTS Specific node to keep track of rollout and score
class MCTSNode(Node):
    def __init__(self, state, parent, action, maxDist):
        super().__init__(state,parent,action)
        self.children = []  #keep track of child nodes
        self.n = 0          #visits
        self.q = 0          #score
        self.maxDist = maxDist      #starting distance from the goal (heurstic score of initNode)

    #update get children for the MCTS
    def getChildren(self,visited):
        #if the children have already been made use them
        if(len(self.children) > 0):
            return self.children

        children = []
        for d in directions:
            childState = self.state.clone()
            crateMove = childState.update(d["x"], d["y"])
            if childState.player["x"] == self.state.player["x"] and childState.player["y"] == self.state.player["y"]:
                continue
            if crateMove and checkDeadlock(childState):
                continue
            if getHash(childState) in visited:
                #print('seen')
                continue
            children.append(MCTSNode(childState, self, d, self.maxDist))

        self.children = list(children)    #save node children to generated child

        return children

    #calculates the score the distance from the starting point to the ending point (closer = better = larger number)
    def calcEvalScore(self,state):
        return self.maxDist - getHeuristic(state)

    #compares the score of 2 mcts nodes
    def __lt__(self, other):
        return self.q < other.q

    def __str__(self):
        return str(self.q) + ", " + str(self.n) + ' - ' + str(self.getActions())


# Monte Carlo Tree Search Algorithm code
class MCTSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        initNode = MCTSNode(state.clone(), None, None, getHeuristic(state))

        while(iterations < maxIterations):
            #print("\n\n---------------- ITERATION " + str(iterations+1) + " ----------------------\n\n")
            iterations += 1

            #mcts algorithm
            rollNode = self.treePolicy(initNode)
            score = self.rollout(rollNode)
            self.backpropogation(rollNode, score)

            #if in a win state, return the sequence
            if(rollNode.checkWin()):
                return rollNode.getActions()

            #set current best node
            bestNode = self.bestChildUCT(initNode)

            #if in a win state, return the sequence
            try:
                if(bestNode.checkWin()):
                    return bestNode.getActions()
            except:
                raise


        #return solution of highest scoring descendent for best node
        print("timeout")
        return self.bestActions(bestNode)
        

    #returns the descendent with the best action sequence based
    def bestActions(self, node):
        bestActionSeq = []
        while(len(node.children) > 0):
            node = self.bestChildUCT(node)

        return node.getActions()


    ####  MCTS SPECIFIC FUNCTIONS BELOW  ####

    #determines which node to expand next
    def treePolicy(self, rootNode):
        curNode = rootNode
        visited = []
        
        ## YOUR CODE HERE ##
        unexplored = []
        for x in rootNode.children:
            if x.n > 0:
                visited.append(x.getHash())
        while curNode.getChildren(visited):
            nodeCh = curNode.getChildren(visited)
            for ch in nodeCh:
                if ch.n == 0:
                    unexplored.append(ch)
                elif ch not in visited:
                    visited.append(ch.getHash())
            if not unexplored:
                curNode = self.bestChildUCT(curNode)
            else:
                ind = random.randint(0, len(unexplored) - 1)
                curNode = unexplored[ind]
                break

        return curNode



    # uses the exploitation/exploration algorithm
    def bestChildUCT(self, node):
        c = 1               #c value in the exploration/exploitation equation
        bestChild = None

        ## YOUR CODE HERE ##
        bestScore = -1
        for ch in node.children:
            if ch.n == 0:
                continue
            term1 = ch.q/ch.n
            term2 = (2 * math.log(node.n))/ch.n
            term3 = c * math.sqrt(term2)
            result = term1 + term3
            if result < 0:
                result = 0
            if result > bestScore:
                bestScore = result
                bestChild = ch

        return bestChild



     #simulates a score based on random actions taken
    def rollout(self,node):
        numRolls = 7        #number of times to rollout to

        ## YOUR CODE HERE ##
        newState = node.state.clone()
        for i in range(numRolls):
            moves = random.choice(directions)
            newState.update(moves['x'], moves['y'])
            if newState.checkWin():
                break
        return node.calcEvalScore(newState)



     #updates the score all the way up to the root node
    def backpropogation(self, node, score):
        ## YOUR CODE HERE ##
        currentNode = node
        while currentNode != None:
            currentNode.n += 1
            currentNode.q += score
            currentNode = currentNode.parent

        return
        

