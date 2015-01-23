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

class DirParser:
    def __init__(self, dir_name):
        self.dir = dir_name
        self.name_full_name_pair = []
        self._construct_meta()

    def _construct_meta(self):
        # /Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno
        self.name_full_name_pair = []
        for root, dirs, file_names in os.walk(self.dir):
            files = [x for x in file_names if x.endswith('.h')]
            self.name_full_name_pair += list(zip(files, [root+'/'+x for x in files]))    
        print(self.name_full_name_pair)

    def construct_graph(self):
        G = {}
        for file_in_dir in self.name_full_name_pair:
            full_name = file_in_dir[1]
            short_name = file_in_dir[0]
            parser = FileParser(full_name)
            imported_modules = parser.parse_modules_name()
            if len(imported_modules) > 0:
                G[short_name] = imported_modules

        self.graph = graph.Graph(G)

    def get_nodes(self):
        return self.graph.nodes

    def get_edges(self):
        return self.graph.edges

if __name__ == '__main__':
    # simple_text = '\n\n\n\n\#import <some.h>\n#import <some2.h>'
    # parser = FileParser('/Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno/VZVZRSimpleViewController.m')
    # res = parser.parse_modules_name()
    # print(*res, sep='\n')
    
    dp = DirParser('/Users/SDI/Desktop/IOSProjects/vesti-fm-ios/vestifm')
    dp.construct_graph()
    
    print('nodes: ', *dp.get_nodes(), sep='\n')
    print('-'*10)
    print('edges: ', *[str(x[0])+'->'+str(x[1]) for x in dp.get_edges()], sep='\n')