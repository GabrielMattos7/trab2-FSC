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
        self.resultados = []
        self.tipoI = {11: 'sltiu', 23: 'lw', 43: 'sw', 4: 'beq'}
        self.tipoR= {34: 'sub', 36: 'and', 37: 'or'}
        self.tipoJ = {2: "j"}
    
    def tipoR_func(self, op_code, rs, rt, td, shamt, funct):
        pass
    
    def tipoI_func(self,op_code, rs, rt, const):
        pass

    def tipoJ_func(self,op_code,address):
        pass
    def desmonta(self, hex_code, tipoR_func, tipoI_func, tipoJ_func):
        if len(hex_code) != 10:
            raise ErrorCode("Código em Hexadecimal com tamanho inapropriado")
        
        hex_code = hex_code[2:] if hex_code.startswith("0x") else hex_code  
        
        binary_code = "" #string que armazena o binário

        for numero in hex_code:
            binary_code += f"{int(numero, 16):04b}" #converte para binário em separação de 4 bits
        print(binary_code)
        op_code = int(binary_code[0:6])
        


        if op_code == 0:                
         rs = int(binary_code[6: 11])
         rt = int(binary_code[11: 16])
         rd = int(binary_code[16: 21])
         shamt = int(binary_code[21: 26])
         funct = int(binary_code[26: 32])
         tipoR_func(op_code,rs, rt,rd,shamt,funct)
        

        elif op_code == 1:
            rs = int(binary_code[6: 11])
            rt = int(binary_code[11: 16])
            if int(binary_code[16]== 1): 
                const = int(binary_code[17:32])
                const = const-pow(2,15)
            else:
                const = int(binary_code[16: 32])
            tipoI_func(op_code, rs, rt, const)
        else:
            address= binary_code[6:32]
            tipoJ_func(op_code, address)
            pass
        #funct = op_code_map.get(op_code, 0) #valor padrão 0






        funcao_op_code = self.codigos(op_code, funct)
        rs_nome = self.registradores_mips.get(int(rs, 10)) # 2 de binário
        
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
    binary_string = "11111011"  # Substitua isso pelo seu número binário negativo

    # Use a função int() com a base 2 para converter o binário em decimal
    decimal_number = int(binary_string, 2)

    # O decimal_number agora conterá o valor inteiro equivalente ao número binário negativo
    print(decimal_number)
    entrada = "entrada.asm"
    saida = "saida.asm"
    paterson = Paterson()
    paterson.escrever(entrada, saida)
