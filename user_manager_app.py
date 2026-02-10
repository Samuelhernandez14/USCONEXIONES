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

class ModernButton(tk.Button):
    """Botón moderno con efectos hover"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', '#3498db')
        self.hover_bg = self._darken_color(self.default_bg)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def _darken_color(self, color):
        """Oscurecer un color hex"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(max(0, c - 30) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker)
    
    def on_enter(self, e):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.config(bg=self.default_bg)

class UserManagerAppV2:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Sistema de Gestión de Usuarios - OCR Automático")
        self.root.geometry("1400x900")
        self.root.configure(bg='#ecf0f1')
        
        # Configurar estilo
        self.setup_styles()
        
        # Inicializar procesadores
        self.ocr_processor = OCRProcessor()
        self.db_handler = DatabaseHandler()
        self.web_automation = None
        
        # Variables
        self.current_image_path = None
        self.extracted_data = {}
        self.processing = False
        
        self.create_widgets()
        self.log_message("✨ Sistema iniciado correctamente", "SUCCESS")
        
    def setup_styles(self):
        """Configurar estilos ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        self.colors = {
            'primary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#9b59b6',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff'
        }
        
    def create_widgets(self):
        """Crear la interfaz gráfica mejorada"""
        
        # ==================== HEADER ====================
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Logo y título
        title_container = tk.Frame(header_frame, bg=self.colors['dark'])
        title_container.pack(expand=True)
        
        tk.Label(
            title_container, 
            text="🔐", 
            font=('Arial', 32),
            bg=self.colors['dark'],
            fg='white'
        ).pack(side='left', padx=(0, 15))
        
        title_frame = tk.Frame(title_container, bg=self.colors['dark'])
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame, 
            text="Sistema de Gestión de Usuarios", 
            font=('Arial', 20, 'bold'),
            bg=self.colors['dark'],
            fg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame, 
            text="Extracción automática de datos con OCR", 
            font=('Arial', 11),
            bg=self.colors['dark'],
            fg='#95a5a6'
        ).pack(anchor='w')
        
        # ==================== MAIN CONTAINER ====================
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ========== PASO 1: CARGAR IMAGEN ==========
        step1_frame = tk.LabelFrame(
            main_container,
            text="  📷 Paso 1: Cargar Imagen  ",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg=self.colors['dark'],
            padx=20,
            pady=20,
            relief='flat',
            borderwidth=2
        )
        step1_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10), pady=(0, 10))
        
        # Instrucciones
        tk.Label(
            step1_frame,
            text="Selecciona una imagen con los datos del usuario",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 15))
        
        # Botón cargar - más grande y visible
        self.load_btn = ModernButton(
            step1_frame,
            text="📂  SELECCIONAR IMAGEN",
            command=self.load_image,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=15,
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        self.load_btn.pack(pady=10)
        
        # Vista previa de imagen - más grande
        self.image_frame = tk.Frame(step1_frame, bg='#f8f9fa', width=450, height=450, relief='sunken', borderwidth=2)
        self.image_frame.pack(pady=15)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="📄\n\nNo hay imagen cargada\n\nFormatos: PNG, JPG, JPEG",
            bg='#f8f9fa',
            fg='#95a5a6',
            font=('Arial', 11)
        )
        self.image_label.pack(expand=True)
        
        # Nombre del archivo
        self.filename_label = tk.Label(
            step1_frame,
            text="",
            font=('Arial', 9, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        self.filename_label.pack()
        
        # ========== PASO 2: PROCESAR OCR ==========
        step2_frame = tk.LabelFrame(
            main_container,
            text="  🔍 Paso 2: Extraer Datos  ",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg=self.colors['dark'],
            padx=20,
            pady=20,
            relief='flat',
            borderwidth=2
        )
        step2_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0), pady=(0, 10))
        
        # Instrucciones
        tk.Label(
            step2_frame,
            text="El sistema extraerá automáticamente la información",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 15))
        
        # Botón procesar OCR
        self.ocr_btn = ModernButton(
            step2_frame,
            text="🔍  EXTRAER DATOS (OCR)",
            command=self.process_ocr,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=15,
            state='disabled',
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        self.ocr_btn.pack(pady=10)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            step2_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=15)
        
        # Status
        self.status_label = tk.Label(
            step2_frame,
            text="⏳ Esperando imagen...",
            font=('Arial', 10),
            bg='white',
            fg='#95a5a6'
        )
        self.status_label.pack(pady=10)
        
        # Datos extraídos con mejor diseño
        data_container = tk.Frame(step2_frame, bg='white')
        data_container.pack(fill='both', expand=True, pady=(20, 0))
        
        tk.Label(
            data_container,
            text="📋 Datos Extraídos",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 10))
        
        # Canvas para scroll si es necesario
        canvas_frame = tk.Frame(data_container, bg='white')
        canvas_frame.pack(fill='both', expand=True)
        
        fields_frame = tk.Frame(canvas_frame, bg='white')
        fields_frame.pack(fill='both', expand=True)
        
        # Campos de datos con iconos
        fields = [
            ("📇", "Tipo de Documento:", "tipo_doc", "CC, CE, TI, PA..."),
            ("🔢", "Número de Documento:", "num_doc", "1234567890"),
            ("👤", "Nombre Completo:", "nombre", "Juan Pérez García"),
            ("📧", "Email/Usuario:", "email", "juan@empresa.com"),
            ("👔", "Rol/Perfil:", "rol", "Administrador"),
            ("🏢", "Área/Departamento:", "area", "Tecnología")
        ]
        
        self.entry_fields = {}
        
        for idx, (icon, label_text, field_name, placeholder) in enumerate(fields):
            # Container para cada campo
            field_container = tk.Frame(fields_frame, bg='white')
            field_container.pack(fill='x', pady=8)
            
            # Label con icono
            label_frame = tk.Frame(field_container, bg='white')
            label_frame.pack(side='left', anchor='w')
            
            tk.Label(
                label_frame,
                text=icon,
                font=('Arial', 12),
                bg='white'
            ).pack(side='left', padx=(0, 5))
            
            tk.Label(
                label_frame,
                text=label_text,
                font=('Arial', 10),
                bg='white',
                fg=self.colors['dark'],
                width=18,
                anchor='w'
            ).pack(side='left')
            
            # Entry con placeholder
            entry = tk.Entry(
                field_container,
                font=('Arial', 10),
                relief='solid',
                borderwidth=1,
                bg='#f8f9fa'
            )
            entry.pack(side='right', fill='x', expand=True)
            entry.insert(0, placeholder)
            entry.config(fg='#95a5a6')
            
            # Placeholder effects
            def on_focus_in(e, entry=entry, placeholder=placeholder):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['dark'])
            
            def on_focus_out(e, entry=entry, placeholder=placeholder):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg='#95a5a6')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
            
            self.entry_fields[field_name] = entry
        
        # ========== PASO 3: ACCIONES ==========
        step3_frame = tk.LabelFrame(
            main_container,
            text="  ⚙️ Paso 3: Ejecutar Acción  ",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg=self.colors['dark'],
            padx=20,
            pady=20,
            relief='flat',
            borderwidth=2
        )
        step3_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(10, 10))
        
        # Container horizontal para acciones
        actions_container = tk.Frame(step3_frame, bg='white')
        actions_container.pack(fill='x', pady=10)
        
        # Selector de acción con radio buttons mejorados
        tk.Label(
            actions_container,
            text="Selecciona la acción a realizar:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 10))
        
        self.action_var = tk.StringVar(value="consultar")
        
        radio_container = tk.Frame(actions_container, bg='white')
        radio_container.pack(fill='x')
        
        actions = [
            ("🔎 Consultar en Base de Datos", "consultar", self.colors['info']),
            ("🔄 Cambiar Rol de Usuario", "cambiar_rol", self.colors['warning']),
            ("⛔ Desactivar Usuario", "desactivar", self.colors['danger'])
        ]
        
        for text, value, color in actions:
            rb_frame = tk.Frame(radio_container, bg='white')
            rb_frame.pack(side='left', padx=10)
            
            rb = tk.Radiobutton(
                rb_frame,
                text=text,
                variable=self.action_var,
                value=value,
                font=('Arial', 10),
                bg='white',
                fg=self.colors['dark'],
                selectcolor=color,
                cursor='hand2',
                activebackground='white'
            )
            rb.pack()
        
        # Botones de acción
        btn_container = tk.Frame(step3_frame, bg='white')
        btn_container.pack(pady=20)
        
        self.consult_btn = ModernButton(
            btn_container,
            text="🔎  CONSULTAR EN BD",
            command=self.consult_database,
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=25,
            pady=12,
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        self.consult_btn.pack(side='left', padx=10)
        
        self.execute_btn = ModernButton(
            btn_container,
            text="▶️  EJECUTAR ACCIÓN WEB",
            command=self.execute_action,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=25,
            pady=12,
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        self.execute_btn.pack(side='left', padx=10)
        
        # ========== LOG PANEL ==========
        log_frame = tk.LabelFrame(
            main_container,
            text="  📝 Registro de Actividad  ",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg=self.colors['dark'],
            padx=15,
            pady=15,
            relief='flat',
            borderwidth=2
        )
        log_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=(10, 0))
        
        # Log con mejor formato
        log_container = tk.Frame(log_frame, bg='white')
        log_container.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_container,
            height=10,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='white',
            relief='flat',
            padx=10,
            pady=10
        )
        self.log_text.pack(fill='both', expand=True)
        
        # Configurar tags de colores para el log
        self.log_text.tag_config("ERROR", foreground="#ff4444")
        self.log_text.tag_config("SUCCESS", foreground="#00ff00")
        self.log_text.tag_config("WARNING", foreground="#ffaa00")
        self.log_text.tag_config("INFO", foreground="#00aaff")
        
        # Configurar grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=2)
        main_container.rowconfigure(1, weight=1)
        main_container.rowconfigure(2, weight=1)
        
    def load_image(self):
        """Cargar imagen desde archivo"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen con datos del usuario",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.ocr_btn.config(state='normal')
            self.filename_label.config(text=f"📄 {os.path.basename(file_path)}")
            self.status_label.config(text="✅ Imagen cargada - Lista para procesar")
            self.log_message(f"Imagen cargada: {os.path.basename(file_path)}", "SUCCESS")
    
    def display_image(self, image_path):
        """Mostrar imagen en la interfaz"""
        try:
            image = Image.open(image_path)
            # Redimensionar manteniendo aspecto
            image.thumbnail((430, 430), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo
            
        except Exception as e:
            self.log_message(f"Error al cargar imagen: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
    
    def process_ocr(self):
        """Procesar OCR de la imagen"""
        if not self.current_image_path:
            messagebox.showwarning("⚠️ Advertencia", "No hay imagen cargada")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.status_label.config(text="⏳ Procesando OCR...")
        self.ocr_btn.config(state='disabled', text="⏳ PROCESANDO...")
        self.progress.start(10)
        self.log_message("Iniciando extracción de datos con OCR...", "INFO")
        
        def ocr_thread():
            try:
                # Procesar OCR
                extracted_data = self.ocr_processor.extract_user_data(self.current_image_path)
                
                # Actualizar UI en thread principal
                self.root.after(0, lambda: self.update_extracted_data(extracted_data))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Error en OCR: {str(e)}", "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("❌ Error OCR", f"Error al procesar la imagen:\n\n{str(e)}"))
            finally:
                self.root.after(0, self.finish_ocr_processing)
        
        threading.Thread(target=ocr_thread, daemon=True).start()
    
    def finish_ocr_processing(self):
        """Finalizar procesamiento OCR"""
        self.processing = False
        self.progress.stop()
        self.ocr_btn.config(state='normal', text="🔍  EXTRAER DATOS (OCR)")
    
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
        
        # Llenar campos
        for data_key, field_key in field_mapping.items():
            if data_key in data and field_key in self.entry_fields:
                entry = self.entry_fields[field_key]
                # Limpiar placeholder
                if entry.cget('fg') == '#95a5a6':
                    entry.delete(0, tk.END)
                    entry.config(fg=self.colors['dark'])
                else:
                    entry.delete(0, tk.END)
                # Insertar dato
                entry.insert(0, data[data_key])
        
        self.status_label.config(text="✅ Datos extraídos correctamente")
        self.log_message("Datos extraídos exitosamente. Revisa y edita si es necesario.", "SUCCESS")
        messagebox.showinfo(
            "✅ Extracción Completada",
            "Los datos han sido extraídos de la imagen.\n\n"
            "Por favor revisa los campos y edita si es necesario\n"
            "antes de ejecutar una acción."
        )
    
    def get_entry_value(self, field_key):
        """Obtener valor real de un entry (ignorando placeholders)"""
        entry = self.entry_fields[field_key]
        value = entry.get().strip()
        # Si el color es gris, es placeholder
        if entry.cget('fg') == '#95a5a6':
            return ''
        return value
    
    def consult_database(self):
        """Consultar usuario en base de datos"""
        num_doc = self.get_entry_value('num_doc')
        
        if not num_doc:
            messagebox.showwarning("⚠️ Advertencia", "Ingresa un número de documento")
            return
        
        self.log_message(f"Consultando usuario con documento: {num_doc}", "INFO")
        
        try:
            user_data = self.db_handler.get_user_by_document(num_doc)
            
            if user_data:
                self.log_message(f"Usuario encontrado: {user_data.get('nombre_completo', 'N/A')}", "SUCCESS")
                self.show_user_info(user_data)
            else:
                self.log_message(f"Usuario no encontrado en BD", "WARNING")
                messagebox.showinfo(
                    "👤 No encontrado",
                    f"El usuario con documento {num_doc}\nno existe en la base de datos"
                )
                
        except Exception as e:
            self.log_message(f"Error en consulta: {str(e)}", "ERROR")
            messagebox.showerror("❌ Error", f"Error al consultar BD:\n\n{str(e)}")
    
    def show_user_info(self, user_data):
        """Mostrar información del usuario en ventana emergente moderna"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Información del Usuario")
        info_window.geometry("500x400")
        info_window.configure(bg='white')
        info_window.resizable(False, False)
        
        # Header
        header = tk.Frame(info_window, bg=self.colors['info'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="👤 Información del Usuario",
            font=('Arial', 16, 'bold'),
            bg=self.colors['info'],
            fg='white'
        ).pack(pady=15)
        
        # Content
        content = tk.Frame(info_window, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Mostrar datos
        display_fields = [
            ('ID', 'id'),
            ('Tipo de Documento', 'tipo_documento'),
            ('Número de Documento', 'numero_documento'),
            ('Nombre Completo', 'nombre_completo'),
            ('Email', 'email'),
            ('Rol', 'rol'),
            ('Área', 'area'),
            ('Estado', 'estado'),
            ('Fecha Creación', 'fecha_creacion')
        ]
        
        for label, key in display_fields:
            if key in user_data:
                row = tk.Frame(content, bg='white')
                row.pack(fill='x', pady=5)
                
                tk.Label(
                    row,
                    text=f"{label}:",
                    font=('Arial', 10, 'bold'),
                    bg='white',
                    width=20,
                    anchor='w'
                ).pack(side='left')
                
                value = str(user_data[key])
                fg_color = self.colors['success'] if key == 'estado' and value == 'activo' else self.colors['dark']
                
                tk.Label(
                    row,
                    text=value,
                    font=('Arial', 10),
                    bg='white',
                    fg=fg_color,
                    anchor='w'
                ).pack(side='left', fill='x', expand=True)
        
        # Botón cerrar
        ModernButton(
            content,
            text="Cerrar",
            command=info_window.destroy,
            bg=self.colors['info'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        ).pack(pady=(20, 0))
    
    def execute_action(self):
        """Ejecutar acción seleccionada"""
        action = self.action_var.get()
        
        # Obtener datos de los campos
        user_data = {
            'tipo_doc': self.get_entry_value('tipo_doc'),
            'num_doc': self.get_entry_value('num_doc'),
            'nombre': self.get_entry_value('nombre'),
            'email': self.get_entry_value('email'),
            'rol': self.get_entry_value('rol'),
            'area': self.get_entry_value('area')
        }
        
        # Validar datos mínimos
        if not user_data['num_doc']:
            messagebox.showwarning("⚠️ Advertencia", "El número de documento es obligatorio")
            return
        
        if action == 'cambiar_rol' and not user_data['rol']:
            messagebox.showwarning("⚠️ Advertencia", "Debes especificar el nuevo rol")
            return
        
        # Confirmar acción
        action_names = {
            'cambiar_rol': 'Cambiar Rol de Usuario',
            'desactivar': 'Desactivar Usuario',
            'consultar': 'Consultar en BD'
        }
        
        action_messages = {
            'cambiar_rol': f"¿Cambiar el rol del usuario {user_data['num_doc']}\na '{user_data['rol']}'?",
            'desactivar': f"¿Desactivar el usuario {user_data['num_doc']}?\n\n⚠️ Esta acción puede ser reversible dependiendo\nde la configuración de la plataforma.",
            'consultar': f"Consultar usuario {user_data['num_doc']} en la base de datos"
        }
        
        if action != 'consultar':
            if not messagebox.askyesno(
                "⚠️ Confirmar Acción",
                action_messages.get(action, "¿Ejecutar esta acción?")
            ):
                return
        
        self.execute_btn.config(state='disabled', text="⏳ EJECUTANDO...")
        self.log_message(f"Ejecutando: {action_names[action]}", "INFO")
        
        def action_thread():
            try:
                if action == 'consultar':
                    self.root.after(0, self.consult_database)
                    return
                
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
                    self.root.after(0, lambda: self.log_message(result['message'], "SUCCESS"))
                    self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", result['message']))
                else:
                    self.root.after(0, lambda: self.log_message(result['message'], "ERROR"))
                    self.root.after(0, lambda: messagebox.showerror("❌ Error", result['message']))
                    
            except Exception as e:
                error_msg = f"Error al ejecutar acción: {str(e)}"
                self.root.after(0, lambda: self.log_message(error_msg, "ERROR"))
                self.root.after(0, lambda: messagebox.showerror("❌ Error", error_msg))
            finally:
                self.root.after(0, lambda: self.execute_btn.config(state='normal', text="▶️  EJECUTAR ACCIÓN WEB"))
        
        threading.Thread(target=action_thread, daemon=True).start()
    
    def log_message(self, message, level="INFO"):
        """Agregar mensaje al log con colores"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Iconos según nivel
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }
        
        icon = icons.get(level, "ℹ️")
        log_entry = f"[{timestamp}] {icon} {message}\n"
        
        self.log_text.insert(tk.END, log_entry, level)
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = UserManagerAppV2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
