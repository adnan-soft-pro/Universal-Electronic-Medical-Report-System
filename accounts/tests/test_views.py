from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from model_mommy import mommy

from payment.models import OrganisationFee

from organisations.models import OrganisationGeneralPractice, OrganisationClient, OrganisationMedidata
from accounts.models import ClientUser, GeneralPracticeUser, MedidataUser, User, GENERAL_PRACTICE_USER, CLIENT_USER, MEDIDATA_USER


class TestAccountBase(TestCase):
    def setUp(self):
        self.claim_organisation = OrganisationClient.objects.create(
            trading_name='Claim Organisation',
            legal_name='Claim Organisation',
            address='1, My Street, Kingston, New York 12401 United States',
            type=OrganisationClient.INSURANCE_CLAIM
        )

        self.underwriter_organisation = OrganisationClient.objects.create(
            trading_name='Underwriter Organisation',
            legal_name='Underwriter Organisation',
            address='2, My Street, Kingston, New York 12401 United States',
            type=OrganisationClient.INSURANCE_CLAIM
        )

        self.medidata_organisation = OrganisationMedidata.objects.create(
            trading_name='Medidata Organisation',
            legal_name='Medidata Organisation',
            address='3 Western Road Brighton East Sussex England BN1 2NW'
        )
        self.gp_organisation = OrganisationGeneralPractice.objects.create(
            name='Test Surgery 0001',
            practcode='TEST0001'
        )

        self.organisation_fee = mommy.make(
            OrganisationFee,
            gp_practice=self.gp_organisation,
            max_day_lvl_1=3,
            max_day_lvl_2=7,
            max_day_lvl_3=10,
            max_day_lvl_4=11,
            amount_rate_lvl_1=70,
            amount_rate_lvl_2=60,
            amount_rate_lvl_3=50,
            amount_rate_lvl_4=40
        )

        # create user
        self.claim_user_admin = User.objects._create_user(email='claim_user1@mohara.co', username='claim_user1',
                                                          password='medi2018', is_staff=True, type=CLIENT_USER)
        self.claim_user2 = User.objects._create_user(email='claim_user2@mohara.co', username='claim_user2',
                                                     password='medi2018', type=CLIENT_USER)
        self.claim_user3 = User.objects._create_user(email='claim_user3@mohara.co', username='claim_user3',
                                                     password='medi2018', type=CLIENT_USER)
        self.underwriter_user_admin = User.objects._create_user(email='underwriter_user1@mohara.co',
                                                                username='underwriter_user1', password='medi2018',
                                                                is_staff=True, type=CLIENT_USER)
        self.underwriter_user2 = User.objects._create_user(email='underwriter_user2@mohara.co',
                                                           username='underwriter_user2', password='medi2018',
                                                           type=CLIENT_USER)
        self.gp_user_admin = User.objects._create_user(email='gp_user1@mohara.co', username='gp_user1',
                                                       password='medi2018', is_staff=True, type=GENERAL_PRACTICE_USER)
        self.gp_user2 = User.objects._create_user(email='gp_user2@mohara.co', username='gp_user2', password='medi2018',
                                                  type=GENERAL_PRACTICE_USER)
        self.gp_user3 = User.objects._create_user(email='gp_user3@mohara.co', username='gp_user3', password='medi2018',
                                                  type=GENERAL_PRACTICE_USER)
        self.medidata_user1 = User.objects._create_user(email='medidata_user1@mohara.co', username='medidata_user1',
                                                        password='medi2018', type=MEDIDATA_USER)
        self.medidata_user2 = User.objects._create_user(email='medidata_user2@mohara.co', username='medidata_user2',
                                                        password='medi2018', type=MEDIDATA_USER)

        # create claim organisation's user
        ClientUser.objects.create(user=self.claim_user_admin, organisation=self.claim_organisation, role=ClientUser.CLIENT_ADMIN)
        ClientUser.objects.create(user=self.claim_user2, organisation=self.claim_organisation)
        ClientUser.objects.create(user=self.claim_user3, organisation=self.claim_organisation)

        # create underwriter organisation's user
        ClientUser.objects.create(user=self.underwriter_user_admin, organisation=self.underwriter_organisation)
        ClientUser.objects.create(user=self.underwriter_user2, organisation=self.underwriter_organisation)

        # create gp organisation's user
        GeneralPracticeUser.objects.create(user=self.gp_user_admin, organisation=self.gp_organisation,
                                           role=GeneralPracticeUser.PRACTICE_MANAGER)
        GeneralPracticeUser.objects.create(user=self.gp_user2, organisation=self.gp_organisation,
                                           role=GeneralPracticeUser.GENERAL_PRACTICE)
        GeneralPracticeUser.objects.create(user=self.gp_user3, organisation=self.gp_organisation,
                                           role=GeneralPracticeUser.GENERAL_PRACTICE)

        # create medidata organisation's user
        MedidataUser.objects.create(user=self.medidata_user1, organisation=self.medidata_organisation)
        MedidataUser.objects.create(user=self.medidata_user2, organisation=self.medidata_organisation)


class TestAccountView(TestAccountBase):

    def test_get_account_view(self):
        self.client.force_login(self.gp_user_admin)
        response = self.client.get(
            reverse('accounts:view_account')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/accounts_view.html')


class TestManageUser(TestAccountBase):

    def test_post_remove(self):
        # TODO: IMPLEMENT POST REMOVE USER TEST
        pass

    def test_post_change(self):
        # TODO: IMPLEMENT POST CHANGE USER TEST
        pass

    def test_reset_pasword(self):
        # TODO: IMPLEMENT POST RESET PASSWORD USER TEST
        pass


class TestViewUser(TestAccountBase):

    def test_get_view_user_by_gp_manager(self):
        self.client.force_login(self.gp_user_admin)
        response = self.client.get(
            reverse('accounts:view_users'), {
                'type': 'allType'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_management.html')

    def test_get_view_user_by_client_admin(self):
        self.client.force_login(self.claim_user_admin)
        response = self.client.get(
            reverse('accounts:view_users'), {
                'type': 'allType'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_management.html')

    def test_get_view_user_by_medidata(self):
        self.client.force_login(self.medidata_user1)
        response = self.client.get(
            reverse('accounts:view_users'), {
                'type': 'allType'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_management.html')


class TestViews( TestCase ):
    def setUp( self ):
        #   Prepare request for test.
        self.userNameTest = 'testMedi007'
        self.method = 'POST'
        self.request = RequestFactory()

        #   create User_A in DB.
        #   create userProfile.
        self.userName_A = 'pringleUser'
        self.firstName_A = 'Pringle'
        self.lastName_A = 'Iphone'
        self.email_A = 'medi001@mohara.co'
        self.password_A = 'secret'
        self.role_A = '1'

        #   create organisationProfile
        self.organisation_A = 'Test organisation.'
        self.practCode_A = 'TEST0001'

        self.gp_practice = mommy.make( OrganisationGeneralPractice, name = self.organisation_A, practcode = self.practCode_A )
        self.userProfileA = mommy.make( User, username = self.userName_A, password = self.password_A, first_name = self.firstName_A, last_name = self.lastName_A, email = self.email_A )
        self.userA = mommy.make( GeneralPracticeUser,
            organisation = self.gp_practice,
            user = self.userProfileA,
            role = self.role_A,
            title = 'DR'
        )
        
        #   create userTest for request
        user = User.objects.create( username='testuser', email = 'testuser@mohara.co', first_name='testuser', is_active = True, type = GENERAL_PRACTICE_USER )
        user.set_password('secret')
        user.save()

        self.request_user = mommy.make(
            GeneralPracticeUser,
            organisation = self.gp_practice,
            user = user,
            role = 0,
            title = 'MR'
        )

    def test_create_user_exist( self ):
        #   Test create function but fail. Because exist account
        firstName = 'Jirayu'
        lastName = 'Oopipat'
        email = self.email_A
        password = 'secret1'
        role = '1'

        self.client.login( email = 'testuser@mohara.co', password = 'secret' )
        response = self.client.post('/accounts/create-user/', {
            'user_role' : role,
            'first_name': firstName,
            'last_name': lastName,
            'email': email,
            'password' : password
        })

        expectedMassage = 'User Account Existing In Database'
        messages = list( response.context[ 'messages' ] )

        self.assertEqual( 200, response.status_code )
        self.assertEqual( 1, len( messages ) )
        self.assertEqual( expectedMassage, str( messages[0] ) )

    def test_create_user_success( self ):
        #   Test create user and success.
        firstName = 'Jirayu'
        lastName = 'Oopipat'
        email = 'snoopy@mohara.co'
        password = 'secret2'
        role = '1'

        self.client.login( email = 'testuser@mohara.co', password = 'secret' )
        response = self.client.post('/accounts/create-user/', {
            'user_role' : role,
            'first_name': firstName,
            'last_name': lastName,
            'email': email,
            'password' : password
        })

        queryResultUser = User.objects.all()
        resultUser = queryResultUser[2]

        self.assertEqual( 302, response.status_code )
        self.assertEqual( 3, len( queryResultUser ) )
        self.assertEqual( email, resultUser.email )
        self.assertEqual( email, resultUser.username )
        self.assertEqual( firstName, resultUser.first_name )
        self.assertEqual( lastName, resultUser.last_name )
        self.assertEqual( 'General Practice User', resultUser.get_my_role() )

    def test_create_user_fail( self ):
        #   Test create user but fail. Because invalid form.
        firstName = 'Jirayu'
        lastName = 'Oopipat'

        self.client.login( email = 'testuser@mohara.co', password = 'secret' )
        response = self.client.post('/accounts/create-user/', {
            'first_name': firstName,
            'last_name': lastName,
        })

        expectedMassage = 'Please input all the fields properly.'
        messages = list( response.context[ 'messages' ] )

        self.assertEqual( 200, response.status_code )
        self.assertEqual( 1, len( messages ) )
        self.assertEqual( expectedMassage, str( messages[0] ) )


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email='user@gmail.com',
            type=GENERAL_PRACTICE_USER
        )
        user.set_password('User1234')
        user.save()

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(200, response.status_code)

    def test_two_factor_missing_data_redirect(self):
        response = self.client.get('/accounts/two-factor/')
        self.assertEqual(302, response.status_code)
        self.assertEqual("/accounts/login/", response.url)

    def test_login_ip_with_n3_hscn_redirect(self):
        response = self.client.post('/accounts/login/', {'username': 'user@gmail.com', 'password': 'User1234'}, REMOTE_ADDR="172.17.5.3")
        self.assertEqual(302, response.status_code)
        self.assertEqual("/instruction/view-pipeline/", response.url)

    def test_login_ip_outside_n3_hscn_redirect(self):
        response = self.client.post('/accounts/login/', {'username': 'user@gmail.com', 'password': 'User1234'}, REMOTE_ADDR="127.0.0.1")
        self.assertEqual(302, response.status_code)
        self.assertEqual("/accounts/two-factor/", response.url)
