#primeira versão, ainda com muita coisa pra arrumar mas já da pra ver um esboço se formando

class ErrorCode(Exception):
    def __init__(self, msg):
        self.msg = msg

class Paterson:
    def __init__(self, instruction, code):
        self.code = code
        self.instruction = instruction

        if len(code) != 10:
            raise ErrorCode("Codigo em Hexadecimal com tamanho inapropriado")
        
        self.resultados = []  # Inicialize uma lista para armazenar os resultados

    def Tipo_R(self, code):
        op_code = code[0]
        op_code_map = {'0': 6, '1': 6}
        rs = code[1:6]
        rt = code[6:11]
        rd = code[11:16]
        shamt = code[16:21]
        funct = op_code_map[op_code]

        # Faça algo com as informações, como armazená-las na lista de resultados
        self.resultados.append({'op_code': op_code, 'rs': rs, 'rt': rt, 'rd': rd, 'shamt': shamt, 'funct': funct})

    def carregar_codigo(self, filename, code_type):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.Tipo_R(line)  # Processar as linhas como Tipo-R (ajuste para outros tipos)

    def save_to_file(self, file):
        with open(file, "w") as f:
            for resultado in self.resultados:
                f.write(f"Operação: Tipo-R\n")
                f.write(f"op_code: {resultado['op_code']}\n")
                f.write(f"rs: {resultado['rs']}\n")
                f.write(f"rt: {resultado['rt']}\n")
                f.write(f"rd: {resultado['rd']}\n")
                f.write(f"shamt: {resultado['shamt']}\n")
                f.write(f"funct: {resultado['funct']}\n")

if __name__ == '__main__':
    p = Paterson("instrução", "código")
    p.carregar_codigo('teste.asm', 'Tipo-R')
    p.save_to_file('resultado.txt')
