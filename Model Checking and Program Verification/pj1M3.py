'''
@author: wge  

Notes: 
M2  the specification automaton S and the system model A 
    L(M) = L(A) intersect L(S)    output a str in LM and M 
'''
import sys
import copy

#inputfilename = 'exmp01_M22.txt'
inputfilename = 'exmp01_M2.txt'

class FA(object):
#     alphabet = []
#     states = []
#     statesobject = []
#     initstates = []
#     finalstates =  []
#     transitionfunction = [] # [[1 a 6], [1 b 2], ...[ ] ]
#     lasttransition = ''
#     aptset = set()
#     aptlist = []
    
    def __init__(self):
        #pass
        self.alphabet = []
        self.states = []
        self.statesobject = []
        self.initstates = []
        self.finalstates = []
        self.transitionfunction = [] # [[1 a 6], [1 b 2], ...[ ] ]
        self.lasttransition = ''
        self.aptset = set()
        self.aptlist = []
    
    def genString(self):
        #generate accepted strings from NFA transition functions
        try:
            for eachinitstate in self.initstates:
                self.aptlist.extend( self.resultinfinalStateDFA(eachinitstate) )
                #self.aptlist = self.resultinfinalStateDFA(eachinitstate)
            self.aptset = set(self.aptlist)
        
            if not self.aptlist or self.aptlist[0] == ' ':
                print('There is no accepted string for L(m\'), ' )
                print('The language is empty and system satisfy the specification' )
            else:
                print('There are accepted strings for L(m\'), ' )
                print('The language is not empty and system does not satisfy the specification' )
        except RuntimeError as re:
            print('There is no accepted string for L(m\'), ' )
            print('The language is empty and system satisfy the specification' )
                    
        
    def resultinfinalState(self,eis):
        mylist = []
        fsFlag = False
        
        for tf in self.transitionfunction:
            if eis == tf[0]:
                rs = tf[4]
                mylist.append(tf[2])
                if rs in self.finalstates:
                    fsFlag = True
                    #print('string that M\' accepts')
                    print(''.join(mylist))
                    return mylist
                else:
                    if tf == self.lasttransition:
                        fsFlag = False  
                    else:
                        self.lasttransition = tf
                        self.resultinfinalState(rs)
                        return mylist
        if not fsFlag:
            return []
     
    def resultinfinalStateDFA(self,eis):
        mylist = []
        fsFlag = False
        
        for tf in self.transitionfunction: # TFs [ [[1,2],a,[2,3]], [].... ,[] ]    tf [[1,2],a,[2,3]]
            if eis == tf[0]:
                rs = tf[2]
                mylist.append(tf[1])
                if rs in self.finalstates:
                    fsFlag = True
                    #print('string that M\' accepts')
                    #print(''.join(mylist))
                    return mylist
                else:
                    if tf == self.lasttransition:
                        fsFlag = False  
                    else:
                        self.lasttransition = tf
                        self.resultinfinalStateDFA(rs)
                        return mylist
        if not fsFlag:
            return [] 
        
    def genStates(self):
        for tf in self.transitionfunction:
            self.states.append(tf[0])
            self.states = removeduplistoflist(self.states)

def NFAComplement(NFA1):
    NFA2 = NFA1
    NFA2.finalstates = list(set(NFA2.states) - set(NFA2.finalstates))  #set difference what is in A but not in B (elements just in B not displayed)
    return NFA2;

def DFAComplementref(DFA1):  #this one replaces M with M' for the DFA passed in
    newfinalstates = []
    for DFA1state in DFA1.states:   # DFA states are list of list, mutable so we can not use set
        if DFA1state in DFA1.finalstates:
            pass
        else:
            newfinalstates.append(DFA1state)  #add the state that were not fs
    DFA1.finalstates = newfinalstates
    return DFA1;

def DFAComplement(DFA1):
    DFA2 = copy.deepcopy(DFA1)
    newfinalstates = []
    for DFA1state in DFA1.states:   # DFA states are list of list, mutable so we can not use set
        if DFA1state in DFA1.finalstates:
            pass
        else:
            newfinalstates.append(DFA1state)  #add the state that were not fs
    DFA2.finalstates = newfinalstates
    return DFA2;

def txt2NFA(NFA1, NFA2):
    #try reading NFA as txt  
    print('now reading NFA')
    #NFA1 = FA()
    SFlag = False  #Specification automaton 
    AFlag = False  #System automaton
    alphabetFlag = False
    initstateFlag = False
    finalstateFlag = False
    tfFlag = False
    
    try: 
        reader = open(inputfilename, 'r')
        for row in reader:
            if row:
                #print row
                if '% Specification automaton' in row:
                    SFlag = True 
                    AFlag = False 

                elif '% System automaton' in row:
                    SFlag = False 
                    AFlag = True 
                
                elif alphabetFlag == True:
                    NFA1.alphabet.append(row[0])
                    NFA2.alphabet.append(row[0])

                elif  SFlag == True:
                    if initstateFlag == True:
                        NFA1.initstates.append(row[0])
                        
                    elif finalstateFlag == True:
                        NFA1.finalstates.append(row[0])
                        NFA1.finalstates = removeduplistoflist(NFA1.finalstates)
                        
                    elif tfFlag == True:
                        NFA1.transitionfunction.append(row[0:5])

                elif AFlag == True:
                    if initstateFlag == True:
                        NFA1.initstates.append(row[0])
                        
                    elif finalstateFlag == True:
                        NFA1.finalstates.append(row[0])
                        NFA1.finalstates = removeduplistoflist(NFA1.finalstates)
                        
                    elif tfFlag == True:
                        NFA1.transitionfunction.append(row[0:5])

                elif '% Input alphabet' in row:
                    alphabetFlag = True
                    initstateFlag = False
                    finalstateFlag = False
                    tfFlag = False
                
                elif '% Transition function' in row:
                    alphabetFlag = False
                    initstateFlag = False
                    finalstateFlag = False 
                    tfFlag = True
                    
                elif '% Initial state' in row:
                    alphabetFlag = False
                    initstateFlag = True
                    finalstateFlag = False 
                    tfFlag = False
                
                elif '% Final states' in row:
                    alphabetFlag = False
                    initstateFlag = False
                    finalstateFlag = True 
                    tfFlag = False
                elif '% Specification automaton' in row:
                    alphabetFlag = False
                    initstateFlag = False
                    finalstateFlag = False 
                    tfFlag = False 
                elif '% System automaton' in row:
                    alphabetFlag = False
                    initstateFlag = False
                    finalstateFlag = False 
                    tfFlag = False 
            
                #end of if row       
                
                         
                
        reader.close()
        print('NFA1.alphabet')
        print(NFA1.alphabet)
        print('NFA1.initstates')
        print(NFA1.initstates)
        print('NFA1.finalstates')
        print(NFA1.finalstates)
        print('NFA1.transitionfunction')
        print(NFA1.transitionfunction)

        print('NFA2.alphabet')
        print(NFA2.alphabet)
        print('NFA2.initstates')
        print(NFA2.initstates)
        print('NFA2.finalstates')
        print(NFA2.finalstates)
        print('NFA2.transitionfunction')
        print(NFA2.transitionfunction)
        
    except:
        print("Unexpected error while parsing FA:", sys.exc_info()[0])
        raise   

def reformattfDFA(NFA1):
    newtf = []
    for tf in NFA1.transitionfunction:
        newtfelement = []
        newtfelement.append(tf[0])
        newtfelement.append(tf[2])
        newtfelement.append(tf[4])
        newtf.append(newtfelement)
    NFA1.transitionfunction = newtf
    

def NFA2DFA(NFA1):
    DFA2 = NFA1
    # if NFA covert to DFA, else no change 
    sadict = {}    #start state key, transition bit value 
    isNFA = False
    for tf in NFA1.transitionfunction:
            if tf[0] in sadict.keys():
                if sadict[tf[0]] == tf[2]:   #if same start state and alphabet, it is a NFA
                    isNFA = True
                else:   #if same start state but different alphabet, we keep on looking
                    pass
            else: 
                sadict[tf[0]] = tf[2]
    if isNFA:
        print('This is a NFA')
        DFA2.states = getstatesDFA(NFA1)
        DFA2.initstates = getinitstDFA(NFA1,DFA2)
        DFA2.finalstates = getfinalstDFA(NFA1,DFA2)
        DFA2.transitionfunction = gettfDFA(NFA1,DFA2)
        print('DFA2.states')
        print(DFA2.states)
        print('DFA2.initstates')
        print(DFA2.initstates)
        print('DFA2.finalstates')
        print(DFA2.finalstates)
        print('DFA2.transitionfunction')
        print(DFA2.transitionfunction)
        return DFA2;
    else: #if not NFA, we return as DFA with no change
        print('This is a DFA')
        reformattfDFA(DFA2)
        return DFA2;

def getstatesDFA(NFA1):
    Qlist = []  #DFA states are the power set of NFA states 
    qlist = NFA1.states
    Qlist = powerset(qlist)
    return Qlist

def removeduplistoflist(duplist):
    newlist = []
    for i in duplist:
        if i not in newlist:
            newlist.append(i) 
    return newlist
   
def powerset(mylist):
    powerset = []
    x = len(mylist)
    for state in range(1 << x):
        #print [mylist[j] for j in range(x) if (state & (1 << j))]   
        powerset.append([mylist[j] for j in range(x) if (state & (1 << j))])
    return powerset

def powerset1(s):
    x = len(s)
    mylist = []
    for i in range(1 << x):
        mylist.append( [s[j] for j in range(x) if (i & (1 << j))]        )
    print(mylist)
        
def getinitstDFA(NFA1,DFA2):
    initstDFA = []
    for statelist in DFA2.states:
        for element in statelist:
            if element in NFA1.initstates:
                initstDFA.append(statelist)
    initstDFA = removeduplistoflist(initstDFA)  
    return initstDFA      

def getfinalstDFA(NFA1,DFA2):
    finalstDFA = []
    for statelist in DFA2.states:
        for element in statelist:
            if element in NFA1.finalstates:
                finalstDFA.append(statelist)
    finalstDFA = removeduplistoflist(finalstDFA)         
    return finalstDFA 
    
def gettfDFA(NFA1, DFA2):
    for q in DFA2.states: #for each state which is list of states in DFA   q is ss
        for ab in NFA1.alphabet: # for each transition a or b 
            ss = q
            #trans = ab 
            rs = []
            for eachNFAstate in q: 
                for eachrsfromeachNFAstate in getnxtstsNFA(NFA1, eachNFAstate, ab):
                    rs.append(eachrsfromeachNFAstate)
                    rs = removeduplistoflist(rs)  
            delement = [ss,ab,rs]  #each element of the DFA transition function       
            DFA2.transitionfunction.append(delement)
    return removeduplistoflist(DFA2.transitionfunction) 

def getnxtstsNFA(NFA1, ss, ab): # get the list of next states from start state aa and string ab
    rslist = []
    for tf in NFA1.transitionfunction: #[01234] [1 a b]
        if (tf[0] == ss) and (tf[2] == ab):
            rslist.append(tf[4])
        else: 
            pass
    return rslist

def print2txt(DFA2):
    fstr = open('1211_Milestone2_str.txt','w')
    fdp = open('1211_Milestone2_M.txt','w')
    setwrite(fstr,DFA2.aptset)
    if (DFA2.aptlist):
        print(DFA2.aptlist[0])
    #print(DFA2.aptset)
    #print(DFA2.aptlist)
    
    fdp.write('% Input alphabet \n')
    listwrite(fdp,DFA2.alphabet)
    #fdp.write()
    fdp.write('% Specification automaton \n')
    fdp.write('% Transition function \n')
    llistwrite(fdp,DFA2.transitionfunction)
    fdp.write('% Initial state \n')
    listwrite(fdp,DFA2.initstates)
    fdp.write('% Final states \n')
    listwrite(fdp,DFA2.finalstates)
    
    fstr.close()
    fdp.close()

def setwrite(fileobj, pset):
    for ele in pset: 
        fileobj.write(ele)
        fileobj.write('\n')
        
def listwrite(fileobj, plist):
    for ele in plist: 
        fileobj.write(str(ele) )
        fileobj.write('\n')

def llistwrite(fileobj, pplist):
    for plist in pplist: 
        for ele in plist:
            fileobj.write(str(ele) ) 
            fileobj.write(' ')
        fileobj.write('\n')

def intersectionCPC(DFA1, DFA2):
    LM = FA()
    
    return LM


def main():
    #First we find comp LS
    NFA1Spec = FA()
    NFA2Sys = FA()
    #powerset1([4,5,6])
    #print(powerset([1,2,3]))
    print('Hello World')
    txt2NFA(NFA1Spec, NFA2Sys)
    NFA1Spec.genStates()
    print('Convert to DFA')
    DFA1 = NFA2DFA(NFA1Spec)
    print('Finished')
    DFA1C = DFAComplement(DFA1)
    print('list of final states for M')
    print(DFA1C.finalstates)
    #print('string that M accepts')
    #DFA1.genString()
    print('list of final states for complement M\'')
    print(DFA1C.finalstates)
    #print('string that M\' accepts')
    DFA1C.genString()

    #then we find Lsys  and intersect Lsys with Lspec comp 
    DFA2 = NFA2DFA(NFA2Sys)
    LM = FA()
    LM = intersectionCPC(DFA2, DFA1C)
    LM.genString()
    #output string and LM 
    
    print2txt(LM)
    
    


if __name__ == '__main__':
    main()