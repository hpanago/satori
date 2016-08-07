#-*- coding: utf-8 -*-

program_name = 'Satori (悟り)'
version = '0.06'
description = '''

'''


last_compatible = '0.04'

meta_tags = [ 'program', 'version', 'system', 'date', 'excludes', 'user', 'modes', 'hostname', 'UID', 'GID' ]

meta_templates = {}
meta_templates['program'] = 'Created by {0}'
meta_templates['version'] = 'Image version: {0}'
meta_templates['system'] = "System string is '{0}'"
meta_templates['date'] = "Created on '{0}'"
meta_templates['excludes'] = "Excluded directories: '{0}'"
meta_templates['modes'] = "Supported modes are: '{0}'"
meta_templates['user'] = "Image created as user: '{0}'"
meta_templates['UID'] = "Image created by User ID: '{0}'"
meta_templates['GID'] = "Image created as Group ID: '{0}'"
meta_templates['hostname'] = "Machine's hostname is: '{0}'"



file_tags = [ 'filename', 'path', 'owner', 'group', 'size', 'privileges', 'type', 'content', 'SHA2' ]


banner = '''
   ▄████████    ▄████████     ███      ▄██████▄     ▄████████  ▄█  
  ███    ███   ███    ███ ▀█████████▄ ███    ███   ███    ███ ███  
  ███    █▀    ███    ███    ▀███▀▀██ ███    ███   ███    ███ ███▌ 
  ███          ███    ███     ███   ▀ ███    ███  ▄███▄▄▄▄██▀ ███▌ 
▀███████████ ▀███████████     ███     ███    ███ ▀▀███▀▀▀▀▀   ███▌ 
         ███   ███    ███     ███     ███    ███ ▀███████████ ███  
   ▄█    ███   ███    ███     ███     ███    ███   ███    ███ ███  
 ▄████████▀    ███    █▀     ▄████▀    ▀██████▀    ███    ███ █▀   
                                                   ███    ███      '''


header = '''%s
Welcome to %s 
{0}
Version %s
''' % ( banner, program_name, version )

cant_read_file = "	[X] File '%s' could not be read. Quiting..."



bash_n_color="\033[0m"
bash_l_gray="\033[0;37m"

#="\[\033[0;37m\]"
