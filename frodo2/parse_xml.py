"""[PARSE XML FRODO INPUT]

[#code to parse the celar instances into frodo input]

Variables:
    celarForFrodoObj {[type]} -- [description]
    var {[type]} -- [description]
    crt {[type]} -- [description]
    cnt {[type]} -- [description]
    dom {[type]} -- [description]
    dummy {[type]} -- [description]
    xml {[type]} -- [description]
    output_file {[type]} -- [description]
    output_file.write(xml) {[type]} -- [description]
    output_file.close() {[type]} -- [description]
"""
import numpy as np
from functools import reduce
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

class CelarForFrodo:
    def __init__(self,path_of_folder):
        self.path_of_folder=path_of_folder

    def get_constraints(self):
        constrant = open('./Data/' + self.path_of_folder + '/CTR.txt', 'r')
        lines = constrant.readlines()
        crt = []
        for line in lines:
            new_line = " ".join(line.split())
            info = new_line.split(' ')
            crt.append(info)
        constrant.close()
        return crt

    def get_domain(self):
        domain = open('./Data/' + self.path_of_folder + '/DOM.txt', 'r')
        lines = domain.readlines()
        dom = []
        for line in lines:
            new_line = " ".join(line.split())
            info = new_line.split(' ')
            dom.append(info)
        domain.close()
        return dom

    def get_variables(self):
        variables = open('./Data/' + self.path_of_folder + '/VAR.txt', 'r')
        lines = variables.readlines()
        var = []
        for line in lines:
            new_line = " ".join(line.split())
            info = new_line.split(' ')
            var.append(info)
        variables.close()
        return var

    # cosite cinstraints
    def getting_filtered_constarints(self,crt):
        cnt = []
        for i in range(len(crt)):
            if (crt[i][2] == "C"):
                cnt.append(crt[i])
            elif (crt[i][2] == "D"):
                cnt.append(crt[i])
            else:
                pass
        return cnt

    def getting_agents(self,crt):
        c = []
        for i in range(len(crt)):
            if (crt[i][2] == "C"):
                c.append(crt[i])
            else:
                pass

        sites = []
        for i in range(len(c)):
            if (c[i][2] == "C"):
                if (len(sites) == 0):
                    same_site = []
                    same_site.append(c[i][0])
                    same_site.append(c[i][1])
                    sites.append(same_site)
                else:
                    find = False
                    for j in range(len(sites)):
                        if (c[i][0] in sites[j]):
                            sites[j].append(c[i][1])
                            find = True
                        elif (c[i][1] in sites[j]):
                            sites[j].append(c[i][0])
                            find = True
                    if (find == False):
                        same_site = []
                        same_site.append(c[i][0])
                        same_site.append(c[i][1])
                        sites.append(same_site)
        dummy = sites

        for i in range(len(var)):
            find = False
            for j in range(len(dummy)):
                if (var[i][0] in dummy[j]):
                    find = True
            if (find == False):
                same_site = []
                same_site.append(var[i][0])
                dummy.append(same_site)
        return dummy

    def generating_xml(self,var, cnt, dummy, dom):
        root = Element('instance')

        presentation = SubElement(root, 'presentation')
        presentation.set('name', 'sampleProblem')
        presentation.set('maxConstraintArity', '3')
        presentation.set('maximize', 'false')
        presentation.set('format', 'XCSP 2.1_FRODO')

        # Agent Tags
        agents = SubElement(root, 'agents')
        agents.set('nbAgents', str(len(dummy)))

        for i in range(len(dummy)):
            agent = SubElement(agents, 'agent')
            agent.set('name', str('A' + str(i)))
        # Domain Tags
        domains = SubElement(root, 'domains')
        domains.set('nbDomains', str(len(dom)))

        for i in range(len(dom)):
            domain = SubElement(domains, 'domain')
            domain.set('name', str('D' + dom[i][0]))
            domain.set('nbValues', str(dom[i][1]))
            string = ' '
            for j in range(int(dom[i][1])):
                if j == 0:
                    string += (dom[i][j + 2])
                else:
                    string += ' ' + (dom[i][j + 2])
            domain.text = string

        # Variable Tags
        variables = SubElement(root, 'variables')
        variables.set('nbVariables', str(len(var)))

        for i in range(len(var)):
            variable = SubElement(variables, 'variable')
            variable.set('name', str('X' + var[i][0]))
            variable.set('domain', str('D' + var[i][1]))
            for j in range(len(dummy)):
                if (var[i][0] in dummy[j]):
                    variable.set('agent', str('A' + str(j)))
                else:
                    pass

        # Predicate Tags
        predicates = SubElement(root, 'predicates')
        predicates.set('nbPredicates', str(5))

        # Predicate D
        predicate = SubElement(predicates, 'predicate')
        predicate.set('name', 'D')

        parameters = SubElement(predicate, 'parameters')
        value = 'int X int Y int Z'
        parameters.text = value

        expression = SubElement(predicate, 'expression')
        functional = SubElement(expression, 'functional')
        value = 'eq(sub(X,Y),Z)'
        functional.text = value

        # Predicate F
        predicate = SubElement(predicates, 'predicate')
        predicate.set('name', 'F')

        parameters = SubElement(predicate, 'parameters')
        value = 'int X int Y int Z'
        parameters.text = value

        expression = SubElement(predicate, 'expression')
        functional = SubElement(expression, 'functional')
        value = 'gt(sub(X,Y),Z)'
        functional.text = value

        # Predicate P
        predicate = SubElement(predicates, 'predicate')
        predicate.set('name', 'P')

        parameters = SubElement(predicate, 'parameters')
        value = 'int X int Y int Z'
        parameters.text = value

        expression = SubElement(predicate, 'expression')
        functional = SubElement(expression, 'functional')
        value = 'gt(sub(X,Y),Z)'
        functional.text = value

        # Predicate C
        predicate = SubElement(predicates, 'predicate')
        predicate.set('name', 'C')

        parameters = SubElement(predicate, 'parameters')
        value = 'int X int Y int Z'
        parameters.text = value

        expression = SubElement(predicate, 'expression')
        functional = SubElement(expression, 'functional')
        value = 'gt(sub(X,Y),Z)'
        functional.text = value

        # Predicate L
        predicate = SubElement(predicates, 'predicate')
        predicate.set('name', 'L')

        parameters = SubElement(predicate, 'parameters')
        value = 'int X int Y int Z'
        parameters.text = value

        expression = SubElement(predicate, 'expression')
        functional = SubElement(expression, 'functional')
        value = 'gt(sub(X,Y),Z)'
        functional.text = value

        # Constraints
        constraints = SubElement(root, 'constraints')
        constraints.set('nbConstraints', str(len(cnt)))

        for i in range(len(cnt)):
            constraint = SubElement(constraints, 'constraint')
            constraint.set('name', 'Crt' + str(i))
            constraint.set('arity', '3')
            constraint.set('reference', cnt[i][2])
            constraint.set('scope', 'X' + cnt[i][0] + ' ' + 'X' + cnt[i][1])
            value = 'X' + cnt[i][0] + ' ' + 'X' + cnt[i][1] + '  ' + cnt[i][4]
            parameters = SubElement(constraint, 'parameters')
            parameters.text = value

        return (self.prettify(root))

    # copied from internet
    def prettify(self,elem):
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")








#here we create an instance from CelarForFrodo

celarForFrodoObj=CelarForFrodo(path_of_folder='CELAR/scen01')
var=celarForFrodoObj.get_variables()
crt=celarForFrodoObj.get_constraints()
cnt=celarForFrodoObj.getting_filtered_constarints(crt=crt)
dom=celarForFrodoObj.get_domain()
dummy=celarForFrodoObj.getting_agents(crt=crt)
xml=celarForFrodoObj.generating_xml(var=var,cnt=cnt,dom=dom,dummy=dummy)



output_file = open('scene01.xml', 'w' )
output_file.write(xml)
output_file.close()
