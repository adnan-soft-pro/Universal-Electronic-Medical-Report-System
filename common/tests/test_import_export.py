from django.test import Client
from django.utils import timezone
from model_mommy import mommy

from accounts.models import User
from instructions.models import Instruction
from organisations.models import OrganisationGeneralPractice
from payment.tests.test_functions import CalculateInstructionFeeBaseTest
from payment.functions import calculate_instruction_fee
from instructions import model_choices

import csv
import io
import zipfile
import os


class ImportExportTest(CalculateInstructionFeeBaseTest):

    def setUp(self):
        super().setUp()
        self.medidata_user = User.objects.create_superuser(email='medidta@test.com', password='test1234')
        self.client = Client()
        self.client.login(email=self.medidata_user.email, password='test1234')
        self.amra_instruction = mommy.make(
            Instruction,
            id=3,
            type=model_choices.AMRA_TYPE,
            gp_practice=self.gp_practice,
            client_user=self.client_user,
            status=model_choices.INSTRUCTION_STATUS_COMPLETE,
            created=timezone.now(),
            completed_signed_off_timestamp=timezone.now()
        )
        self.sars_instruction = mommy.make(
            Instruction,
            id=4,
            type=model_choices.SARS_TYPE,
            gp_practice=self.gp_practice,
            client_user=self.client_user,
            status=model_choices.INSTRUCTION_STATUS_COMPLETE,
            created=timezone.now(),
            completed_signed_off_timestamp=timezone.now()
        )
        self.instruction_status_header = 'ID, MediRef, Surgery, Status'
        self.instruction_content = [
            '3, 10000003, Test Name GP Organisation, Completed',
            '4, 10000004, Test Name GP Organisation, Completed'
        ]

        for instruction in Instruction.objects.all():
            calculate_instruction_fee(instruction)

    def test_export_payment_as_csv(self):
        response = self.client.post('/admin/instructions/instruction/', {'action': 'export_payment_as_csv'})
        self.assertEqual(response.status_code, 200)

        # load and extract members in zip file then keep temporary csv files to '/common/tests/test_file_data' directory
        z = zipfile.ZipFile(io.BytesIO(response.content))
        test_data_directory_path = os.getcwd()+'/common/tests/test_file_data'
        z.extractall(test_data_directory_path)

        # test contents of instruction status csv file
        instruction_status_file_name = z.filelist[1].filename
        instruction_reader = csv.reader(open(test_data_directory_path + '/' + instruction_status_file_name))

        for i, row in enumerate(instruction_reader):
            if i == 0:
                self.assertEqual(', '.join(row), self.instruction_status_header)
            else:
                self.assertEqual(', '.join(row), self.instruction_content[i-1])

        # test contents of payment report csv file
        payment_filename = z.filelist[0].filename
        payment_reader = csv.reader(open(test_data_directory_path + '/' + payment_filename))
        payment_header = 'Sort Code, Account number, GP Surgery, Amount, VAT, Reference'
        payment_content = [
            '12-34-56, 12345678, Test Name GP Organisation, 70.00, , '
        ]
        for i, row in enumerate(payment_reader):
            if i == 0:
                self.assertEqual(', '.join(row), payment_header)
            else:
                self.assertEqual(', '.join(row), payment_content[i-1])

        os.remove(test_data_directory_path + '/' + instruction_status_file_name)
        os.remove(test_data_directory_path + '/' + payment_filename)

    def test_export_client_payment_as_csv(self):
        response = self.client.post('/admin/instructions/instruction/', {'action': 'export_client_payment_as_csv'})
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        client_payment_reader = csv.reader(io.StringIO(content))
        body = list(client_payment_reader)
        client_payment_header = 'Client Id, Client Organisation, Amount, VAT, Reference'
        client_payment_content = [
            '1, Test Trading Name Client Organisation, 110.00, 8.00, '
        ]
        for i, row in enumerate(body):
            if i == 0:
                self.assertEqual(', '.join(row), client_payment_header)
            else:
                self.assertEqual(', '.join(row), client_payment_content[i-1])

    def test_export_status_report_as_csv(self):
        response = self.client.post(
            '/admin/instructions/instruction/',
            {
                'action': 'export_status_report_as_csv',
                '_selected_action': ['3', '4']
            }
        )
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        instruction_reader = csv.reader(io.StringIO(content))
        body = list(instruction_reader)
        for i, row in enumerate(body):
            if i == 0:
                self.assertEqual(', '.join(row), self.instruction_status_header)
            else:
                self.assertEqual(', '.join(row), self.instruction_content[i-1])
