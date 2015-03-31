import ast, re, sys
from xml.dom import minidom

try:
    from xml.etree import cElementTree as etree
except:
    try:
        from lxml import etree
    except:
        from xml.etree import ElementTree as etree

def prettify(xml_string):
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="  ") 

class ast2xml(ast.NodeVisitor):
    def __init__(self):
        super(ast.NodeVisitor, self).__init__()
        self.root = etree.Element('ast')
        self.celement = self.root
        self.lname = 'module'
    def convert(self, tree):
        self.visit(tree)
        return etree.tostring(self.root)
    def generic_visit(self, node):
        ocelement = self.celement
        self.celement = etree.SubElement(self.celement, self.lname)
        self.celement.attrib.update({'_name': type(node).__name__})
        olname = self.lname
        self.lname = type(node).__name__
        for item in node.__dict__:
            self.lname = item
            if isinstance(getattr(node, item), ast.AST):
                self.generic_visit(getattr(node, item))
            elif isinstance(getattr(node, item), list):
                ocel2 = self.celement
                olname2 = self.lname
                self.celement = etree.SubElement(self.celement, self.lname)
                self.celement.attrib.update({'_name': '_list'})
                self.lname = '_list_element'
                [self.generic_visit(childnode) for childnode in getattr(node, item) if isinstance(childnode, (ast.AST, list))]
                self.celement = ocel2
                self.lname = olname2
            else:
                self.celement.attrib.update({item: str(getattr(node, item))})
        self.celement = ocelement
        self.lname = olname

def main(fpath):
	with open(fpath,'r') as f:
		  tree = ast.parse(f.read())
	f.close()
	res = ast2xml().convert(tree)
	print prettify(res)
	with open("generar.txt",'a') as f:
		  f.write(prettify(res))
	f.close()



"""
    with open(fpath, 'r') as f:
        tree = ast.parse(f.read())
				f.close()

        res = ast2xml().convert(tree)
        print prettify(res)
"""

if __name__ == '__main__':
    main(sys.argv[1])



"""
import ast


class AnalysisNodeVisitor(ast.NodeVisitor):
 
    def __init__(self,rootNode = None):
        self._modules = []
        self._classes = []
        self._functions = []
        self._variables = []
        self._imports = []
        self._rootNode = rootNode
        self._parentNode = rootNode
        self._level = 0
 
    @property
    def rootNode(self):
        return self._rootNode
 
    @property
    def imports(self):
        return self._imports
 
    @property
    def functions(self):
        return self._functions
 
    @property
    def variables(self):
        return self._variables
 
    @property
    def classes(self):
        return self._classes
 
    def visit_Import(self,node):
        for name in node.names:
            importNode = Node(attributes = {'type':'import','names':map(lambda x:x.name,node.names)},parent = self._parentNode)
            self._imports.append(importNode)
        ast.NodeVisitor.generic_visit(self, node)
 
    def visit_ImportFrom(self,node):
        for name in node.names:
            importNode = Node(attributes = {'line_number':node.lineno,'type':'from_import','module':node.module,'names':map(lambda x:x.name,node.names)},parent = self._parentNode)
            self._imports.append(importNode)
        ast.NodeVisitor.generic_visit(self, node)
 
    def visit_Assign(self,node):
        for target in node.targets:
            self._add_target_to_variables(target)
        ast.NodeVisitor.generic_visit(self, node)
 
    def visit_AssignAug(self,node):
        self._add_target_to_variables(node.target)
        ast.NodeVisitor.generic_visit(self, node)
 
    def _add_target_to_variables(self,target):
        if hasattr(target,'value'):
            self._add_target_to_variables(target.value)
        elif hasattr(target,'id'):
            if not target.id in self._variables and not target.id == "self":
                variableNode = Node(attributes = {'type':'variable','name':target.id},parent = self._parentNode)
                self._variables.append(variableNode)
 
    def visit_FunctionDef(self,node):
        body = node.body
        functionNode = Node(attributes = {'type':'function','name':node.name,'start_line':body[0].lineno,'end_line':_get_last_line_number(body),'docstring':ast.get_docstring(node)},parent = self._parentNode)
        self._functions.append(functionNode)
        oldParent = self._parentNode
        self._parentNode = functionNode
        ast.NodeVisitor.generic_visit(self, node)
        self._parentNode = oldParent
 
    def visit_ClassDef(self,node):
        body = node.body
        classNode = Node(attributes = {'type':'class','name':node.name,'start_line':body[0].lineno,'end_line':_get_last_line_number(body),'docstring':ast.get_docstring(node)},parent = self._parentNode)
        self._classes.append(classNode)
        oldParent = self._parentNode
        self._parentNode = classNode
        ast.NodeVisitor.generic_visit(self, node)
        self._parentNode = oldParent




def _get_last_line_number(nodes):
    children = None
    if hasattr(nodes[-1],'orelse'):
        children = nodes[-1].orelse
    elif hasattr(nodes[-1],'finalbody'):
        children = nodes[-1].finalbody
    elif hasattr(nodes[-1],'body'):
        children = nodes[-1].body
    if children:
        return max(nodes[-1].lineno,_get_last_line_number(children))
    else:
        return nodes[-1].lineno


class Node(object):
 
    def __init__(self,attributes = {},parent = None):
        self.__dict__.update({'_children':[],'_parent':None,'_attributes':attributes})
        self.parent = parent
 
    def __repr__(self):
        return self.__class__.__name__+"(attributes = "+str(self.attributes)+")"
 
    @property
    def attributes(self):
        return self._attributes
 
    @attributes.setter
    def attributes(self,attributes):
        self._attributes = attributes
 
    @property
    def parent(self):
        return self._parent
 
    @parent.setter
    def parent(self,parent):
        if self._parent != None:
            self._parent.removeChild(self)
        self._parent = parent
        if self._parent != None:
            self._parent.addChild(self)
 
    @property
    def children(self):
        return self._children
 
    def removeChild(self,child):
        if child in self.children():
            del self._children[self._children.indexof(child)]
 
    def addChild(self,child):
        if not child in self._children:
            self._children.append(child)


with open("System.py",'r') as f:
    content = f.read()
f.close()

node = ast.parse(content)
analysis=AnalysisNodeVisitor(node)
#analysis.visit_Import(node)
analysis.visit_ClassDef(node)
for a in clases:
	print a
"""
