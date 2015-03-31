import ast,sys

class Py2Neko(ast.NodeVisitor):
    def __init__(self):
        super(ast.NodeVisitor, self).__init__()
        self.rep=0
		
    def generic_visit(self, node):
				amg=self.rep
				self.rep+=1
				print self.rep,self.rep*" ",type(node).__name__
				for item in node.__dict__:
					if isinstance(getattr(node, item), ast.AST):
						self.generic_visit(getattr(node, item))
					elif isinstance(getattr(node, item), list):
						print self.rep,self.rep*" ",'_list ',item
						[self.generic_visit(childnode) for childnode in getattr(node, item) if isinstance(childnode, (ast.AST, list))]
					else:
						print self.rep,self.rep*" ",item,"-",str(getattr(node, item))
				self.rep=amg
        #ast.NodeVisitor.generic_visit(self, node)

"""
    def visit_Name(self, node):
        print 'Name :', node.id

    def visit_Num(self, node):
        print 'Num :', node.__dict__['n']

    def visit_Str(self, node):
        print "Str :", node.s

    def visit_Print(self, node):
        print "Print :"
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print "Assign :"
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print "Expr :"
        ast.NodeVisitor.generic_visit(self, node)
"""

def main(fpath):
		with open(fpath,'r') as f:
				node = ast.parse(f.read())
				print ast.dump(node)
		f.close()
		v = Py2Neko()
		v.visit(node)




if __name__ == '__main__':
    main(sys.argv[1])
