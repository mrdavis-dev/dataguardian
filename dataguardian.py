import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading
import os
import time
import schedule

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Backup App")

        # Configurar el estilo del título
        title_style = ttk.Style()
        title_style.configure("Title.TLabel", font=("Segoe UI", 18), padding=(10, 10))
        
        # Título
        self.title_label = ttk.Label(root, text="Database Backup", style="Title.TLabel")
        self.title_label.pack()

        # Configurar el estilo del botón
        button_style = ttk.Style()
        button_style.configure(
            "Blue.TButton",
            font=("Segoe UI", 12),
            padding=(10, 10),
            width=15,
            height=2,
            background="#45b592",
            foreground="#000000",
            borderwidth=0
        )
        
        # Botón de backup manual
        ttk.Button(
            root,
            text="Realizar Backup Manual",
            style="Blue.TButton",
            command=self.manual_backup
        ).pack(pady=20)  # Agregamos espacio entre el título y el botón

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack(pady=20)  # Agregamos espacio entre el botón y la barra de progreso

        self.backup_table = ttk.Treeview(root, columns=("Date", "Location"))
        self.backup_table.heading("#0", text="Fecha")
        self.backup_table.heading("#1", text="Ubicación")
        self.backup_table.pack()

        # Iniciar el proceso de programación de respaldos automáticos en segundo plano
        self.start_schedule_thread()

        # Cargar los respaldos guardados en la tabla
        self.load_backups()

    def manual_backup(self):
        try:
            # Nombre de la base de datos y contraseña
            database_name = "clisys"
            password = "37395"

            # Ruta y nombre del archivo de respaldo
            file_path = f"D:/py_projects/dataguardian/autodataguardian/auto_backups/autorespaldo_{time.strftime('%Y%m%d%H%M%S')}.sql"

            # Crear un hilo para realizar el respaldo
            backup_thread = threading.Thread(target=self.backup_database, args=(database_name, password, file_path))
            backup_thread.start()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def backup_database(self, database_name, password, file_path):
        try:
            # Comando para realizar el respaldo
            command = f"mysqldump -u root -p{password} --databases {database_name} > {file_path}"

            # Ejecutar el comando
            subprocess.call(command, shell=True)

            # Actualizar la barra de progreso en el hilo principal
            self.root.after(1000, self.update_progress_bar, 100)

            # Registrar la fecha y la ubicación del backup en la tabla
            backup_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.backup_table.insert("", "end", values=(backup_date, file_path))

            messagebox.showinfo("Backup Manual", f"Respaldo manual realizado con éxito. Archivo: {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_progress_bar(self, value):
        self.progress_bar["value"] = value

    def start_schedule_thread(self):
        def worker():
            print("Programación de trabajos programados...")
            # Programar el respaldo automático cada 15 segundos
            schedule.every(15).seconds.do(self.auto_backup)
            while True:
                schedule.run_pending()
                time.sleep(1)
                print("Verificando trabajos programados...")

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    def auto_backup(self):
        try:
            # Nombre de la base de datos y contraseña
            database_name = "clisys"
            password = "37395"

            # Ruta y nombre del archivo de respaldo
            file_path = f"D:/py_projects/dataguardian/autodataguardian/auto_backups/autorespaldo_{time.strftime('%Y%m%d%H%M%S')}.sql"

            # Comando para realizar el respaldo
            command = f"mysqldump -u root -p{password} --databases {database_name} > {file_path}"

            # Ejecutar el comando
            subprocess.call(command, shell=True)

            # Actualizar la barra de progreso en el hilo principal
            self.root.after(1000, self.update_progress_bar, 100)

            # Registrar la fecha y la ubicación del backup en la tabla
            backup_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.backup_table.insert("", "end", values=(backup_date, file_path))

            print(f"Respaldo automático realizado con éxito. Archivo: {file_path}")

        except Exception as e:
            print(f"Error en el respaldo automático: {str(e)}")

    def load_backups(self):
        # Directorio donde se almacenan los respaldos automáticos
        backup_dir = "D:/py_projects/dataguardian/autodataguardian/auto_backups/"

        # Listar los archivos de respaldo en el directorio
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".sql")]

        # Recorrer la lista de archivos y cargarlos en la tabla
        for backup_file in backup_files:
            backup_path = os.path.join(backup_dir, backup_file)
            backup_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(backup_path)))
            self.backup_table.insert("", "end", values=(backup_date, backup_path))

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
