import unittest
import System
#from holaMundo import *


class Test(unittest.TestCase):
	obj=System.Systems()
	obj.insert("Universidad","uni",None)
	obj.insert("Ingenieria","ing","uni")
	obj.insert("Ciencias basicas","cb","ing")
	obj.insert("Ciencias basicas","cb","ing")
	obj.insert("Ciencias basicas","cb","uni")
	obj.insert("Ciencias basicas","ab","un")
	obj.insert("Salud","sal","uni")
	obj.insert("Sistemas","sis","ing")
	obj.insert("Electronica","elec","ing")
	obj.insert("Electronica","dir","elec")
	def test_tam(self):
		print "1"
		self.assertEqual(len(self.obj.elements),7)
	def test_getSubsystemsById(self):
		print "2"
		self.assertEqual(len(self.obj.getSubsystemsById("uni")),2)
	def test_getSubsystemsById_2(self):
		print "3"
		self.assertEqual(len(self.obj.getSubsystemsById("ing")),3)
	def test_getAllSubsystemsById(self):
		print "4"
		self.assertEqual(len(self.obj.getAllSubsystemsById("ing")),4)
	def test_getLevelById(self):
		print "5"
		self.assertEqual(self.obj.getLevelById("dir"),3)

if __name__ == '__main__':
	unittest.main()
