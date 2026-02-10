"""
Aplicación de Gestión de Usuarios con OCR
Automatiza la creación, modificación de roles y desactivación de usuarios
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
from datetime import datetime
import os

# Importar módulos personalizados
from ocr_processor import OCRProcessor
from database_handler import DatabaseHandler
from web_automation import WebAutomation

class UserManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Usuarios - OCR")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar procesadores
        self.ocr_processor = OCRProcessor()
        self.db_handler = DatabaseHandler()
        self.web_automation = None
        
        # Variables
        self.current_image_path = None
        self.extracted_data = {}
        
        self.create_widgets()
        self.log_message("Sistema iniciado correctamente")
        
    def create_widgets(self):
        """Crear la interfaz gráfica"""
        
        # ==================== HEADER ====================
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🔐 Sistema de Gestión de Usuarios", 
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # ==================== MAIN CONTAINER ====================
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== LEFT PANEL - Imagen y Carga ==========
        left_panel = tk.LabelFrame(
            main_container, 
            text="📁 Cargar Imagen",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Botón cargar imagen
        self.load_btn = tk.Button(
            left_panel,
            text="📂 Seleccionar Imagen",
            command=self.load_image,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.load_btn.pack(pady=10)
        
        # Vista previa de imagen
        self.image_frame = tk.Frame(left_panel, bg='#ecf0f1', width=400, height=400)
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="No hay imagen cargada",
            bg='#ecf0f1',
            fg='#7f8c8d',
            font=('Arial', 10)
        )
        self.image_label.pack(expand=True)
        
        # Botón procesar OCR
        self.ocr_btn = tk.Button(
            left_panel,
            text="🔍 Extraer Datos (OCR)",
            command=self.process_ocr,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            state='disabled',
            cursor='hand2'
        )
        self.ocr_btn.pack(pady=10)
        
        # ========== RIGHT PANEL - Datos y Acciones ==========
        right_panel = tk.Frame(main_container, bg='#f0f0f0')
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        # Panel de datos extraídos
        data_frame = tk.LabelFrame(
            right_panel,
            text="📋 Datos Extraídos",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=15,
            pady=15
        )
        data_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Campos de datos
        fields = [
            ("Tipo de Documento:", "tipo_doc"),
            ("Número de Documento:", "num_doc"),
            ("Nombre Completo:", "nombre"),
            ("Email/Usuario:", "email"),
            ("Rol/Perfil:", "rol"),
            ("Área/Departamento:", "area")
        ]
        
        self.entry_fields = {}
        
        for idx, (label_text, field_name) in enumerate(fields):
            label = tk.Label(
                data_frame,
                text=label_text,
                font=('Arial', 10),
                bg='white',
                anchor='w'
            )
            label.grid(row=idx, column=0, sticky='w', pady=5, padx=(0, 10))
            
            entry = tk.Entry(
                data_frame,
                font=('Arial', 10),
                width=40,
                relief='solid',
                borderwidth=1
            )
            entry.grid(row=idx, column=1, sticky='ew', pady=5)
            self.entry_fields[field_name] = entry
        
        data_frame.columnconfigure(1, weight=1)
        
        # Panel de acciones
        action_frame = tk.LabelFrame(
            right_panel,
            text="⚙️ Acciones",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=15,
            pady=15
        )
        action_frame.pack(fill='x', pady=(0, 10))
        
        # Selector de acción
        tk.Label(
            action_frame,
            text="Seleccionar acción:",
            font=('Arial', 10, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.action_var = tk.StringVar(value="cambiar_rol")
        
        actions = [
            ("Cambiar Rol", "cambiar_rol"),
            ("Desactivar Usuario", "desactivar"),
            ("Consultar en BD", "consultar")
        ]
        
        for text, value in actions:
            rb = tk.Radiobutton(
                action_frame,
                text=text,
                variable=self.action_var,
                value=value,
                font=('Arial', 10),
                bg='white',
                cursor='hand2'
            )
            rb.pack(anchor='w', pady=2)
        
        # Botones de acción
        btn_frame = tk.Frame(action_frame, bg='white')
        btn_frame.pack(fill='x', pady=(15, 0))
        
        self.consult_btn = tk.Button(
            btn_frame,
            text="🔎 Consultar BD",
            command=self.consult_database,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.consult_btn.pack(side='left', padx=(0, 5))
        
        self.execute_btn = tk.Button(
            btn_frame,
            text="▶️ Ejecutar Acción",
            command=self.execute_action,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.execute_btn.pack(side='left')
        
        # ========== LOG PANEL ==========
        log_frame = tk.LabelFrame(
            right_panel,
            text="📝 Registro de Actividad",
            font=('Arial', 12, 'bold'),
            bg='white',
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='white',
            relief='flat'
        )
        self.log_text.pack(fill='both', expand=True)
        
        # Configurar grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=2)
        main_container.rowconfigure(0, weight=1)
        
    def load_image(self):
        """Cargar imagen desde archivo"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.ocr_btn.config(state='normal')
            self.log_message(f"✅ Imagen cargada: {os.path.basename(file_path)}")
    
    def display_image(self, image_path):
        """Mostrar imagen en la interfaz"""
        try:
            image = Image.open(image_path)
            # Redimensionar manteniendo aspecto
            image.thumbnail((380, 380), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # Mantener referencia
            
        except Exception as e:
            self.log_message(f"❌ Error al cargar imagen: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
    
    def process_ocr(self):
        """Procesar OCR de la imagen"""
        if not self.current_image_path:
            messagebox.showwarning("Advertencia", "No hay imagen cargada")
            return
        
        self.log_message("🔄 Procesando OCR...")
        self.ocr_btn.config(state='disabled', text="Procesando...")
        
        def ocr_thread():
            try:
                # Procesar OCR
                extracted_data = self.ocr_processor.extract_user_data(self.current_image_path)
                
                # Actualizar UI en thread principal
                self.root.after(0, lambda: self.update_extracted_data(extracted_data))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Error en OCR: {str(e)}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("Error OCR", str(e)))
            finally:
                self.root.after(0, lambda: self.ocr_btn.config(state='normal', text="🔍 Extraer Datos (OCR)"))
        
        threading.Thread(target=ocr_thread, daemon=True).start()
    
    def update_extracted_data(self, data):
        """Actualizar campos con datos extraídos"""
        self.extracted_data = data
        
        # Mapeo de campos
        field_mapping = {
            'tipo_documento': 'tipo_doc',
            'numero_documento': 'num_doc',
            'nombre_completo': 'nombre',
            'email': 'email',
            'rol': 'rol',
            'area': 'area'
        }
        
        # Limpiar campos
        for entry in self.entry_fields.values():
            entry.delete(0, tk.END)
        
        # Llenar campos
        for data_key, field_key in field_mapping.items():
            if data_key in data and field_key in self.entry_fields:
                self.entry_fields[field_key].insert(0, data[data_key])
        
        self.log_message("✅ Datos extraídos correctamente")
        messagebox.showinfo("Éxito", "Datos extraídos. Revisa y edita si es necesario.")
    
    def consult_database(self):
        """Consultar usuario en base de datos"""
        num_doc = self.entry_fields['num_doc'].get().strip()
        
        if not num_doc:
            messagebox.showwarning("Advertencia", "Ingresa un número de documento")
            return
        
        self.log_message(f"🔎 Consultando usuario con documento: {num_doc}")
        
        try:
            user_data = self.db_handler.get_user_by_document(num_doc)
            
            if user_data:
                self.log_message(f"✅ Usuario encontrado: {user_data.get('nombre', 'N/A')}")
                # Mostrar datos en ventana emergente
                self.show_user_info(user_data)
            else:
                self.log_message(f"⚠️ Usuario no encontrado en BD")
                messagebox.showinfo("No encontrado", "Usuario no existe en la base de datos")
                
        except Exception as e:
            self.log_message(f"❌ Error en consulta: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Error al consultar BD: {str(e)}")
    
    def show_user_info(self, user_data):
        """Mostrar información del usuario en ventana emergente"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Información del Usuario")
        info_window.geometry("400x300")
        info_window.configure(bg='white')
        
        tk.Label(
            info_window,
            text="👤 Información del Usuario",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        info_frame = tk.Frame(info_window, bg='white')
        info_frame.pack(fill='both', expand=True, padx=20)
        
        for key, value in user_data.items():
            row = tk.Frame(info_frame, bg='white')
            row.pack(fill='x', pady=3)
            
            tk.Label(
                row,
                text=f"{key.replace('_', ' ').title()}:",
                font=('Arial', 10, 'bold'),
                bg='white',
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row,
                text=str(value),
                font=('Arial', 10),
                bg='white',
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
    
    def execute_action(self):
        """Ejecutar acción seleccionada"""
        action = self.action_var.get()
        
        # Obtener datos de los campos
        user_data = {
            'tipo_doc': self.entry_fields['tipo_doc'].get().strip(),
            'num_doc': self.entry_fields['num_doc'].get().strip(),
            'nombre': self.entry_fields['nombre'].get().strip(),
            'email': self.entry_fields['email'].get().strip(),
            'rol': self.entry_fields['rol'].get().strip(),
            'area': self.entry_fields['area'].get().strip()
        }
        
        # Validar datos mínimos
        if not user_data['num_doc']:
            messagebox.showwarning("Advertencia", "El número de documento es obligatorio")
            return
        
        # Confirmar acción
        action_names = {
            'cambiar_rol': 'Cambiar Rol',
            'desactivar': 'Desactivar Usuario',
            'consultar': 'Consultar en BD'
        }
        
        if not messagebox.askyesno(
            "Confirmar",
            f"¿Ejecutar acción: {action_names[action]}?"
        ):
            return
        
        self.execute_btn.config(state='disabled', text="Ejecutando...")
        self.log_message(f"▶️ Ejecutando: {action_names[action]}")
        
        def action_thread():
            try:
                if self.web_automation is None:
                    self.web_automation = WebAutomation()
                
                if action == 'cambiar_rol':
                    result = self.web_automation.change_user_role(
                        user_data['num_doc'],
                        user_data['rol']
                    )
                elif action == 'desactivar':
                    result = self.web_automation.deactivate_user(user_data['num_doc'])
                else:
                    result = {'success': False, 'message': 'Acción no implementada'}
                
                # Actualizar UI
                if result['success']:
                    self.root.after(0, lambda: self.log_message(f"✅ {result['message']}"))
                    self.root.after(0, lambda: messagebox.showinfo("Éxito", result['message']))
                else:
                    self.root.after(0, lambda: self.log_message(f"❌ {result['message']}", "ERROR"))
                    self.root.after(0, lambda: messagebox.showerror("Error", result['message']))
                    
            except Exception as e:
                error_msg = f"Error al ejecutar acción: {str(e)}"
                self.root.after(0, lambda: self.log_message(f"❌ {error_msg}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            finally:
                self.root.after(0, lambda: self.execute_btn.config(state='normal', text="▶️ Ejecutar Acción"))
        
        threading.Thread(target=action_thread, daemon=True).start()
    
    def log_message(self, message, level="INFO"):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Color según nivel
        if level == "ERROR":
            # Última línea en rojo
            start_idx = self.log_text.index("end-2l")
            end_idx = self.log_text.index("end-1l")
            self.log_text.tag_add("error", start_idx, end_idx)
            self.log_text.tag_config("error", foreground="#ff4444")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagerApp(root)
    root.mainloop()
