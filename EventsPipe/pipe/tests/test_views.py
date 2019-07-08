# from django.test import TestCase
# from django.urls import reverse
#
# from pipe.models import Event, Ticket
#
# class PipeViewGETTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create an Event and a Ticket
#         Event.objects.create(
#             description = "Test Description",
#             name = "Test Name",
#             event_id = "123",
#             start_date = timezone.now(),
#         )
#
#         event = Event.objects.get(name="Test Name")
#         Ticket.objects.create(
#             ticket_cost = 1.0,
#             event_id = event,
#         )
#
#
#     def test_GET_name_view(self):
#         response = self.client.get('/pipe/authors/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'catalog/author_list.html')
#
#     def test_pagination_is_ten(self):
#         response = self.client.get(reverse('authors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertTrue(len(response.context['author_list']) == 10)
#
#     def test_lists_all_authors(self):
#         # Get second page and confirm it has (exactly) remaining 3 items
#         response = self.client.get(reverse('authors')+'?page=2')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertTrue(len(response.context['author_list']) == 3)
