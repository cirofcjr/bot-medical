from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class APITest(TestCase):

	def test_create_especialidade_and_delete(self):
		data = {"nome":"Ortopedista"}
		response = self.client.post(reverse('list-especialidades'), data=data)
		id = response.json()['id']
		delete = self.client.delete(reverse('especialidade-detail', kwargs={'pk':id}))
		self.assertEqual(response.status_code, 201, msg="Criar especialidade")
		self.assertEqual(delete.status_code, 204,msg="Deletar a especialidade criada")
		return response.json() 

	# def test_delete_ortopedista(self):
		# print(reverse('especialidade-detail', kwargs={'pk':'1'}))
		# print(self.client.get(reverse('especialidade-detail', kwargs={'pk':'1'})))

