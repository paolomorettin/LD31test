
class COINFLIP_Parser :

    special_characters = [';','(',')','=',',']

    @classmethod
    def tokenize(cls,code) :        
        code = code.upper()
        for sc in cls.special_characters :
            code = code.replace(sc,' {} '.format(sc))
        code = code.replace('\n',' ')
        return code.strip().split()
        

    @staticmethod
    def parse_code(code) :
        tokens = COINFLIP_Parser.tokenize(code)

        program = ''
        declaration = []
        for t in tokens :
            if t == ';' :
                program += COINFLIP_Parser(
            
        
