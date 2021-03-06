# -*- coding: utf-8 -*-
""" GENERAL TEST DESCRIPTION HERE

TODO: -

command line call:    python tests.py <Test_Case_Name>[.<Test_Method>] [<Test_Case_Name>.<Test_Method>]...
Test_Case_Name:       class name
Test_method:          optional argument
Example:              python tests.py TestRegisterDefinition.test_xxx
"""
import time
import unittest
import sys
import os
import xmlrunner
sys.path.extend(["../", "../plugins/"])
import registerDefinition
import vhdlFileParser
import IpCoreGeneration
from plugins.generateTextRegisterMap import *
from plugins.generateHtmlRegisterMap import *
from plugins.generatePythonRegisterMap import *
from plugins.generateCRegisterMap import *


class TestIpCoreGeneration(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_ipcore_generation(self):
        ''' file parser test '''
        template_path = r'../template/axi_template.vhd'
        for temp_file in ['test_example_1.yml', 'test_example_2.yml']:
            OUTPUT_PATH = os.getcwd() + '/../generated/{0}_v1_0_S00_AXI.vhd'
            definition = IpCoreGeneration.YamlDefinition(os.getcwd() + '/../generation/' + temp_file)
            IpCoreGeneration.VhdlWriter(template_path, OUTPUT_PATH.format(definition.component_name.lower()), definition)


class TestGenerateComponentIndex(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        ''' file header_generation test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        GenerateHTMLMap(parser, 'test.html')
        GenerateComponentIndex([[parser.component_name, parser.ip_core_version, parser.register], ], 'test{0}')


class TestGenerateHTMLMap(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        ''' file header_generation test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateHTMLMap(parser, 'test.html')
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGenerateTextRegisterMap(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        ''' file header_generation test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateTextRegisterMap(parser, 'test.txt')
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGeneratePythonModule(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        ''' file header_generation test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GeneratePythonModule(parser, 'test.pyc')
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGenerateCHeader(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        ''' file header_generation test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateCHeader(parser, 'test.h')
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestVhdlFileParser(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_instantiation(self):
        ''' file parser test '''
        parser = vhdlFileParser.FileParseOperation(os.getcwd() + '/../ip_repo/test_v1_0_S00_AXI.vhd')
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})


class TestRegisterDefinition(unittest.TestCase):
    """ Testcase for checking RegisterDefinition class"""

    def test_instantiation(self):
        ''' will only test the successfull instantiation '''
        reg_def = registerDefinition.RegisterDefinition()
        self.assertEqual(reg_def.component_name, None)
        self.assertEqual(reg_def.orginal_slave_name, None)
        self.assertEqual(reg_def.variable_name, None)
        self.assertEqual(reg_def.binary_coded, None)
        self.assertEqual(reg_def.ip_core_version, None)
        self.assertEqual(reg_def.ip_core_version_naming, None)
        self.assertEqual(reg_def.documentation, None)
        self.assertEqual(reg_def.bit_definition, [])

    def test_string_return(self):
        ''' will test the __str__ function '''
        reg_def = registerDefinition.RegisterDefinition()
        self.assertIsNotNone(str(reg_def))

    def test_add_bit_definition(self):
        ''' will test the __str__ function '''
        reg_def = registerDefinition.RegisterDefinition()
        reg_def._add_bit_definition('test', 0)
        self.assertEqual(reg_def.bit_definition, [['test', 0]])
        reg_def._add_bit_definition('test')


if(__name__ == '__main__'):
    # Note:
    # The loader that sorts the test by their order of definition doesn't
    # work on Python 3.
    BEGIN_TIME = time.time()
    SUITE = unittest.TestSuite()
    if(len(sys.argv)) < 2:
        if(not os.path.exists('coverage')):
            os.mkdir('coverage')
        with open('coverage/test-results.xml', 'w') as output:
            unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output),
                          # these make sure that some options that are not applicable
                          # remain hidden from the help menu.
                          failfast=False, buffer=False, catchbreak=False)
    else:
        while(len(sys.argv) > 1):
            TMP_ARGUMENT = sys.argv.pop(1)
            if(TMP_ARGUMENT[0:2] == '--'):
                # add optional parameter here
                pass
            else:
                # split the test method from test class
                TEST_ARGUMENT = TMP_ARGUMENT.split('.')
                if(len(TEST_ARGUMENT) == 2):
                    TEST_CASE = TEST_ARGUMENT[0]
                    TEST_METHOD = TEST_ARGUMENT[1]
                    SUITE.addTest((eval(TEST_CASE))(TEST_METHOD))
                elif(len(TEST_ARGUMENT) == 1):
                    TEST_CASE = TEST_ARGUMENT[0]
                    if(SUITE != unittest.TestSuite()):
                        raise Exception('ERROR: Cannot have multiple test suites!')
                    SUITE = unittest.TestLoader().loadTestsFromTestCase(eval(TEST_CASE))
                else:
                    raise Exception('ERROR: invalid test case specification!')
        # set the test runner with parameters (description, verbosity, stream)
        # description means the test method description
        # verbosity is the output for the test suite
        # stream is a stream that can be output to other instances for example see code below:
        #
        # from StringIO import StringIO
        #
        # stream = StringIO()
        # runner = unittest.TextTestRunner(stream = stream)
        # print('Test Output\n{}'.format(stream.read()))
        RUNNER = unittest.TextTestRunner(descriptions=False, verbosity=2)
        TEST_RESULTAT = RUNNER.run(SUITE)
        print('Time elapsed: {0}sec'.format(time.time() - BEGIN_TIME))
        # check for errors or failures and return 0 or 1
        if((TEST_RESULTAT.errors != []) or (TEST_RESULTAT.failures != [])):
            sys.exit(1)
        else:
            sys.exit(0)
