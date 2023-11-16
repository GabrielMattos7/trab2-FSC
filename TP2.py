class ErrorCode(Exception):
    def __init__(self, msg):
        self.msg = msg

class ErrorRegistrador(Exception):
    def __init__(self, msg):
        self.msg = msg

class Paterson:
    def __init__(self):
        #dicionario com chave sendo numero
        self.registradores_mips_num = { 0: '$zero', 1: '$at', 2: '$v0', 3: '$v1', 4: '$a0', 5: '$a1', 6: '$a2', 7: '$a3',
    8: '$t0', 9: '$t1', 10: '$t2', 11: '$t3', 12: '$t4', 13: '$t5', 14: '$t6', 15: '$t7',
    16: '$s0', 17: '$s1', 18: '$s2', 19: '$s3', 20: '$s4', 21: '$s5', 22: '$s6', 23: '$s7',
    24: '$t8', 25: '$t9', 26: '$k0', 27: '$k1', 28: '$gp', 29: '$sp', 30: '$fp', 31: '$ra'}
        
        #dicionario com chave sendo string
        self.registradores_mips_string = { '$zero': 0, '$at': 1, '$v0': 2, '$v1': 3, '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
    '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11, '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
    '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19, '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
    '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27, '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31}
        
        #instruções para desmontar
        self.resultados_desmonta = [] #armazenar os resultados_desmonta em listas
        self.resultados_montar = []
        self.tipoI_num = {11: 'sltiu', 23: 'lw', 43: 'sw', 4: 'beq'} #dicionario das intruções tipo I
        self.tipoR_num = {34: 'sub', 36: 'and', 37: 'or'}#dicionario das intruções tipo R
        self.tipoJ_num = {2: "j"} #dicionario das intruções tipo J
        self.address_inicial = 0x00400000     

        #instruções para montar
        self.tipoI_string = {'sltiu': 11, 'lw': 23, 'sw': 43, 'beq': 4}
        self.tipoR_string = {'sub': 34, 'and': 36, 'or': 37}
        self.tipoJ_string = {'j': 2}
        self.num_loops = 0
        self.label_loop = {}
        # if label_loop[current_address]: write label_loop[current_address] na linba atual
                #label_1: 4
    def label(self):
        self.num_loops += 1
        return f"label_{self.num_loops}" # gera os labels com numeros crescentes

    def __str__(self):
        return '\n'.join(self.resultados_desmonta)

    def desmonta(self, hex_code,linha1):
        if len(hex_code) > 10:
            raise ErrorCode("Código em Hexadecimal com tamanho inapropriado")
        
        hex_code = hex_code[2:]
        binary_code = "" #string que armazena o binário

        for numero in hex_code:
            binary_code += f"{int(numero, 16):04b}" #converte para binário em separação de 4 bits

        op_code = int(binary_code[0:6],2)

        #tipo R
        if op_code == 0:                
            rs = int(binary_code[6: 11], 2)
            rt = int(binary_code[11: 16], 2)
            rd = int(binary_code[16: 21], 2)
            shamt = int(binary_code[21: 26], 2)
            funct = int(binary_code[26: 32], 2)
            
            op_code_nome = self.tipoR_num.get(op_code)
            rs_nome = self.registradores_mips_num.get(int(rs))
            rt_nome = self.registradores_mips_num.get(int(rt))
            rd_nome = self.registradores_mips_num.get(int(rd))
            shamt_nome = self.registradores_mips_num.get(int(shamt))
            funct_nome = self.tipoR_num.get(int(funct))

            #junção do tipo R
            instrucao = f"{funct_nome}, {rd_nome}, {rt_nome}, {rs_nome}"
            self.resultados_desmonta.append(instrucao)
            with open("saida_hex.asm", "a+") as s_hex:
                s_hex.write(instrucao + '\n')

        #tipo J
        elif op_code == 2:
            address= binary_code[6:32] #binario

            address = "0000"+ str(address) + "00"
            # label_add = current_addr + (deslocamento * 4) + 4

            hex_num = "0x"
            for i in range(0, len(address), 4):
                var = address[i: i+4]
                hex_num += str(hex(int(var, 2))[2:])
            
            address = int(hex_num,16) #endereco estar em hexa do jeito certo para ser subtraido
            address -= 0x00400000 # eh para estar com algo ai 
            linha_pra_Escrever_label = address + (1)
            distancia_de_linhas = int((int(address))/4) + 1 #para saber quantas instrucoes esta distante 
            label = self.label()
            
            self.label_loop[label] = distancia_de_linhas #adiciona ao dicionario
            instrucao = f"j {label}"
            with open("saida_hex.asm", "a+") as s_hex:
                s_hex.write(instrucao + '\n')

        

        #tipo I
        else:
            rs = int(binary_code[6: 11],2)
            rt = int(binary_code[11: 16],2)
            op_code = int(binary_code[0: 6],2) #divide o binario e coloca os numeros decimais corretos
            #calculo de negativo
            if int(binary_code[16])== 1:
                const = int(binary_code[16:32],2) - pow(2,16)
            else:
                const = int(binary_code[16: 32],2)

            op_code_nome = self.tipoI_num.get(int(op_code))
            rs_nome = self.registradores_mips_num.get(int(rs))
            rt_nome = self.registradores_mips_num.get(int(rt))
            if op_code == 4: 
                        
                #const vai ser um endereço para escrever un label
                #const+=1  #incrementa op_code

                print("const incrementado", const)
                contador =1 
                print("JAckson",op_code_nome)

                line_to_write= linha1+1 + const
                    #contador+1 por que o loop nao chega em beq, pois ainda nao fez append da operação    contador+=1
                #line_to_write está correto aparentemente
                label = self.label()
                self.label_loop[label] = line_to_write
            #junção do tipo I
            instrucao = f"{op_code_nome}, {rt_nome}, {rs_nome}, {const}"
            self.resultados_desmonta.append(instrucao)
        print("\n"*3)
        print(self.label_loop)
        for item, value in self.label_loop.items():
            contador = 1 
            for i, instrucao in enumerate(self.resultados_desmonta):
                print(value , "->>" , i )
                if  int(value) == int(contador):
                    print(item +":  "+ instrucao)
                    nova_instrucao = (item +":  "+ instrucao)
                    self.resultados_desmonta[i]=nova_instrucao
            contador+=1

    def montar(self, instruction):
        div = instruction.split() #divide a instrução 
        print("\ndividindo em partes: ", div)
        if len(div) < 2:
            print("Ignorando linha sem instruções MIPS: ", instruction)
            return instruction
        #tentavida de arumar o label:
        label = None
        # Verifica se a instrução contém um rótulo (label)
        if ':' in div[0]:
            label = div[0]
            div = div[1:]  # Remove o rótulo da lista


        function = div[0].lower() #pega a função
        

        #montar tipo R
        if function in self.tipoR_string:

            rs = self.registradores_mips_string[div[2].rstrip(',')] #separa as string dos registradores 
            rt = self.registradores_mips_string[div[3]]
            rd = self.registradores_mips_string[div[1].rstrip(',')]
            funct = self.tipoR_string[function] #le a instrução e separa numa variavel
            op_code_bin = format(0, '06b').zfill(6) #usando format e 06b, ele le o codigo em decimal...
            rs_bin = format(rs, '05b').zfill(5) #...transforma em representação binaria com os bits que eu desejar
            rt_bin = format(rt, '05b').zfill(5)
            rd_bin = format(rd, '05b').zfill(5) #colocar zfill para garantir que teremos 5/6 bits mesmo que sejam zeros, zfill preenche com zeros a esquerda
            shamt = format(0, '05b').zfill(5)
            funct_bin = format(funct, '06b').zfill(6)
            bits_concatenados = op_code_bin + rs_bin + rt_bin + rd_bin + shamt + funct_bin
            
            hex_num = ""
            for i in range(0, len(bits_concatenados), 4):
                var = bits_concatenados[i: i+4]
                hex_num += hex(int(var, 2))[2:]

            resultado_concatenado = ( "0x" + hex_num)
            print("resultado tipo R:", resultado_concatenado)
            self.resultados_montar.append(resultado_concatenado)
            with open("saida_codes.asm", "a+") as s_codes:
                s_codes.write(resultado_concatenado + '\n')
    
        #montar tipo I
        elif function in self.tipoI_string:
            rs = self.registradores_mips_string[div[1].rstrip(',')]  
            print('RS', rs)
            if '(' in div[2]:
                const, parte = div[2].split('(')
                const = int(const)
                rt = self.registradores_mips_string[parte.rstrip(')')]  
            else:
                const = self.registradores_mips_string[div[2].rstrip(',')]
                rt = None
            funct = self.tipoI_string[function] 
            op_code_bin = format(0, '06b').zfill(6)
            rs_bin = format(rs, '05b').zfill(5)
            rt_bin = format(rt, '05b').zfill(5)
            const_bin = format(const, '016b').zfill(16)
            funct_bin = format(funct, '06b').zfill(6)
            
            #tirei o op_code_bin pq eu ACHO que tava sobrando coisa aqui
            bits_concatenados = funct_bin + rs_bin + rt_bin + const_bin
            hex_num = ""
            for i in range(0, len(bits_concatenados), 4):
                var = bits_concatenados[i: i+4]
                hex_num += hex(int(var, 2))[2:]

            resultado_concatenado = ("0x" + hex_num)
            print("bits concatenados:", bits_concatenados)
            print("resultado concatenado:" , resultado_concatenado)
            self.resultados_montar.append(resultado_concatenado)
            with open("saida_codes.asm", "a+") as s_codes:
                s_codes.write(resultado_concatenado + '\n')

    
        #Montar Tipo J
        elif function in self.tipoJ_string:
            address = int(div[1])
            opcode = self.tipoJ_string[function]
            deslocamento = (self.rotulo_loop[label] - final_address) //4
            
            if deslocamento < 0:
                deslocamento += 2**32

            if label and label.lower() == 'loop':
                label = self.label()
                self.rotulo_loop[label] = final_address
            else:
                pass

            if label not in self.label_loop:
                raise ErrorCode(f"Rótulo {label} não encontrado.")
            address = self.label_loop[label]

            final_address = self.address_inicial + address

            address_bin = format(final_address, '032b')

            address_bin = address_bin[4:30] #tira os bits

            op_code_bin = format(opcode, '06b').zfill(6)
            address_bin = format(address, '026b').zfill(26)

            # Concatenação dos bits
            bits_concatenados = op_code_bin + address_bin
            resultado_concatenado = ( "0x" +
                str(int(bits_concatenados[0:4], 2)) +
                str(int(bits_concatenados[4:8], 2)) +
                str(int(bits_concatenados[8:12], 2)) +
                str(int(bits_concatenados[12:16], 2)) +
                str(int(bits_concatenados[16:20], 2)) +
                str(int(bits_concatenados[20:24], 2)) +
                str(int(bits_concatenados[24:28], 2)) +
                str(int(bits_concatenados[28:32], 2))
            )
            print("bits CONCATENADOS tipo j: ", bits_concatenados)
            print("resultado tipo j montar: ", resultado_concatenado)
            self.resultados_montar.append(resultado_concatenado)
            with open("saida_codes.asm", "a+") as s_codes:
                s_codes.write(resultado_concatenado + '\n')


    def escrever_code(self, entrada_codes, saida_codes):
        print('\n DAQUI PRA BAIXO É CODES:')
        with open(entrada_codes, 'r') as file:
            linhas = file.readlines()
            for linha in linhas:
                self.montar(linha.strip())

        with open(saida_codes, 'w') as saida_file:
            for resultado in self.resultados_montar:
                saida_file.write(resultado + '\n')

    def escrever_hex(self, entrada_hex, saida_hex):
        self.rotulo_loop = {}
        with open(entrada_hex, 'r') as file:
            linha1 = 1
            linhas = file.readlines()
            for linha in linhas:
                self.desmonta(linha.strip(),linha1)
                linha1+=1

        with open(saida_hex, 'w') as saida_file:
            for resultado in self.resultados_desmonta:
                saida_file.write(resultado + '\n')

if __name__ == '__main__':
    entrada_codes = "entrada_codes.asm"
    saida_codes = "saida_codes.asm"
    entrada_hex = "entrada_hex.asm"
    saida_hex = "saida_hex.asm"

    paterson = Paterson()

    paterson.escrever_hex(entrada_hex, saida_hex)
    paterson.escrever_code(entrada_codes, saida_codes)

    #0xAD480000
    #0x12A0FFFE
    #0xAD480000
    #0x02744925
    #0x02744925
    #0x02744925
    #0x08100005
