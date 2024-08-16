import unittest
import tests.unit.test_app_update_incidence as test_update_incidence
import tests.unit.test_app_set_password as test_set_password
import tests.unit.test_app_read_all_incidences as test_read_all_incidences
import tests.unit.test_app_login as test_login
import tests.unit.test_app_delete_incidence as test_delete_incidence
import tests.unit.test_app_create_incidence as test_create_incidence
import tests.unit.test_read_aula_all as test_read_aula_all
import tests.unit.test_read_div_academica as test_read_div_academica
import tests.unit.test_read_edificio as test_read_edificio
import tests.unit.test_read_grado as test_read_grado
import tests.unit.test_read_grupo as test_read_grupo
import tests.unit.test_read_one_incidence as test_read_one_incidence
import tests.unit.test_app_update_only_status as tes_update_status


loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_update_incidence))
suite.addTests(loader.loadTestsFromModule(test_set_password))
suite.addTests(loader.loadTestsFromModule(test_read_all_incidences))
suite.addTests(loader.loadTestsFromModule(test_login))
suite.addTests(loader.loadTestsFromModule(test_delete_incidence))
suite.addTests(loader.loadTestsFromModule(test_create_incidence))
suite.addTests(loader.loadTestsFromModule(test_read_aula_all))
suite.addTests(loader.loadTestsFromModule(test_read_div_academica))
suite.addTests(loader.loadTestsFromModule(test_read_edificio))
suite.addTests(loader.loadTestsFromModule(test_read_grado))
suite.addTests(loader.loadTestsFromModule(test_read_grupo))
suite.addTests(loader.loadTestsFromModule(test_read_one_incidence))
suite.addTests(loader.loadTestsFromModule(tes_update_status))






runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)