"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class PagosTest(TestCase):
	def testBasic(self):
		p = Pago()
		p.importe = 100
		p.descripcion = "Pago de prueba de test.py"
		p.save()
		print "Pago creado"
		print p.get_absolute_url()
		p.set_as_paid()
		p.delete()
		self.assertEqual(p.set_as_paid(),True)
		p.delete()
