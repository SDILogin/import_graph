import re, os, graph

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
    files_in_dir, full_file_names, name_full_name_pair = [], [], []
    for root, dirs, file_names in os.walk('/Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno'):
        files = [x for x in file_names if x.endswith('.h')]
        full_file_names += [root+'/'+x for x in files]
        files_in_dir +=  files
        name_full_name_pair += list(zip(files, full_file_names))
    
    G = {}
    for file_in_dir in name_full_name_pair:
        full_name = file_in_dir[1]
        short_name = file_in_dir[0]
        parser = FileParser(full_name)
        imported_modules = parser.parse_modules_name()
        G[short_name] = imported_modules

    gr = graph.Graph(G)
    print('nodes: ', *gr.nodes, sep='\n')
    print('-'*10)
    print('edges: ', *[str(x[0])+'->'+str(x[1]) for x in gr.edges], sep='\n')