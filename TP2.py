class ErrorCode(Exception):
    def __init__(self, msg):
        self.msg = msg

class Paterson:
    def __init__(self, instruction, hex_code):
        self.hex_code = hex_code
        self.instruction = instruction

        if len(hex_code) != 10:
            raise ErrorCode("Codigo em Hexadecimal com tamanho inapropriado")
        
        self.resultados = []  # Inicialize uma lista para armazenar os resultados
        #codigo_hexadecimal = "0x00C94022"
        #codigo_bin = bin(int(codigo_hexadecimal, 16))[2:].zfill(32)  # Converte para binário e preenche com zeros à esquerda

    def Tipo_R(self, hex_code):
        hex_code = hex_code[2:] if hex_code.startswith("0x") else hex_code  
        binary_code = "" #string que armazena o binario

        for digit in hex_code:
            binary_code += f"{int(digit, 16):04b}" #converte pra binario em separação de 4 bits


        #print(binary_code)
        binario= self.append(binary_code)
        op_code = binario[0: 6]
        rs = binario[6: 11]
        rt = binario[11: 16]
        rd = binario[16: 21]
        shamt = binario[21: 26]
        funct = binario[26: 32]

        op_code_map = {'0': 6, '1': 6}
        funct = op_code_map.get(op_code, 0) #valor padrao 0
        binario = ({'op_code': op_code, 'rs': rs, 'rt': rt, 'rd': rd, 'shamt': shamt, 'funct': funct})
    
    def codigos(self):
        tipos = ['Tipo-R', 'Tipo-I', 'Tipo-J']
        codigos_zero = {'sltiu': 11, 'lw': 23, 'sw': 43, 'beq' : 4, 'j': 2}
        codigos_um = {'sub' : 34, 'and' : 36, 'or': 37}
        

    def registradores(instruction):
        registradores_mips = {
            '$zero': 0, '$at': 1, '$v0': 2, '$v1': 3, '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
            '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
            '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
            '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27, '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
        }


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
