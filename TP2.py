from typing import Any

class ErrorCode(Exception):
    def __init__(self, msg):
        self.msg = msg

class ErrorRegistrador(Exception):
    def __init__(self, msg):
        self.msg = msg

class Paterson:
    def __init__(self):
        self.registradores_mips = self.registradores()
        self.resultados = []

    def Tipo_R(self, hex_code):
        hex_code = hex_code[2:] if hex_code.startswith("0x") else hex_code  
        
        if len(hex_code) != 10:
            raise ErrorCode("Código em Hexadecimal com tamanho inapropriado")
        
        binary_code = "" #string que armazena o binário

        for numero in hex_code:
            binary_code += f"{int(numero, 16):04b}" #converte para binário em separação de 4 bits

        op_code = binary_code[0: 6]
        rs = binary_code[6: 11]
        rt = binary_code[11: 16]
        rd = binary_code[16: 21]
        shamt = binary_code[21: 26]
        funct = binary_code[26: 32]

        op_code_map = {'0': 6, '1': 6}
        funct = op_code_map.get(op_code, 0) #valor padrão 0

        funcao_op_code = self.codigos(op_code, funct)
        rs_nome = self.registradores_mips.get(int(rs, 2)) # 2 de binário
        rt_nome = self.registradores_mips.get(int(rt, 2))
        rd_nome = self.registradores_mips.get(int(rd, 2))

        if not funcao_op_code:
            raise ErrorCode(f'{op_code} não é uma função MIPS válida')
        if rs_nome is None:
            raise ErrorRegistrador(f"{rs} não é um registrador MIPS válido")
        if rt_nome is None:
            raise ErrorRegistrador(f"{rt} não é um registrador MIPS válido")
        if rd_nome is None:
            raise ErrorRegistrador(f"{rd} não é um registrador MIPS válido")

        self.resultados.append({ 'op_code': op_code, 'funct': funct, 'rs_nome': rs_nome, 
                                 'rt_nome': rt_nome, 'rd_nome': rd_nome,})


    def codigos(self, op_code, funct):
        codigos_zero = {11: 'sltiu', 23: 'lw', 43: 'sw', 4: 'beq', 2: 'j'}
        codigos_um = {34: 'sub', 36: 'and', 37: 'or'}

        # op-code 0 ou 1
        if op_code == 0:
            return codigos_zero.get(funct, None)
        elif op_code == 1:
            return codigos_um.get(funct, None)

        return None

    def registradores(self):
        return{
            '$zero': 0, '$at': 1, '$v0': 2, '$v1': 3, '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
            '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
            '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
            '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27, '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
        }


    #def carregar_codigo(self, filename, code_type):
    #    with open(filename, 'r') as file:
    #        lines = file.readlines()
    #        for line in lines:
    #            self.Tipo_R(line)  # Processar as linhas como Tipo-R (ajuste para outros tipos)

    def desmontagem(self, entrada, saida):
            with open(entrada, 'r') as file:
                linhas = file.readlines()
                for linha in linhas:
                    self.Tipo_R(linha)  

            with open(saida, "w") as s:
                for resultado in self.resultados:
                    s.write(f"Operação: Tipo-R\n")
                    s.write(f"op_code: {resultado['op_code']}\n")
                    s.write(f"funct: {resultado['funct']}\n")
                    s.write(f"rs_nome: {resultado['rs_nome']}\n")
                    s.write(f"rt_nome: {resultado['rt_nome']}\n")
                    s.write(f"rd_nome: {resultado['rd_nome']}\n")
                    s.write(f"shamt: {resultado['shamt']}\n")
                    s.write("final do codigo\n")


if __name__ == '__main__':
    entrada = "entrada.asm"
    saida = "saida.asm"
    paterson = Paterson("intrução", "0x00cd0820")
    paterson.desmontagem(entrada, saida)
