import tkinter as tk

class CheckBoxList:
    """
        Clase que representa el elemento gráfico CheckBoxList, que representa
        una ventana en la que se muestra una lista de opciones, permite 
        seleccionar múltiples opciones y en caso de que se haga click en el 
        botón de aceptar se retornará la lista de las opciones elegidas
    """
    def __init__(self, items: list[str]) -> None:
        # Gestión de los elementos de la lista
        self.items = items
        self.selected_items = []

        # Creacción del root
        self.root = tk.Tk()
        self.root.title("Lista de categorías")
        self.root.configure(bg="white")

        # Creamos los elementos de la interfaz gráfica
        self.frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.frame)
        self.listbox = tk.Listbox(self.frame, selectmode='multiple', 
        yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.button_accept = tk.Button(self.root, text="Aceptar", 
        command=self.accept_selection)
        self.button_clear = tk.Button(self.root, text="Limpiar",
        command=self.clear_selection)
        
        # Insertamos los elementos a la lista
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Añadir los elementos a la ventana
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill='both', expand=1)
        self.frame.pack(fill='both', expand=1)
        self.button_accept.pack()
        self.button_clear.pack()
    
    def run(self) -> list[str]:
        """
            Ejecuta la ventana, y no termina hasta que esta no sea cerrada.
        Returns:
            list[str]: elementos de la lista que se han elegido
        """
        self.root.mainloop()
        return self.selected_items
    
    def accept_selection(self):
        """
            Acción realizada cuando se pulsa el botón de aceptar, almacena los 
            elementos seleccionados dentro del objeto ventana
        """
        self.selected_items = [self.listbox.get(idx) for idx in 
                               self.listbox.curselection()]
        self.root.destroy()

    def clear_selection(self):
        """
            Limpia la ventana para poder elegir nuevos elementos diferentes
        """
        self.listbox.selection_clear(0, tk.END)