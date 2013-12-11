import pymc as mc;
import pylab as pl;
import numpy as np;
#######ALL THESE PARAMETERS ARE ARBITRARY AND SHOULD BE TRAINED OR BETTER CHOSEN OR SOMETHING
#probability of a guess
pG = .1
#probability of a slip
pS = .3
#compensatory probability (p(correct | partial knowledge of reqs), extra arbitrary - should probably be contextual)
pC = .4
#basic probability a student already knows a concept given we know they know all the prereqs.  Coinflip?  
pK = .5 #p(Knowledge)
#probability a student knows a concept given they miss knowledge on one or more prereqs
pU = .1 #p(Understanding)
#probability a student knows a concept given that they DON'T know ANY of the prereq(s)
pM = .05 #p(Magic)


def performInference(responses):
    #this is a really hacky solution for now until I can spend more time figuring out how to do this more programatically 
    def stopGapDependencies(name, dependencies):
        p = 0;
        if len(dependencies) == 1:
            dep = dependencies[0]
            #for reference, the semantics of this are if dep=1, p=pK, else if dep=0, p=pM
            p = mc.Lambda(name, lambda dep=dep: pl.where(dep, pK, pM))
        elif len(dependencies) == 2:
            dep = dependencies[0]
            dep2 = dependencies[1]
            p = mc.Lambda(name, lambda dep=dep, dep2=dep2: pl.where(dep2, pl.where(dep, pK, pU), pl.where(dep, pU, pM)))
        elif len(dependencies) == 3:
            dep = dependencies[0]
            dep2 = dependencies[1]
            dep3 = dependencies[2]
            p = (mc.Lambda(name, lambda dep=dep, dep2=dep2, dep3=dep3: pl.where(dep3, pl.where(dep2, pl.where(dep, pK, pU),
                                                                                               pl.where(dep, pU, pU/2)), pl.where(dep2, pl.where(dep, pU, pU/2),
                                                                                                                                  pl.where(dep, pU/2, pM)))))
        else:
            print "This is hacky and doesnt work for nodes with more than 3 dependencies"
        return p
    concepts = [];        
    ###########hardcoding our graph in for some testing - fix this###############
    primitives = mc.Bernoulli('primitives', pK, value=1)
    concepts.append(primitives);
    proceduralExecution = mc.Bernoulli('procedural_execution', pK, value=1)
    concepts.append(proceduralExecution);
    pOperations = stopGapDependencies('pOperations', [primitives])
    operations = mc.Bernoulli('operations', pOperations, value=1)
    concepts.append(operations);
    pVariables = stopGapDependencies('pVariables', [operations])
    variables = mc.Bernoulli('variables', pVariables, value=1)
    concepts.append(variables);
    pConditionals = stopGapDependencies('pConditionals', [variables, proceduralExecution])
    conditionals = mc.Bernoulli('conditionals', pConditionals, value=1)
    concepts.append(conditionals);
    pVariableMutation = stopGapDependencies('pVariableMutation',[variables])
    variableMutation = mc.Bernoulli('variable_mutation', pVariableMutation, value=1)
    concepts.append(variableMutation);
    pTypes = stopGapDependencies('pTypes', [variables])
    types = mc.Bernoulli('types', pTypes, value=1)
    concepts.append(types);
    pIteration = stopGapDependencies('pIteration', [variableMutation, conditionals])
    iteration = mc.Bernoulli('iteration', pIteration, value=1)
    concepts.append(iteration);
    pFunctions = stopGapDependencies('pFunctions', [types])
    functions = mc.Bernoulli('functions', pFunctions, value=1)
    concepts.append(functions);
    pArrays = stopGapDependencies('pArrays', [iteration])
    arrays = mc.Bernoulli('arrays', pArrays, value=1)
    concepts.append(arrays);
    pHofs = stopGapDependencies('pHofs', [functions])
    hofs = mc.Bernoulli('higher_order_functions', pHofs, value=1)
    concepts.append(hofs);
    pRecursion = stopGapDependencies('pRecursion', [functions])
    recursion = mc.Bernoulli('recursion', pRecursion, value=1)
    concepts.append(recursion);
    pSorting = stopGapDependencies('pSorting', [hofs, recursion, arrays])
    sorting = mc.Bernoulli('sorting', pSorting, value=1)
    concepts.append(sorting);
    pDataStructures = stopGapDependencies('pDataStructures', [arrays])
    dataStructures = mc.Bernoulli('data_structures', pDataStructures, value=1)
    concepts.append(dataStructures);
    pAComplexity = stopGapDependencies('pAComplexity', [sorting, dataStructures])
    aComplexity = mc.Bernoulli('algorithmic_complexity', pAComplexity, value=1)
    concepts.append(aComplexity);
    ########################################################################
    
    pQuestion1 = mc.Lambda('pQuestion1', lambda sorting=sorting: pl.where(sorting, 1-pS, pG))
    question1 = mc.Bernoulli('question1', pQuestion1, value=[1,1,1,1], observed=True)
    
    pQuestion2 = mc.Lambda('pQuestion2', lambda hofs=hofs: pl.where(hofs, 1-pS, pG))
    question2 = mc.Bernoulli('question2', pQuestion2, value=[1, 1, 1, 1, 1], observed=True)

    pQuestion3 = mc.Lambda('pQuestion3', lambda recursion=recursion: pl.where(recursion, 1-pS, pG))
    question3 = mc.Bernoulli('question3', pQuestion3, value=[1,1,1,1,1], observed=True)

    pQuestion4 = mc.Lambda('pQuestion4', lambda iteration=iteration: pl.where(iteration, 1-pS, pG))
    question4 = mc.Bernoulli('question4', pQuestion4, value=[1,1,1,1,1], observed=True)

    pQuestion5 = mc.Lambda('pQuestion5', lambda conditionals=conditionals: pl.where(conditionals, 1-pS, pG))
    question5 = mc.Bernoulli('question5', pQuestion5, value=1, observed=True)

    pQuestion6 = mc.Lambda('pQuestion6', lambda arrays=arrays: pl.where(arrays, 1-pS, pG))
    question6 = mc.Bernoulli('question6', pQuestion6, value=[1,1,1], observed=True)

    #pQuestion7 = mc.Lambda('pQuestion7', lambda aComplexity=aComplexity: pl.where(aComplexity, 1-pS, pG))
    #question7 = mc.Bernoulli('question7', pQuestion7, value=0, observed=True)
    
    
    
    ##################some simple tests##########
    
    model = mc.Model([primitives, operations, variables, proceduralExecution, types, variableMutation, conditionals, functions, iteration, hofs, recursion, arrays, sorting, dataStructures, aComplexity, question1, question2, question3, question4, question5, question6]);
    
    
    samples = mc.MCMC(model)
    unknownNodes = [];
    knownNodes = [];
    samples.sample(1000)

    for concept in concepts:
        if concept.trace().mean() < 0.4:
            unknownNodes.append(concept)
        elif concept.trace().mean() > 0.85:
            knownNodes.append(concept)
    return [unknownNodes, knownNodes, concepts]

#this needs tweaking till it works  Try constructing the pl.where structure instead maybe?
#def buildDependencies(dependencies, name, idealP, nonIdealP, compensatoryP):
 #   p = 0;
 #   if len(dependencies) == 1:
 #       dep = dependencies[0];
 #       #for reference, the semantics of this are if dep=1, p=idealP, else if dep=0, p=nonIdealP
 #       p = mc.Lambda('', lambda dep=dep: pl.where(dep, idealP, nonIdealP))
 #   else:
 #       previousDep = buildDependencies(dependencies[1:len(dependencies)], name, idealP, nonIdealP, compensatoryP)
 #       dep = dependencies[0];
 #       #likewise with above, just with two variables that vary between 1 and zero, with the 1 case first
 #       p = (mc.Lambda('', lambda previousDep=previousDep, dep=dep: pl.where(dep, pl.where(previousDep,
 #           idealP, compensatoryP), pl.where(previousDep, compensatoryP, nonIdealP))))
 #   return p


         

x = performInference('lol')