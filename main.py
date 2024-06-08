from tkinter import *  # Importa todas as classes e funções da biblioteca tkinter
from tkinter import ttk  # Importa o módulo ttk para widgets temáticos
from tkinter import messagebox  # Importa o módulo messagebox para exibir caixas de diálogo
import sqlite3  # Importa a biblioteca sqlite3 para interagir com o banco de dados

# Inicializa a janela principal do Tkinter
root = Tk()

# Define uma classe Funcs para agrupar as funções relacionadas à aplicação
class Funcs():
    # Define a função limpar_tela para limpar os campos de entrada
    def limpar_tela(self):
        # Limpa o conteúdo dos campos de entrada
        self.codigo_entry.delete(0, END)
        self.Nome_entry.delete(0, END)
        self.tel_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.embarc_entry.delete(0, END)
        self.pesca_entry.delete(0, END)
        self.local_entry.delete(0, END)

    # Define a função conectar_bd para conectar ao banco de dados
    def conectar_bd(self):
        # Estabelece uma conexão com o banco de dados SQLite "clientes.bd"
        self.conn = sqlite3.connect("clientes.bd")
        # Cria um cursor para executar comandos SQL
        self.cursor = self.conn.cursor(); 
        print('Conectando ao Banco de Dados')

    # Define a função desconecta_bd para desconectar do banco de dados
    def desconecta_bd(self):
        # Fecha a conexão com o banco de dados
        self.conn.close(); 
        print('Desconectando do Banco de Dados')

    # Define a função montaTabelas para criar a tabela "clientes" no banco de dados
    def montaTabelas(self):
        # Conecta ao banco de dados
        self.conectar_bd()
        # Cria a tabela "clientes" se ela não existir
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes(
                            cod INTEGER PRIMARY KEY,
                            nome_cliente CHAR(40) NOT NULL,
                            telefone INTEGER(20),
                            cpf CHAR(40),
                            embarcação CHAR(40),
                            tipo_pesca CHAR(40),
                            local_pesca CHAR(40)
                        );
                    """)
        # Confirma as alterações no banco de dados
        self.conn.commit(); 
        print("Banco de Dados criado")
        # Desconecta do banco de dados
        self.desconecta_bd()

    # Define a função variaveis para obter os valores dos campos de entrada
    def variaveis(self):
        # Obtém os valores dos campos de entrada
        self.codigo = self.codigo_entry.get()
        self.Nome = self.Nome_entry.get()
        self.telefone =  self.tel_entry.get()
        self.cpf = self.cpf_entry.get()
        self.embarc = self.embarc_entry.get()
        self.pesca = self.pesca_entry.get()
        self.local = self.local_entry.get()

    # Define a função add_cliente para adicionar um novo cliente ao banco de dados
    def add_cliente(self):
        # Obtém os valores dos campos de entrada
        self.variaveis()
        # Conecta ao banco de dados
        self.conectar_bd()

        # Executa a consulta SQL para inserir um novo cliente na tabela "clientes"
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cpf, embarcação, tipo_pesca, local_pesca)
                            VALUES (?, ?, ?, ?, ?, ?)""", (self.Nome, self.telefone, self.cpf, self.embarc, self.pesca, self.local))
        # Confirma as alterações no banco de dados
        self.conn.commit()
        # Desconecta do banco de dados
        self.desconecta_bd()
        # Atualiza a lista de clientes na tela
        self.select_lista()
        # Limpa os campos de entrada
        self.limpar_tela()

    # Define a função select_lista para exibir a lista de clientes na tela
    def select_lista(self):
        # Limpa a lista de clientes na tela
        self.lista_inputs.delete(*self.lista_inputs.get_children())
        # Conecta ao banco de dados
        self.conectar_bd()
        # Executa a consulta SQL para selecionar todos os clientes ordenados por nome
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cpf, embarcação, tipo_pesca, local_pesca FROM clientes
                                    ORDER BY nome_cliente ASC; """)
        # Insere cada cliente na lista de clientes na tela
        for i in lista:
            self.lista_inputs.insert("", END, values=i)
        # Desconecta do banco de dados
        self.desconecta_bd()

    # Define a função doubleClick para preencher os campos de entrada com os dados de um cliente selecionado
    def doubleClick(self, event):
        # Limpa os campos de entrada
        self.limpar_tela()
        # Seleciona o cliente na lista
        self.lista_inputs.selection()

        # Percorre cada cliente selecionado
        for n in self.lista_inputs.selection():
            # Obtém os valores dos campos do cliente selecionado
            col1, col2, col3, col4, col5, col6, col7 = self.lista_inputs.item(n, 'values')
            # Preenche os campos de entrada com os valores do cliente
            self.codigo_entry.insert(END, col1)
            self.Nome_entry.insert(END, col2)
            self.tel_entry.insert(END, col3)
            self.cpf_entry.insert(END, col4)
            self.embarc_entry.insert(END, col5)
            self.pesca_entry.insert(END, col6)
            self.local_entry.insert(END, col7)

    # Define a função deleta_cliente para excluir um cliente do banco de dados
    def deleta_cliente(self):
        # Obtém os valores dos campos de entrada
        self.variaveis()
        # Conecta ao banco de dados
        self.conectar_bd()
        try:
            # Executa a consulta SQL para excluir o cliente com o código selecionado
            self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
            # Confirma as alterações no banco de dados
            self.conn.commit()
            # Desconecta do banco de dados
            self.desconecta_bd()
            # Limpa os campos de entrada
            self.limpar_tela()
            # Atualiza a lista de clientes na tela
            self.select_lista()
            # Exibe uma mensagem de sucesso
            messagebox.showinfo('Sucesso', 'Cliente deletado com sucesso!')
        except Exception as e:
            # Imprime o erro no console
            print(f"Erro ao deletar cliente: {e}")
            # Exibe uma mensagem de erro na tela
            messagebox.showerror('Erro', 'Erro ao deletar cliente.')

    # Define a função altera_cliente para alterar os dados de um cliente no banco de dados
    def altera_cliente(self):
        # Obtém os valores dos campos de entrada
        self.variaveis()
        # Conecta ao banco de dados
        self.conectar_bd()
        try:
            # Executa a consulta SQL para atualizar os dados do cliente com o código selecionado
            self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cpf = ?, embarcação = ?, tipo_pesca = ?, local_pesca = ? WHERE cod = ?""",
                            (self.Nome, self.telefone, self.cpf, self.embarc, self.pesca, self.local, self.codigo))
            # Confirma as alterações no banco de dados
            self.conn.commit()
            # Desconecta do banco de dados
            self.desconecta_bd()
            # Atualiza a lista de clientes na tela
            self.select_lista()
            # Limpa os campos de entrada
            self.limpar_tela()
            # Exibe uma mensagem de sucesso
            messagebox.showinfo('Sucesso', 'Cliente alterado com sucesso!')
        except Exception as e:
            # Imprime o erro no console
            print(f"Erro ao alterar cliente: {e}")
            # Exibe uma mensagem de erro na tela
            messagebox.showerror('Erro', 'Erro ao alterar cliente.')

    # Define a função busca_cliente para buscar clientes pelo nome
    def busca_cliente(self):
        # Conecta ao banco de dados
        self.conectar_bd()
        # Limpa a lista de clientes na tela
        self.lista_inputs.delete(*self.lista_inputs.get_children())

        # Obtém o nome digitado pelo usuário
        Nome = self.Nome_entry.get()
        # Se o usuário digitou um nome
        if Nome:
            # Executa a consulta SQL para buscar clientes com o nome digitado
            self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cpf, embarcação, tipo_pesca, local_pesca FROM clientes
                                WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % Nome)
            # Obtém os resultados da busca
            buscanomeCli = self.cursor.fetchall()
            # Se encontrar clientes com o nome digitado
            if buscanomeCli:
                # Insere os clientes encontrados na lista na tela
                for i in buscanomeCli:
                    self.lista_inputs.insert("", END, values=i)
            else:
                # Exibe uma mensagem informando que nenhum cliente foi encontrado
                messagebox.showinfo('Aviso', 'Nenhum cliente encontrado com este nome.')
        else:
            # Exibe uma mensagem solicitando que o usuário digite um nome
            messagebox.showinfo('Aviso', 'Por favor, digite um nome para buscar.')

        # Limpa os campos de entrada
        self.limpar_tela()
        # Desconecta do banco de dados
        self.desconecta_bd()


# Define uma classe Application para criar a interface gráfica da aplicação
class Application(Funcs):
    # Inicializa a classe Application
    def __init__(self):
        # Define a janela principal como atributo da classe
        self.root = root
        # Cria a tela da aplicação
        self.tela()
        # Cria os frames da aplicação
        self.frames()
        # Cria os botões do frame 1
        self.botoes_frame1()
        # Cria a lista de clientes no frame 2
        self.lista_frame2()
        # Cria a tabela "clientes" no banco de dados
        self.montaTabelas()
        # Exibe a lista de clientes na tela
        self.select_lista()
        # Inicia o loop principal do Tkinter
        root.mainloop()

    # Define a função tela para configurar a janela principal
    def tela(self):
        # Define o título da janela
        self.root.title("Cadastro de Navegantes")
        # Define a cor de fundo da janela
        self.root.configure(background='#1e3743')
        # Define as dimensões da janela
        self.root.geometry("700x500")
        # Permite redimensionar a janela
        self.root.resizable(True, True)
        # Define o tamanho mínimo da janela
        self.root.minsize(width=500, height=400)

    # Define a função frames para criar os frames da aplicação
    def frames(self):
        # Cria o frame 1 para os campos de entrada
        self.frame_1 = Frame(self.root, bd= 4, bg='#dfe3ee')
        # Posiciona o frame 1 na tela
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight= 0.46)

        # Cria o frame 2 para a lista de clientes
        self.frame_2 = Frame(self.root, bd= 4, bg='#dfe3ee')
        # Posiciona o frame 2 na tela
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight= 0.46)

    # Define a função botoes_frame1 para criar os botões do frame 1
    def botoes_frame1(self):
        # criação do botão limpar 
        self.bt_limpar = Button(self.frame_1, text='Limpar',bd=2, bg='#107db2', fg='white', command= self.limpar_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight= 0.15)
        # criação do botão Buscar
        self.bt_Buscar = Button(self.frame_1, text='Buscar', bg='#107db2', fg='white', command= self.busca_cliente)
        self.bt_Buscar.place(relx=0.33, rely=0.1, relwidth=0.1, relheight= 0.15)
        # criação do botão Novo
        self.bt_Novo = Button(self.frame_1, text='Novo', bg='#107db2', fg='white', command= self.add_cliente)
        self.bt_Novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight= 0.15)

        # criação do botão Alterar 
        self.bt_Alterar = Button(self.frame_1, text='Alterar', bg='#107db2', fg='white',command= self.altera_cliente)
        self.bt_Alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight= 0.15)
        # criação do botão Apagar 
        self.bt_Apagar = Button(self.frame_1, text='Apagar', bg='#107db2', fg='white', command= self.deleta_cliente)
        self.bt_Apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight= 0.15)

        # criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text="Codigo:")
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)
        

        # criação da label e entrada do Nome
        self.lb_Nome = Label(self.frame_1, text="Nome:")
        self.lb_Nome.place(relx=0.05, rely=0.31)

        self.Nome_entry = Entry(self.frame_1)
        self.Nome_entry.place(relx=0.05, rely=0.41, relwidth=0.8)


        # criação da label e entrada do telefone 
        self.lb_telefone = Label(self.frame_1, text="Telefone:")
        self.lb_telefone.place(relx=0.05, rely=0.54)

        self.tel_entry = Entry(self.frame_1)
        self.tel_entry.place(relx=0.05, rely=0.64, relwidth=0.2)

        # criação da label e entrada do cpf 
        self.lb_cpf = Label(self.frame_1, text="CPF:")
        self.lb_cpf.place(relx=0.28, rely=0.54)

        self.cpf_entry = Entry(self.frame_1)
        self.cpf_entry.place(relx=0.28, rely=0.64, relwidth=0.17)

        # criação da label e entrada do Tipo de embarcação
        self.lb_embarc = Label(self.frame_1, text="Tipo de Embarcação:")
        self.lb_embarc.place(relx=0.5, rely=0.54)

        self.embarc_entry = Entry(self.frame_1)
        self.embarc_entry.place(relx=0.5, rely=0.64, relwidth=0.2)

        # criação da label e entrada do tipo de pesca  
        self.lb_pesca = Label(self.frame_1, text="Tipo de Pesca:")
        self.lb_pesca.place(relx=0.05, rely=0.75)

        self.pesca_entry = Entry(self.frame_1)
        self.pesca_entry.place(relx=0.05, rely=0.85, relwidth=0.2)

        # criação da label e entrada local de pesca 
        self.lb_local = Label(self.frame_1, text="Local da Pesca:")
        self.lb_local.place(relx=0.28, rely=0.75)

        self.local_entry = Entry(self.frame_1)
        self.local_entry.place(relx=0.28, rely=0.85, relwidth=0.42)
        
    def lista_frame2(self): # Esta função serve para criar a segunta dela, chamda de lista_frame2
        # Esta função da a ordem de cada título em sua respectiva coluna
        self.lista_inputs = ttk.Treeview(self.frame_2, height= 3, column= ("col1", "col2", "col3","col4","col5","col6","col7"))
        self.lista_inputs.heading("#0", text="")
        self.lista_inputs.heading("#1", text='Código')
        self.lista_inputs.heading("#2", text='Nome')
        self.lista_inputs.heading("#3", text='Telefone')
        self.lista_inputs.heading("#4", text='CPF')
        self.lista_inputs.heading("#5", text='Tipo de Embarcação')
        self.lista_inputs.heading("#6", text='Tipo de pesca')
        self.lista_inputs.heading("#7", text='Local da Pesca')
        # Este da a posição e o tamanho de cada ele mento que fica na parte superior da segunda tela, onde separa as informações or tipos 
        self.lista_inputs.column("#0", width=1) 
        self.lista_inputs.column("#1", width=50) 
        self.lista_inputs.column("#2", width=200)
        self.lista_inputs.column("#3", width=125)  
        self.lista_inputs.column("#4", width=125)
        self.lista_inputs.column("#5", width=125)
        self.lista_inputs.column("#6", width=125)   
        self.lista_inputs.column("#7", width=125) 

        self.lista_inputs.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85) # Esta função ajusta o enquadramento da tela do lista_frame2

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.lista_inputs.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85) # O scrool que fica ao lado da tela do segundo frame 
        self.lista_inputs.bind("<Double-1>", self.doubleClick) # Função para que quando p usuario der os dois cliques os dados subam para o frame 1 
        
Application() # Esta parte no fim do código faz com que o sistema não feche, pois se não tivesse ela ele iniciaria e logo fecharia.