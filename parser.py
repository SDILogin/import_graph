import re, os

class Parser:
    def __init__(self, module_code):
        self.regex_find_result = []
        self.module_code = module_code
        self.regex = re.compile('#import [<"]+[a-zA-Z][a-zA-Z0-9]*.[(hpp)(c)(m)(h)][>"]')
        self.parsed = []

    def parse_modules_name(self):
        regex_find_result = self.regex.findall(self.module_code)
        self.parsed = [x[len('#import <'):-1] for x in regex_find_result]
        return self.parsed

class FileParser:
    def __init__(self, file_name):
        f = open(file_name, 'r')
        self.parser = Parser(f.read())

    def parse_modules_name(self):
        self.parsed = self.parser.parse_modules_name()
        return self.parsed

if __name__ == '__main__':
    # simple_text = '\n\n\n\n\#import <some.h>\n#import <some2.h>'
    # parser = FileParser('/Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno/VZVZRSimpleViewController.m')
    # res = parser.parse_modules_name()
    # print(*res, sep='\n')
    files_in_dir, full_file_names = [], []
    for root, dirs, file_names in os.walk('/Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno'):
        files = [x for x in file_names if x.endswith('.h')]
        full_file_names += [root+'/'+x for x in files]
        files_in_dir +=  files
    
    G = {}
    for file_in_dir in full_file_names:
        parser = FileParser(file_in_dir)
        imported_modules = parser.parse_modules_name()
        G[file_in_dir] = imported_modules

    print(G)