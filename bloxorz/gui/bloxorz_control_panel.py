from tkinter import Canvas, OptionMenu, \
    StringVar, Variable, Radiobutton, NW, Entry, W


class BloxorzControlPanel(Canvas):

    def __init__(self, master) -> None:
        self.stage = StringVar()
        self.algorithm = StringVar()
        self.algorithm.set("DFS")
        self.population_size = Variable(value=100)
        self.chromosome_length = Variable(value=20)
        self.mutation_chane = Variable(value=0.2)
        self.cross_type = StringVar()
        self.cross_type.set("default")
        self.distance_type = StringVar()
        self.distance_type.set("manhattan")
        self.default_font = ("Inter", 14 * -1)

        super().__init__(master=master, width=900, height=100,
                         bd=0, highlightthickness=0, relief="ridge", borderwidth=0)
        self.create_element()

    def create_element(self):
        self.create_text(10, 15, text="Stage", font=self.default_font, anchor=W)
        stage_option = OptionMenu(self, self.stage, "01", "02", "03", "04", "05", "10", "33")
        stage_option.place(x=60, y=15, anchor=W)

        self.create_text(200, 15, text="Algorithm", font=self.default_font, anchor=W)
        R1 = Radiobutton(text="DFS", value="DFS", variable=self.algorithm, font=self.default_font)
        R2 = Radiobutton(text="BrFS", value="BFS", variable=self.algorithm, font=self.default_font)
        R3 = Radiobutton(text="Genetic", value="Genetic", variable=self.algorithm, font=self.default_font)
        R1.place(x=380, y=15, anchor=W)
        R2.place(x=450, y=15, anchor=W)
        R3.place(x=520, y=15, anchor=W)

        self.create_text(10, 45, text="Population size", font=self.default_font, anchor=W)
        self.create_text(200, 45, text="Chromosome length", font=self.default_font, anchor=W)
        self.create_text(400, 45, text="Mutation chance", font=self.default_font, anchor=W)
        # Entry
        entry_1 = Entry(textvariable=self.population_size, justify='center')
        entry_1.place(x=210, y=45, width=60, height=24, anchor=W)
        entry_2 = Entry(textvariable=self.chromosome_length, justify='center')
        entry_2.place(x=430, y=45, width=40, height=24, anchor=W)
        entry_3 = Entry(textvariable=self.mutation_chane, justify='center')
        entry_3.place(x=620, y=45, width=40, height=24, anchor=W)

        self.create_text(10, 75, text="Cross type", font=self.default_font, anchor=W)
        self.create_text(200, 75, text="Distance type", font=self.default_font, anchor=W)
        # Option
        cross_type_option = OptionMenu(self, self.cross_type, "default", "custom")
        cross_type_option.place(x=100, y=75, anchor=W)
        distance_type_option = OptionMenu(self, self.distance_type, "manhattan", "maze")
        distance_type_option.place(x=300, y=75, anchor=W)

    def get_algorithm(self):
        return self.algorithm.get()

    def get_stage(self):
        return int(self.stage.get())

    def get_population_size(self):
        return int(self.population_size.get())

    def get_chromosome_length(self):
        return int(self.chromosome_length.get())

    def get_mutation_chane(self):
        return float(self.mutation_chane.get())

    def get_cross_type(self):
        return self.cross_type.get()

    def get_distance_type(self):
        return self.distance_type.get()


