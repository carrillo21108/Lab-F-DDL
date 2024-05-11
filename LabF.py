import LRLib

grammar = {
    'E':["E + T",'T'],
    'T':["T * F",'F'],
    'F':['( E )','id']
}

LRLib.print_parsing_table(LRLib.generate_SLRTable())