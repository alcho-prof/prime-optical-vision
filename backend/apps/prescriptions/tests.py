from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Prescription

User = get_user_model()

class PrescriptionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rxuser', email='rx@test.com', password='password')
        self.client.force_login(self.user)

    def test_create_prescription(self):
        url = reverse('prescriptions:add')
        data = {
            'name': 'My Glasses',
            'doctor_name': 'Dr. Vision',
            'exam_date': '2025-01-01',
            'od_sphere': '-2.00',
            'od_cylinder': '-0.50',
            'od_axis': 90,
            'od_add': '2.00',
            'os_sphere': '-2.50',
            'os_cylinder': '-0.75',
            'os_axis': 180,
            'os_add': '2.00',
            'pd_single': '62.0'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirects on success
        
        self.assertEqual(Prescription.objects.count(), 1)
        rx = Prescription.objects.first()
        self.assertEqual(rx.name, 'My Glasses')
        self.assertEqual(rx.user, self.user)

    def test_list_prescriptions(self):
        Prescription.objects.create(
            user=self.user, name="Existing Rx", od_sphere='-1', os_sphere='-1'
        )
        url = reverse('prescriptions:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Rx")
