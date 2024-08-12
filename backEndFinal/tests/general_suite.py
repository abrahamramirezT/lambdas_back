import unittest
import tests.unit.test_app_update_incidence as test_update_incidence
import tests.unit.test_app_set_password as test_set_password
import tests.unit.test_app_read_all_incidences as test_read_all_incidences
import tests.unit.test_app_login as test_login
import tests.unit.test_app_delete_incidence as test_delete_incidence
import tests.unit.test_app_create_user as test_create_user
import tests.unit.test_app_create_incidence as test_create_incidence

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_update_incidence))
suite.addTests(loader.loadTestsFromModule(test_set_password))
suite.addTests(loader.loadTestsFromModule(test_read_all_incidences))
suite.addTests(loader.loadTestsFromModule(test_login))
suite.addTests(loader.loadTestsFromModule(test_delete_incidence))
suite.addTests(loader.loadTestsFromModule(test_create_user))
suite.addTests(loader.loadTestsFromModule(test_create_incidence))



runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)