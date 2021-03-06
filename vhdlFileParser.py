from registerDefinition import *
import re

REGISTER_SIZE = 32
REGEX_SLAVE_REG_NAME = re.compile(r'(?:slv\w+[^\W_])')
REGEX_SLAVE_REG_DEFINITION = re.compile(r'(?:slv_reg\d+\(\d+\))')
REGEX_SLAVE_REG_ALIAS_NAME = re.compile(r'(?:(?<=a_)\w+)')
REGEX_VERSION_NAME = re.compile(r'(\w+)(?:_VERSION)')
REGEX_VERSION_NUMBER_HEX = re.compile(r'(?<=x\")[^\"]\d+[^\"]')
REGEX_VERSION_NUMBER_BIN = re.compile(r'(?<=b\")[0-1]+')
REGEX_REGISTER_DEFINITION = re.compile(r'(?<=\()(\d+)[^\b](\w+)[^\b](\d+)|(?<=\()(\d+)')


class FileParseOperation():

    def __init__(self, path):
        self.file_path = path
        self.variable_definition = False
        self.process = False
        self.read_process = False
        self.write_process = False
        self.ip_core_version = None
        self.ip_core_version_naming = None
        self.register = {}
        self.component_name = self._extract_component_name()
        self._parse_file_for_slave_register()

    def _extract_component_name(self):
        # to separate the component we need the "/" and also the "_v"
        return self.file_path[self.file_path.rfind('/') + 1:self.file_path.rfind('_v')].upper()

    def _extract_bit_definition(self, line):
        if(self.variable_definition):
            if('signal slv_reg' in line and 'signal slv_reg_' not in line):
                ############## extract the slave register name and get rid of unnecessary symbols ##############
                slave_name = REGEX_SLAVE_REG_NAME.search(line).group()
                self.register[slave_name] = RegisterDefinition()
                self.register[slave_name].component_name = self.component_name
                self.register[slave_name].orginal_slave_name = slave_name
                self.register[slave_name].binary_coded = bin(int(slave_name[slave_name.find('g') + 1:]))
            elif('alias' in line and 'slv_reg' in line):
                ############## extract big definition here ##############
                temp_reg_name = REGEX_SLAVE_REG_NAME.search(line).group()
                alias_name = REGEX_SLAVE_REG_ALIAS_NAME.search(line).group()
                definition = REGEX_REGISTER_DEFINITION.findall(line)
                bit_depth = definition[0]
                try:
                    self._get_alias_bit_definition(bit_depth, alias_name, temp_reg_name)
                except BaseException as e:
                    print(alias_name)
                    print('Cannot convert bit_depth "{0}" type: "{1}"\n{2}'.format(bit_depth, type(bit_depth), str(e)))

    def _get_alias_bit_definition(self, bit_depth, alias_name, temp_reg_name):
        if('downto' in bit_depth):
            bit_depth = [int(bit_depth[0]), int(bit_depth[2])]
            if((bit_depth[0] - bit_depth[1]) == REGISTER_SIZE - 1):
                self._extract_status_control(alias_name, temp_reg_name)
            elif((bit_depth[0] - bit_depth[1]) < REGISTER_SIZE - 1):
                self.register[temp_reg_name]._add_bit_definition(alias_name, [bit_depth, ])
        elif('to' in bit_depth):
            bit_depth = [int(bit_depth[0]), int(bit_depth[2])]
            if((bit_depth[1] - bit_depth[0]) == REGISTER_SIZE - 1):
                self._extract_status_control(alias_name, temp_reg_name)
            elif((bit_depth[1] - bit_depth[0]) < REGISTER_SIZE - 1):
                self.register[temp_reg_name]._add_bit_definition(alias_name, [bit_depth, ])
        else:
            self.register[temp_reg_name]._add_bit_definition(alias_name, [bit_depth[-1], ])

    def _extract_status_control(self, alias_name, temp_reg_name):
        self.register[temp_reg_name].variable_name = alias_name.upper()
        if('control' in alias_name):
            self.register[temp_reg_name].option['write'] = True
            self.register[temp_reg_name].option['finished'] = True
        elif('status' in alias_name):
            self.register[temp_reg_name].option['read'] = True
            self.register[temp_reg_name].option['finished'] = True

    def _check_address_and_register_binary(self, line):
        if('when b"' in line):
            temp_binary_address = bin(int(REGEX_VERSION_NUMBER_BIN.search(line).group(), 2))
            for temp_reg in self.register.keys():
                if(self.register[temp_reg].binary_coded == temp_binary_address):
                    return (temp_reg, True)
            return (None, False, int(REGEX_VERSION_NUMBER_BIN.search(line).group(), 2))

    def _extract_version_information(self, line):
        if('constant' in line and '_VERSION' in line):
            # we need the name for further mapping of the slv reg and also the version definition
            self.ip_core_version_naming = REGEX_VERSION_NAME.search(line).group()
            self.ip_core_version = REGEX_VERSION_NUMBER_HEX.search(line).group()

    def _setup_register(self, line):
        if('architecture' in line):
            self.variable_definition = True

    def _check_end_process(self, line):
        if('end process' in line):
            self.process = False
            self.read_process = False
            self.write_process = False
            self.version_check = False

    def _setup_boolean(self, line):
        if('process(S_AXI_ACLK)' in line.replace(' ', '')):
            self.process = True
        elif('process' in line and 'slv_reg_rden' in line and 'S_AXI_ARESETN' in line):
            self.read_process = True
            self.write_process = False
            self.process = False

    def _parse_file_for_slave_register(self):
        self.version_check = False
        self.temp_register_name = None
        for line in open(self.file_path, 'r').readlines():
            ############## extract variable definition here ##############
            self._setup_register(line)
            self._extract_bit_definition(line)
            self._extract_version_information(line)
            ############## read and write access must be defined ##############
            if('begin' in line):
                self.variable_definition = False
            self._setup_boolean(line)
            if(self.process and 'case loc_addr is' in line):
                self.write_process = True
            if(not self._check_read_process(line)):
                continue
            if(not self._check_write_process(line)):
                continue
            self._check_end_process(line)
        ############## set the attributes of the enumeration ##############
        for temp_register_map in self.register.keys():
            self.register[temp_register_map].ip_core_version = self.ip_core_version

    def _check_version(self, line):
        if(self.version_check):
            if(self.ip_core_version_naming is not None and self.ip_core_version_naming in line):
                temp_slv_name = 'slv_reg{0}'.format(self.temp_register_name)
                self.register[temp_slv_name] = RegisterDefinition()
                self.register[temp_slv_name].component_name = self.component_name
                self.register[temp_slv_name].orginal_slave_name = self.ip_core_version_naming
                self.register[temp_slv_name].binary_coded = bin(self.temp_register_name)
            self.version_check = False

    def _check_write_process(self, line):
        if(self.write_process):
            boolean_write = self._check_address_and_register_binary(line)
            if(boolean_write is None):
                return False
            elif(boolean_write[1]):
                self.register[boolean_write[0]].option['write'] = True
        return True

    def _check_read_process(self, line):
        if(self.read_process):
            boolean_read = self._check_address_and_register_binary(line)
            self._check_version(line)
            if(boolean_read is None):
                return None
            elif(len(boolean_read) > 2):
                self.version_check = True
                self.temp_register_name = boolean_read[2]
            elif(boolean_read[1]):
                self.register[boolean_read[0]].option['read'] = True
        return True
