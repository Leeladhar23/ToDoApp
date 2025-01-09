from django.test import TestCase
from django.urls import reverse
from .models import TodoList, TodoItem
import json

class TodoAppTests(TestCase):

    def setUp(self):
        # Set up initial data for the tests
        self.list_data = {"name": "Test List"}
        self.todo_list = TodoList.objects.create(**self.list_data)
        self.item_data = {"title": "Test Item", "completed": False, "deadline": "2021-12-31"}
        self.todo_item = TodoItem.objects.create(todo_list=self.todo_list, **self.item_data)

    def test_create_todo_list(self):
        url = reverse('lists')
        data = {"name": "New List"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

    def test_create_todo_list_name_required(self):
        url = reverse('lists')
        response = self.client.post(url, data={})
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Name is required")

    def test_get_all_todo_lists(self):
        url = reverse('lists')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('lists', response.json())

    def test_get_todo_list_detail(self):
        url = reverse('list', kwargs={'pk': self.todo_list.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.todo_list.name)
    
    def test_get_todo_list_detail_not_found(self):
        url = reverse('list', kwargs={'pk': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "List not found")

    def test_delete_todo_list(self):
        url = reverse('list', kwargs={'pk': self.todo_list.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(TodoList.objects.filter(pk=self.todo_list.pk).exists())

    def test_add_item_to_list(self):
        url = reverse('list-items', kwargs={'pk': self.todo_list.pk})
        data = {"title": "New Item", "completed": False, "deadline": None}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

    def test_get_items_in_list(self):
        url = reverse('list-items', kwargs={'pk': self.todo_list.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.json())

    def test_update_item(self):
        url = reverse('update-item', kwargs={'pk': self.todo_list.pk, 'li': self.todo_item.pk})
        data = {"title": "Updated Title", "completed": True}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.todo_item.pk)
        self.todo_item.refresh_from_db()
        self.assertEqual(self.todo_item.title, "Updated Title")
        self.assertTrue(self.todo_item.completed)

    def test_delete_item(self):
        url = reverse('update-item', kwargs={'pk': self.todo_list.pk, 'li': self.todo_item.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(TodoItem.objects.filter(pk=self.todo_item.pk).exists())

    def test_delete_all_items(self):
        url = reverse('list-items', kwargs={'pk': self.todo_list.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TodoItem.objects.count(), 0)

    def test_todo_list_duplicate_name(self):
        url = reverse('lists')
        data = {"name": "Test List"}  # same name as already exists
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()['error'], "List already exists")
        
    def test_mutliple_create_todo_list(self):
        url = reverse('lists')
        data = {"name": "New List"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        
        data = {"name": "Another List"}
        response = self.client.post(url, data=data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['lists']), 3)
        
    def test_complex_workflow(self):
        # Create a new list
        url = reverse('lists')
        data = {"name": "New List"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        
        list_id = response.json()['id']
        # Add an item to the list
        url = reverse('list-items', kwargs={'pk': list_id})
        data = {"title": "New Item", "completed": False, "deadline": None}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        
        item_id = response.json()['id']
        
        # Update the item
        url = reverse('update-item', kwargs={'pk': list_id, 'li': item_id})
        data = {"title": "Updated Item", "completed": True}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(item_id, response.json()['id'])
        
        # Delete the item
        url = reverse('update-item', kwargs={'pk': list_id, 'li': item_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        
        # Delete all items in the list
        url = reverse('list-items', kwargs={'pk': list_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(TodoItem.objects.count(), 1)
        
        # Delete the list
        url = reverse('list', kwargs={'pk': list_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(TodoList.objects.filter(pk=list_id).exists())
