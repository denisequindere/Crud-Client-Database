import tkinter as tk
from tkinter import ttk
import re
import mysql.connector  



class App(tk.Tk):

    def __init__(self) :
        super().__init__()

        self.title('CRUD - cliente')
        self.iconbitmap("img/python.ico")

        #label de resultado
        self.varResultado = tk.StringVar(self)
        self.lblResultado = ttk.Label(
            self,textvariable=self.varResultado,
            font=("Arial",18),
            background="#DDDDDD"
        )
        self.lblResultado.grid(row=0, column=0, columnspan=3, padx=10, sticky="ewns")


        #label nome
        self.lblNome = ttk.Label(
            self,text="Nome",
            font=("Arial",16,"bold")
        )

        # chamada e posicionamento do label Nome
        self.lblNome.grid(row=1, column=0, sticky="w", padx=20, pady=5)
        # input Nome
        self.varNome = tk.StringVar(self)
        self.txtNome = ttk.Entry(
            self, textvariable=self.varNome,
            font=("Arial", 16)
        )
        self.txtNome.grid(row=1, column=1, sticky="we", padx=20, pady=5)
        self.txtNome.focus()

        # label E-mail
        self.lblEmail = ttk.Label(
            self, text="E-mail",
            font=("Arial", 16, "bold")
        )
        # chamada e posicionamento do label E-mail
        self.lblEmail.grid(row=2, column=0, sticky="w", padx=20, pady=5)
        # input Nome
        self.varEmail = tk.StringVar(self)
        self.txtEmail = ttk.Entry(
            self, textvariable=self.varEmail,
            font=("Arial", 16)
        )
        self.txtEmail.grid(row=2, column=1, sticky="we", padx=20, pady=5)


        #buttons
        self.Bnt1 = ttk.Button(
            self,text="Conectar",
            command=self.btnConectar_Click
            )  
        self.Bnt1.grid(row=1,column=2,padx=20,pady=5,sticky="we",)  

        self.Bnt2 = ttk.Button(self,text="Criar tabela",
            command=self.btnCriarTable_Click)  
        self.Bnt2.grid(row=2,column=2,padx=20,pady=5,sticky="we")  

        self.Bnt3 = ttk.Button(self,text="CREATE",
            command=self.btnInserir_Click)  
        self.Bnt3.grid(row=3,column=2,padx=20,pady=5,sticky="we") 

        self.Bnt4 = ttk.Button(self,text="READ")
        #,command=self.btnLeitura_Click  
        self.Bnt4.grid(row=4,column=2,padx=20,pady=5,sticky="we") 

        self.Bnt5 = ttk.Button(self,text="UPDATE")
            #,command=self.btnAtualiza_Click  
        self.Bnt5.grid(row=5,column=2,padx=20,pady=5,sticky="we") 

        self.Bnt6 = ttk.Button(self,text="DELETE")
            #,command=self.btnDeleta_Click  
        self.Bnt6.grid(row=6,column=2,padx=20,pady=5,sticky="we")  


# Lista resultados
        # chamada e posicionamento da lista de clientes
        self.frameLista = ttk.Frame(self)
        self.frameLista.grid(row=3, column=0, columnspan=2, rowspan=4, sticky="nwes", padx=20, pady=10)

        self.txtLista = ttk.Treeview(
            self.frameLista, columns=('nome','email'),
            show="headings", height=7
        )
        self.txtLista.heading('nome', text='Nome')
        self.txtLista.heading('email', text='Email')

        def item_selected(event):
            for selected_item in self.txtLista.selection():
                item = self.txtLista.item(selected_item)
                record = item['values']
                self.varNome.set(record[0])
                self.varEmail.set(record[1])
            
            self.txtLista.bind('<<TreeviewSelect>>', item_selected)

            self.txtLista.grid(row=0, column=0, sticky="nwes")

            scrollbar = ttk.Scrollbar(
                self.frameLista, orient=tk.VERTICAL, 
                command=self.txtLista.yview)
            self.txtLista.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')


    def btnConectar_Click(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='Dddlma10@30#')

            cursor = connection.cursor()
            sql = "CREATE DATABASE IF NOT EXISTS Crud_Clientes"
            cursor.execute(sql)
            self.varResultado.set("Connected to MySQL Server" )
            self.lblResultado.configure(background="#3cb371")


        except :
            self.varResultado.set("Not Connected to MySQL Server" )
            self.lblResultado.configure(background="#ff0000")

    def btnCriarTable_Click(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='Dddlma10@30#',
                                                database = 'Crud_Clientes')

            cursor = connection.cursor()
            sql = "CREATE TABLE IF NOT EXISTS clientes (nome VARCHAR(55) NOT NULL,email VARCHAR(55),PRIMARY KEY(email))"
            cursor.execute(sql)
            self.varResultado.set("Table created successfully" )
            self.lblResultado.configure(background="#3cb371")
            

        except :
            self.varResultado.set("Error on create Table")
            self.lblResultado.configure(background="#ff0000")

    def btnInserir_Click(self):

        nome = self.varNome.get().strip()
        email = self.varEmail.get().strip()

        resnome =  re.fullmatch(r"\b[A-Za-z ]+\b", nome)
        resemail = re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)

        if resnome is None:
            self.varResultado.set("Campo nome obrigatório!")
            self.lblResultado.configure(background="#ff0000")
            self.txtNome.focus()


        elif resemail is None:
            self.varResultado.set("Campo email obrigatório!")
            self.lblResultado.configure(background="#ff0000")
            self.txtEmail.focus()
        else:

            try:
                connection = mysql.connector.connect(host='localhost',
                                                    user='root',
                                                    password='Dddlma10@30#',
                                                    database = 'Crud_Clientes')

                cursor = connection.cursor()
                sql = "INSERT INTO clientes(nome,email) VALUES (%s , %s)"
                val = (nome,email)
                cursor.execute(sql,val)
                connection.commit()
                self.varResultado.set("client inserted successfully" )
                self.lblResultado.configure(background="#3cb371")
            

            except :
                self.varResultado.set("Error on insert client")
                self.lblResultado.configure(background="#ff0000")
"""
    def btnLeitura_Click(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='Dddlma10@30#',
                                                database = 'Crud_Clientes')

            cursor = connection.cursor()
            sql = "SELECT * FROM clientes"
            cursor.execute(sql)
            self.varResultado.set("client select successfully" )
            self.lblResultado.configure(background="#3cb371")
           

        except :
            self.varResultado.set("Error on select client")
            self.lblResultado.configure(background="#ff0000")

    def btnAtualiza_Click(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='Dddlma10@30#',
                                                database = 'Crud_Clientes')

            cursor = connection.cursor()
            sql = "UPDATE clientes SET nome = self.varNome, email= self.varEmail"
            cursor.execute(sql)
            self.varResultado.set("client updated successfully" )
            self.lblResultado.configure(background="#3cb371")
           

        except :
            self.varResultado.set("Error on update client")
            self.lblResultado.configure(background="#ff0000")
    
    def btnDeleta_Click(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password='Dddlma10@30#',
                                                database = 'Crud_Clientes')

            cursor = connection.cursor()
            sql = "DELETE FROM clientes"
            cursor.execute(sql)
            self.varResultado.set("client deleted successfully" )
            self.lblResultado.configure(background="#3cb371")
           

        except :
            self.varResultado.set("Error on delete client")
            self.lblResultado.configure(background="#ff0000")

            
"""
#inicialização
if __name__ == "__main__":
    app = App()
    app.mainloop()
    

      
