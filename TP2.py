from typing import Any

class ErrorCode(Exception):
    def __init__(self, msg):
        self.msg = msg

class ErrorRegistrador(Exception):
    def __init__(self, msg):
        self.msg = msg

class Paterson:
    def __init__(self):
        self.registradores_mips = { 0: '$zero', 1: '$at', 2: '$v0', 3: '$v1', 4: '$a0', 5: '$a1', 6: '$a2', 7: '$a3',
    8: '$t0', 9: '$t1', 10: '$t2', 11: '$t3', 12: '$t4', 13: '$t5', 14: '$t6', 15: '$t7',
    16: '$s0', 17: '$s1', 18: '$s2', 19: '$s3', 20: '$s4', 21: '$s5', 22: '$s6', 23: '$s7',
    24: '$t8', 25: '$t9', 26: '$k0', 27: '$k1', 28: '$gp', 29: '$sp', 30: '$fp', 31: '$ra'}
        self.resultados = [] #armazenar os resultados em listas
        self.tipoI = {11: 'sltiu', 23: 'lw', 43: 'sw', 4: 'beq'} #dicionario das intruções tipo I
        self.tipoR= {34: 'sub', 36: 'and', 37: 'or'}#dicionario das intruções tipo R
        self.tipoJ = {2: "j"} #dicionario das intruções tipo J
    
    def tipoR_func(self, op_code, rs, rt, rd, shamt, funct):
        pass
    
    def tipoI_func(self,op_code, rs, rt, const):
        pass

    def tipoJ_func(self,op_code,address):
        pass

        #aqui em cima tá as linhas separadas pra montagem da decodificação em formato de instrução mips

    def desmonta(self, hex_code):
        if len(hex_code) != 10:
            raise ErrorCode("Código em Hexadecimal com tamanho inapropriado")
        
        hex_code = hex_code[2:] if hex_code.startswith("0x") else hex_code  # hex_code recebe o binario sem os primeiros dois digitos 0x
        
        binary_code = "" #string que armazena o binário

        for numero in hex_code:
            binary_code += f"{int(numero, 16):04b}" #converte para binário em separação de 4 bits
        print(binary_code)
        op_code = int(binary_code[0:6])
        
        if op_code == 0:                
            rs = int(binary_code[6: 11], 2)
            rt = int(binary_code[11: 16], 2)
            rd = int(binary_code[16: 21], 2)
            shamt = int(binary_code[21: 26], 2)
            funct = int(binary_code[26: 32], 2)
        
            
            op_code_nome = self.registradores_mips.get(int(op_code))
            rs_nome = self.registradores_mips.get(int(rs))
            rt_nome = self.registradores_mips.get(int(rt))
            rd_nome = self.registradores_mips.get(int(rd))
            shamt_nome = self.registradores_mips.get(int(shamt))
            funct_nome = self.registradores_mips.get(int(funct))

            funcao_op_code = op_code_nome + funct_nome

            #verificação de erros:
            if not funcao_op_code:
                raise ErrorCode(f'{op_code} não é uma função MIPS válida')
            if rs_nome is None:
                raise ErrorRegistrador(f"{rs} não é um registrador MIPS válido")
            if rt_nome is None:
                raise ErrorRegistrador(f"{rt} não é um registrador MIPS válido")
            if rd_nome is None:
                raise ErrorRegistrador(f"{rd} não é um registrador MIPS válido")

            #junção do tipo R
            self.resultados.append({'tipo': 'Tipo R', 'funcao_op_code': funcao_op_code,
                        'rs_nome': rs_nome, 'rt_nome': rt_nome, 'rd_nome': rd_nome,})


        elif op_code == 2:
            address= binary_code[6:32]
            #tipoJ_func(op_code, address)
            pass

        else:
            rs = int(binary_code[6: 11])
            rt = int(binary_code[11: 16])
            
            if int(binary_code[16]== 1): 
                const = int(binary_code[17:32])
                const = const-pow(2,15)
                constante = const
            else:
                const = int(binary_code[16: 32])
            #tipoI_func(op_code, rs, rt, constante)
        
        #funct = op_code_map.get(op_code, 0) #valor padrão 0
        
    #def carregar_codigo(self, filename, code_type):
    #    with open(filename, 'r') as file:
    #        lines = file.readlines()
    #        for line in lines:
    #            self.Tipo_R(line)  # Processar as linhas como Tipo-R (ajuste para outros tipos)

    def escrever(self, entrada, saida):
            with open(entrada, 'r') as file:
                linhas = file.readlines()
                for linha in linhas:
                    print(linha)
                    self.desmonta(linha)  

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
    entrada = "entrada.asm" #limpei o main aqui
    saida = "saida.asm"
    paterson = Paterson()
    paterson.escrever(entrada, saida)
