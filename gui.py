from sre_parse import State
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter.font import Font
from csv import reader, DictReader
import yaml
from yaml.loader import SafeLoader
import re
import os

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.channelsloading_enable = False
        # configure window
        self.title("Dallara Alignment Application")
        self.geometry(f"{1100}x{875}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1,2), weight=0)
        self.grid_rowconfigure(3, weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Dallara Alignment", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.start_alignment_event, text="Start Alignment", fg_color='green', hover_color='darkgreen')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.load_config_event, text="Load config")
        self.sidebar_button_3.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.save_config_event, text="Save config")
        self.sidebar_button_4.grid(row=3, column=0, padx=20, pady=10)
        self.real_data = None
        #self.real_data_event()
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))        

        # create tabview
        self.tabcontent = {}

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.plus_tab_creating()

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0, column=7, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.switch1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, text=f"Parallel")
        self.switch1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.switch2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, text=f"Surrogate")
        self.switch2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.switch3 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, text=f"FastPars")
        self.switch3.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="n")
        self.optimtype = customtkinter.CTkOptionMenu(master=self.checkbox_slider_frame, dynamic_resizing=False, values=["NelderMead", "Gradient", "Coordinate"])
        self.optimtype.grid(row=4, column=0, padx=20, pady=(20, 10))

        cpu_label = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="CPU\n\n\n")
        cpu_label.grid(row=5, column=0, padx=20, pady=(20, 10))
        self.cpu_value = tkinter.StringVar(value=1)
        self.cpu = tkinter.Spinbox(master=self.checkbox_slider_frame, from_=1, to=100, textvariable=self.cpu_value, wrap=True, font=Font(family='Helvetica', size=20, weight='bold'), width=3)
        self.cpu.grid(row=5, column=0, padx=20, pady=(20, 10))

        racecar_label = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Racecar⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n\n")
        racecar_label.grid(row=6, column=0, padx=20, pady=(20, 10))
        self.racecar = customtkinter.CTkOptionMenu(master=self.checkbox_slider_frame, dynamic_resizing=False, values=["F218", "P417"])
        self.racecar.grid(row=6, column=0, padx=20, pady=(20, 10))
        track_label = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="Track⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n\n")
        track_label.grid(row=7, column=0, padx=20, pady=(20, 10))
        self.track = customtkinter.CTkOptionMenu(master=self.checkbox_slider_frame, dynamic_resizing=False, values=["Bahrain", "Melbourne", "Daytona"])
        self.track.grid(row=7, column=0, padx=20, pady=(20, 10))
        
        self.real_file = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text="\n\n\nNo selected file")
        self.real_file.grid(row=8, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_2 = customtkinter.CTkButton(master=self.checkbox_slider_frame, command=self.real_data_event, text="Load real data")
        self.sidebar_button_2.grid(row=8, column=0, padx=20, pady=10)

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Mathematical channels")
        self.scrollable_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.math_channels = {}

        self.new_math_name = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Channel name...")
        self.new_math_name.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.new_math_formula = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Channel formula...", width=300)
        self.new_math_formula.grid(row=0, column=1, padx=10, pady=(0, 20))

        self.new_math_button = customtkinter.CTkButton(master=self.scrollable_frame, command=self.new_math_channel_event, text="Add new math.channel")
        self.new_math_button.grid(row=0, column=2, padx=10, pady=(0, 20))

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")       

    def load_config_event(self):
        print("Config file is loading!")
        path = tkinter.filedialog.askopenfilename()
        config = {}
        with open(path, "r") as stream:
            try:
                config = yaml.load(stream, Loader=SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)
        for each in config["mat_outputs"]["laptimer"]:
            self.math_channel_init(each, config["mat_outputs"]["laptimer"][each])

        # Load parameter tabs
        self.tabview.delete("+")
        for each in config["inputs"]:
            self.tabview.add(each)
            self.tabcontent[each] = {}
            self.tab_init(each)
            if config["inputs"][each]["usage"]:
                self.tabcontent[each]["Enable"].select()
            self.tabcontent[each]["Priority"] = config["inputs"][each]["priority"]
            self.tabcontent[each]["Priority_spinbox"].delete(0, 1)
            self.tabcontent[each]["Priority_spinbox"].insert(0, self.tabcontent[each]["Priority"])
            self.tabcontent[each]["Experiment"].set(config["inputs"][each]["experiment"])
            self.tabcontent[each]["Init val"].insert(0, str(config["inputs"][each]["init_val"]))
            self.tabcontent[each]["Step val"].insert(0, str(config["inputs"][each]["init_step"]))
            self.tabcontent[each]["Tol val"].insert(0, str(config["inputs"][each]["tolerance"]))
            dep_str = str(config["inputs"][each]["dependent"])
            if dep_str != "None":
                dep_str = dep_str.replace("'", "")
                self.tabcontent[each]["Dependent"].insert(0, dep_str[1:-1])

            self.tabcontent[each]["Reading"] = config["inputs"][each]["access_r"]
            self.tabcontent[each]["Writing"] = config["inputs"][each]["access_w"]

            # Load metrics
            param_name = each
            self.tabcontent[param_name]["Subtab"].delete("+")
            for every in config["inputs"][each]["affect_on"]:   
                self.tabcontent[param_name]["Subtab"].add(every)
                self.metric_init(every, param_name)
                filter_str = str(config["inputs"][each]["affect_on"][every]["filter"])
                if filter_str != "None":
                    self.tabcontent[param_name]["Metrics"][every]["filter"].insert(0, filter_str)
                self.tabcontent[param_name]["Metrics"][every]["arg"].insert(0, config["inputs"][each]["affect_on"][every]["wrt"])
                self.tabcontent[param_name]["Metrics"][every]["mult"].insert(0, str(config["inputs"][each]["affect_on"][every]["multiplicator"]))
                self.tabcontent[param_name]["Metrics"][every]["cost"].set(config["inputs"][each]["affect_on"][every]["cost"])


            self.tabcontent[param_name]["Subtab"].add("+")
            self.tabcontent[param_name]["Subtab"].tab("+").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tabcontent[param_name]["New metric"] = customtkinter.CTkEntry(self.tabcontent[param_name]["Subtab"].tab("+"), placeholder_text="Channel name...")
            self.tabcontent[param_name]["New metric"].grid(row=0, column=0, padx=20, pady=20, sticky="n")
            new_metric_button = customtkinter.CTkButton(self.tabcontent[param_name]["Subtab"].tab("+"), command=self.new_metric_event, text="Add new metric")
            new_metric_button.grid(row=1, column=0, padx=20, pady=20, sticky="n")

        self.plus_tab_creating()

        if config["config"]["parallel"]:
            self.switch1.select()
        if config["config"]["surrogate"]:
            self.switch2.select()
        if config["config"]["fast_parse"]:
            self.switch3.select()
        self.optimtype.set(config["config"]["optimization"])
        self.cpu.delete(0)
        self.cpu.insert(0, config["config"]["n_cores"])
        self.racecar.set(config["config"]["racecar"])
        self.track.set(config["config"]["track"])
        self.path = config["config"]["reference"]
        self.path = self.path.replace('\\', '/')
        self.real_file.configure(text = "\n\n\n"+self.path.split('/')[-1])
        self.ChannelsLoading()

    def math_channel_init(self, name, formula):
        self.math_channels[name] = {}

        self.math_channels[name]["name_field"] = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Channel name...")
        self.math_channels[name]["name_field"].grid(row=len(self.math_channels)-1, column=0, padx=10, pady=(0, 20))
        self.math_channels[name]["name_field"].insert(0, name)

        self.math_channels[name]["formula_field"] = customtkinter.CTkEntry(master=self.scrollable_frame, placeholder_text="Channel formula...", width=300)
        self.math_channels[name]["formula_field"].grid(row=len(self.math_channels)-1, column=1, padx=10, pady=(0, 20))
        self.math_channels[name]["formula_field"].insert(0, formula)

        self.math_channels[name]["remove button"] = customtkinter.CTkButton(master=self.scrollable_frame, command= lambda: self.remove_channel_event(name, len(self.math_channels)-1), text="Remove channel", fg_color='red', hover_color='darkred')
        self.math_channels[name]["remove button"].grid(row=len(self.math_channels)-1, column=2, padx=10, pady=(0, 20))

        self.math_channels[name]["row"] = len(self.math_channels)-1

        self.new_math_name.grid(row=len(self.math_channels), column=0, padx=10, pady=(0, 20))
        self.new_math_formula.grid(row=len(self.math_channels), column=1, padx=10, pady=(0, 20))
        self.new_math_button.grid(row=len(self.math_channels), column=2, padx=10, pady=(0, 20))        

        self.new_math_name.delete(0, len(name))
        self.new_math_formula.delete(0, len(formula))

    def tab_init(self, tabname):
        enable = customtkinter.CTkSwitch(master=self.tabview.tab(tabname), text=f"Enable")
        enable.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.tabcontent[tabname]["Enable"] = enable
        priority_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Priority\n\n\n")
        priority_label.grid(row=0, column=1, padx=20, pady=(20, 10))
        priority_value = tkinter.StringVar(value=1)
        priority = tkinter.Spinbox(master=self.tabview.tab(tabname), from_=0, to=100, textvariable=priority_value, wrap=True, font=Font(family='Helvetica', size=20, weight='bold'), width=3)
        priority.grid(row=0, column=1, padx=20, pady=(20, 10))
        self.tabcontent[tabname]["Priority"] = priority_value
        self.tabcontent[tabname]["Priority_spinbox"] = priority
        
        experiment_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Experiment⠀⠀⠀⠀⠀⠀⠀⠀\n\n\n")
        experiment_label.grid(row=0, column=2, padx=20, pady=(20, 10))
        experiment = customtkinter.CTkOptionMenu(self.tabview.tab(tabname), dynamic_resizing=False, values=["laptimer", "top_speed", "snail"])
        experiment.grid(row=0, column=2, padx=20, pady=(20, 10))
        self.tabcontent[tabname]["Experiment"] = experiment
        dependent_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Dependent⠀⠀⠀⠀⠀⠀⠀⠀\n\n\n")
        dependent_label.grid(row=0, column=3, padx=20, pady=(20, 10))
        dependent = customtkinter.CTkEntry(self.tabview.tab(tabname), placeholder_text="param1, param2, ...")
        dependent.grid(row=0, column=3, padx=20, pady=(20, 10))
        self.tabcontent[tabname]["Dependent"] = dependent

        init_val_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Init. value⠀⠀\n\n\n")
        init_val_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        init_val = customtkinter.CTkEntry(self.tabview.tab(tabname), placeholder_text="Init. value", width=80)
        init_val.grid(row=1, column=0, padx=20, pady=(20, 10))
        step_val_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Step value⠀⠀\n\n\n")
        step_val_label.grid(row=1, column=1, padx=20, pady=(20, 10))
        step_val = customtkinter.CTkEntry(self.tabview.tab(tabname), placeholder_text="Step value", width=80)
        step_val.grid(row=1, column=1, padx=20, pady=(20, 10))
        tol_val_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Tol. value⠀⠀\n\n\n")
        tol_val_label.grid(row=1, column=2, padx=20, pady=(20, 10))
        tol_val = customtkinter.CTkEntry(self.tabview.tab(tabname), placeholder_text="Tol. value", width=80)
        tol_val.grid(row=1, column=2, padx=20, pady=(20, 10))
        self.tabcontent[tabname]["Init val"] = init_val
        self.tabcontent[tabname]["Step val"] = step_val
        self.tabcontent[tabname]["Tol val"] = tol_val

        remove_button = customtkinter.CTkButton(self.tabview.tab(tabname), command=self.remove_parameter_event, text="Remove parameter", fg_color='red', hover_color='darkred')
        remove_button.grid(row=1, column=3, padx=20, pady=(20, 10))

        tol_val_label = customtkinter.CTkLabel(self.tabview.tab(tabname), text="Alignment metrics of parameters")
        tol_val_label.place(x=25, y=175)
        subtab = customtkinter.CTkTabview(self.tabview.tab(tabname), width=600)
        subtab.place(x=25, y=200)
        subtab.add("+")
        subtab.tab("+").grid_columnconfigure(0, weight=1)
        metric_name = customtkinter.CTkEntry(subtab.tab("+"), placeholder_text="Channel name...")
        metric_name.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        metric_name_button = customtkinter.CTkButton(subtab.tab("+"), command=self.new_metric_event, text="Add new metric")
        metric_name_button.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        
        self.tabcontent[tabname]["Subtab"] = subtab
        self.tabcontent[tabname]["New metric"] = metric_name
        self.tabcontent[tabname]["Metrics"] = {}

    def metric_init(self, name, param_name):
        self.tabcontent[param_name]["Metrics"][name] = {}
        one_label = customtkinter.CTkLabel(self.tabcontent[param_name]["Subtab"].tab(name), text="\n  \n e.g. Speed>26.0")
        one_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        two_label = customtkinter.CTkLabel(self.tabcontent[param_name]["Subtab"].tab(name), text="\n \n  e.g. Speed")
        two_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        third_label = customtkinter.CTkLabel(self.tabcontent[param_name]["Subtab"].tab(name), text="\n \n  e.g. 1.0")
        third_label.grid(row=1, column=1, padx=20, pady=(20, 10))
        filter = customtkinter.CTkEntry(self.tabcontent[param_name]["Subtab"].tab(name), placeholder_text="Filter condition...")
        filter.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.tabcontent[param_name]["Metrics"][name]["filter"] = filter
        arg = customtkinter.CTkEntry(self.tabcontent[param_name]["Subtab"].tab(name), placeholder_text="Argument channel")
        arg.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        self.tabcontent[param_name]["Metrics"][name]["arg"] = arg
        mult = customtkinter.CTkEntry(self.tabcontent[param_name]["Subtab"].tab(name), placeholder_text="Cost multiplicator")
        mult.grid(row=1, column=1, padx=20, pady=20, sticky="n")
        self.tabcontent[param_name]["Metrics"][name]["mult"] = mult
        remove_button = customtkinter.CTkButton(self.tabcontent[param_name]["Subtab"].tab(name), command=self.remove_metric_event, text="Remove metric", fg_color='red', hover_color='darkred')
        remove_button.grid(row=1, column=2, padx=20, pady=(20, 10))
        cost = customtkinter.CTkOptionMenu(self.tabcontent[param_name]["Subtab"].tab(name), dynamic_resizing=False, values=["regress_square_cost", "interp_square_cost", "closest_square_cost"], width=200)
        cost.grid(row=0, column=1, padx=20, pady=(20, 10))
        self.tabcontent[param_name]["Metrics"][name]["cost"] = cost

    def start_alignment_event(self):
        print("Starting alignment")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def new_math_channel_event(self):
        print("New math channel event")

        name = self.new_math_name.get()
        formula = self.new_math_formula.get()
        if not name:
            tkinter.messagebox.showwarning(title="Write a name", message="Write a name of new math. channel")
            return
        if not formula:
            tkinter.messagebox.showwarning(title="Write a formula", message="Write a formula of new math. channel")
            return
        self.math_channel_init(name, formula)


    def remove_channel_event(self, name, number):
        self.math_channels[name]["name_field"].destroy()
        self.math_channels[name]["formula_field"].destroy()
        self.math_channels[name]["remove button"].destroy()
        del self.math_channels[name]
        for each in self.math_channels:
            if self.math_channels[each]["row"] > number:
                new_row = self.math_channels[each]["row"]-1
                self.math_channels[each]["name_field"].grid(row=new_row, column=0, padx=10, pady=(0, 20))
                self.math_channels[each]["formula_field"].grid(row=new_row, column=1, padx=10, pady=(0, 20))
                self.math_channels[each]["remove button"].grid(row=new_row, column=2, padx=10, pady=(0, 20))
        print("Remove channel event from: "+name)


    def plus_tab_creating(self):
        self.tabview.add("+")
        self.tabview.tab("+").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.param_name = customtkinter.CTkEntry(self.tabview.tab("+"), placeholder_text="Parameter name...")
        self.param_name.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.new_parameter_button = customtkinter.CTkButton(self.tabview.tab("+"), command=self.new_parameter_event, text="Add new parameter")
        self.new_parameter_button.grid(row=1, column=0, padx=20, pady=20, sticky="n")

        self.reading_param = tkinter.Text(self.tabview.tab("+"), width=35, height=15, font=('Cascadia Mono', 15))
        self.reading_param.place(x=25, y=250)
        self.reading_param.insert('1.0', "lib.xmlScalarReading(xml, '<param_name_from_xml>')")
        self.writing_param = tkinter.Text(self.tabview.tab("+"), width=35, height=15, font=('Cascadia Mono', 15))
        self.writing_param.place(x=500, y=250)
        self.writing_param.insert('1.0', "lib.xmlScalarWriting(xml, '<param_name_from_xml>', value_script_update)")

        reading_label = customtkinter.CTkLabel(self.tabview.tab("+"), text="Parameter reading code:", anchor="w")
        reading_label.place(x=25, y=140)
        writing_label = customtkinter.CTkLabel(self.tabview.tab("+"), text="Parameter writing code:", anchor="w")
        writing_label.place(x=340, y=140)
        info_label1 = customtkinter.CTkLabel(self.tabview.tab("+"), text="*code must be written in Python. Use 'value_script_update' as new value for writing and 'xml' as file. ", anchor="w")
        info_label1.place(x=25, y=450)
        info_label2 = customtkinter.CTkLabel(self.tabview.tab("+"), text="** in shown example substitude  <param_name_from_xml> for simple parameters from xml file.", anchor="w")
        info_label2.place(x=25, y=475)

    def new_parameter_event(self):
        print("New parameter event!")        
        self.tabview.delete("+")
        name = self.param_name.get()
        if name:
            self.tabview.add(name)
            self.tabcontent[name] = {}
            self.tab_init(name)
        else:
            tkinter.messagebox.showwarning(title="Write a name", message="Write a name of new parameter")
        self.tabcontent[name]["Reading"] = self.reading_param.get()
        self.tabcontent[name]["Writing"] = self.writing_param.get()
        self.plus_tab_creating()     

    def remove_parameter_event(self):
        print("Remove parameter event!")
        name = self.tabview.get()
        self.tabview.delete(name)
        del self.tabcontent[name]

    def new_metric_event(self):
        print("New metric event!")
        param_name = self.tabview.get()
        metric_name = self.tabcontent[param_name]["New metric"].get()
        if not metric_name:
            tkinter.messagebox.showwarning(title="Write a name", message="Write a name of new metric")
            return
        self.tabcontent[param_name]["Subtab"].delete("+")
        self.tabcontent[param_name]["Subtab"].add(metric_name)
        self.tabcontent[param_name]["Subtab"].add("+")
        self.tabcontent[param_name]["Subtab"].tab("+").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabcontent[param_name]["New metric"] = customtkinter.CTkEntry(self.tabcontent[param_name]["Subtab"].tab("+"), placeholder_text="Channel name...")
        self.tabcontent[param_name]["New metric"].grid(row=0, column=0, padx=20, pady=20, sticky="n")
        new_metric_button = customtkinter.CTkButton(self.tabcontent[param_name]["Subtab"].tab("+"), command=self.new_metric_event, text="Add new metric")
        new_metric_button.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        self.metric_init(metric_name, param_name)

    def remove_metric_event(self):
        print("Remove metric event!")
        name = self.tabview.get()
        metric_name = self.tabcontent[name]["Subtab"].get()
        self.tabcontent[name]["Subtab"].delete(metric_name)
        del self.tabcontent[name]["Metrics"][metric_name]

    def real_data_event(self):
        self.path = tkinter.filedialog.askopenfilename()
        self.real_file.configure(text = "\n\n\n"+self.path.split('/')[-1])
        self.ChannelsLoading()

    def ChannelsLoading(self):
        isExisting = os.path.exists(self.path)
        if not isExisting:
            tkinter.messagebox.showwarning(title="File not founded", message="Real data file was not founded.")
        return isExisting
            

    def save_config_event(self):
        print("Save config file")
        save_data = {}
        save_data["config"] = {}
        save_data["inputs"] = {}
        save_data["outputs"] = {}
        save_data["mat_outputs"] = {}
        save_data["output_aliasing"] = {}

        # config part
        save_data["config"]["optimization"] = self.optimtype.get()
        save_data["config"]["parallel"] = bool(self.switch1.get())
        save_data["config"]["surrogate"] = bool(self.switch2.get())
        save_data["config"]["fast_parse"] = bool(self.switch3.get())
        save_data["config"]["n_cores"] = int(self.cpu.get())
        save_data["config"]["track"] = self.track.get()
        save_data["config"]["racecar"] = self.racecar.get()
        save_data["config"]["reference"] = self.path

        # inputs part
        for each in self.tabcontent:
            save_data["inputs"][each] = {}
            save_data["inputs"][each]["usage"] = bool(self.tabcontent[each]["Enable"].get())
            save_data["inputs"][each]["priority"] = int(self.tabcontent[each]["Priority"])
            save_data["inputs"][each]["experiment"] = self.tabcontent[each]["Experiment"].get()
            save_data["inputs"][each]["init_val"] = float(self.tabcontent[each]["Init val"].get())
            save_data["inputs"][each]["init_step"] = float(self.tabcontent[each]["Step val"].get())
            save_data["inputs"][each]["tolerance"] = float(self.tabcontent[each]["Tol val"].get())
            save_data["inputs"][each]["access_r"] = self.tabcontent[each]["Reading"]
            save_data["inputs"][each]["access_w"] = self.tabcontent[each]["Writing"]
            if self.tabcontent[each]["Dependent"].get():
                save_data["inputs"][each]["dependent"] = self.tabcontent[each]["Dependent"].get().split(", ")
            else:
                save_data["inputs"][each]["dependent"] = None
            save_data["inputs"][each]["affect_on"] = {}
            for every in self.tabcontent[each]["Metrics"]:                
                save_data["inputs"][each]["affect_on"][every] = {}
                save_data["inputs"][each]["affect_on"][every]["filter"] = self.tabcontent[each]["Metrics"][every]["filter"].get()
                save_data["inputs"][each]["affect_on"][every]["wrt"] = self.tabcontent[each]["Metrics"][every]["arg"].get()
                save_data["inputs"][each]["affect_on"][every]["multiplicator"] = float(self.tabcontent[each]["Metrics"][every]["mult"].get())
                save_data["inputs"][each]["affect_on"][every]["cost"] = self.tabcontent[each]["Metrics"][every]["cost"].get()

        # mat outputes parts
        for each in self.math_channels:
            save_data["mat_outputs"][self.math_channels[each]["name_field"].get()] = self.math_channels[each]["formula_field"].get()

        # default values
        save_data["output_aliasing"]["Lap Distance"] = "Distance"
        save_data["output_aliasing"]["LapDistance"] = "Distance"
        save_data["output_aliasing"]["speed"] = "Speed"

        for each in list(save_data["mat_outputs"].keys()):
            save_data["outputs"][each] = True

        if self.ChannelsLoading():
            with open(self.path, 'r') as read_obj:
                    csv_reader = reader(read_obj)
                    for _ in range(18):
                        _=next(csv_reader)
                    self.real_data = next(csv_reader)[0].split()
        else:
            return
        for each in self.real_data:
            save_data["outputs"][each] = True


        save_path = tkinter.filedialog.asksaveasfile()
        with open(save_path.name, 'w') as file:
            yaml.dump(save_data, file)

if __name__ == "__main__":
    app = App()
    app.mainloop()
