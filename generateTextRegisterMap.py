from templateFileGeneration import *


class GenerateTextRegisterMap(TemplateGeneration):

    FILE_ENDING = '.txt'
    BIT_DEFINE_STRING = '\t\t{2}[{0}] = {1};\n'
    GENERAL_REGISTER_DEFINITION = '{0:<70}{1:>20}{2:>20}\n{3}'
    REGISTER_BIT_INFORMATION = '{0} {1}\n\n{2}\n'
    COMPONENT_NAMING_AND_DEFINTION = 180*'#' + '\nComponent {0} (IP Core Version: {1})\n{2}\n'
    AUTOGENERATION_HINT = '# This file is automatically generated, don''t modify it! #\n'

    def _extract_register_information(self):
        ''' extraction of the slave register and all including bits '''
        return_string = ''
        keylist = self.parsed_file.register.keys()
        keylist.sort()
        property_comment = '\t# this will add the property name to the class\n'
        for temp_reg in keylist:
            add_property = ''
            return_string += self.GENERAL_REGISTER_DEFINITION.format(self._extract_variable_name(temp_reg),
                                                                     self._calculate_register_offset(self.parsed_file.register[temp_reg].binary_coded[2:]),
                                                                     self._extract_read_write_option(self.parsed_file.register[temp_reg].option), 180*'-')
            return_string += self.REGISTER_BIT_INFORMATION.format(self._extract_bit_defintion(self.parsed_file.register[temp_reg].bit_definition), add_property, 180*'.')
        return return_string

    def _write(self):
        ''' write the whole file '''
        self.output_file.write(self.AUTOGENERATION_HINT)
        out_string = self._extract_register_information()
        self.output_file.write(self.COMPONENT_NAMING_AND_DEFINTION.format(self.parsed_file.component_name, self.parsed_file.ip_core_version, out_string))
