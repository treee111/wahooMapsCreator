"""
functions and object for processing input via CLI and GUI
"""
#!/usr/bin/python

# import official python packages
import argparse
import sys
from platform import uname

# for gui
import tkinter as tk
from tkinter import ttk

# import custom python packages
from common_python import constants


class InputData():
    """
    object with all parameters to process maps and default values
    """

    def __init__(self):
        self.region = ""
        self.country = ""
        self.max_days_old = 14

        self.force_download = False
        self.force_processing = False
        self.border_countries = False
        self.save_cruiser = False
        self.only_merge = False

        self.tag_wahoo_xml = "tag-wahoo.xml"
        # Folder /output/country and /output/country-maps map folders
        # True - Keep them after compression
        # False - Delete them after compression
        self.keep_map_folders = False

        # Way of calculating the relevant tiles for given input (country)
        # True - Use geofabrik index-v1.json file
        # False - Use .json files from folder /common_resources/json
        self.geofabrik_tiles = False


class Input(tk.Tk):
    """
    This is the class to proces user-input via CLI and GUI
    """

    def __init__(self, *args, **kwargs):
        self.o_input_data = InputData()

        if 'microsoft' in uname().release:
            self.gui_mode = False
            return

        if len(sys.argv) == 1:
            self.gui_mode = True

            tk.Tk.__init__(self, *args, **kwargs)
        else:
            self.gui_mode = False

    def start_gui(self):
        """
        start GUI
        """
        self.build_gui()

        # start GUI
        self.mainloop()

        return self.o_input_data

    def build_gui(self):
        """
        builds GUI consisting of several parts
        """
        # build GUI
        # self.geometry("420x360")
        self.title("Wahoo map creator")
        self.configure(bg="white")

        # create notebook + tabs
        tab_control = ttk.Notebook(self, name="notebook")
        tab1 = tk.Frame(tab_control, name="tab1")
        tab2 = tk.Frame(tab_control)

        # add tabs to notebook & position
        tab_control.add(tab1, text="General settings")
        tab_control.add(tab2, text="Advanced settings")
        tab_control.pack(expand=1, fill="both")

        # content of 1. tab
        tab1.first = ComboboxesEntryField(
            tab1, self.o_input_data.max_days_old)
        tab1.first.pack(side=tk.TOP, fill=tk.X)

        tab1.third = Checkbuttons(
            tab1, self.o_input_data, controller=self)
        tab1.third.pack(side=tk.TOP, fill=tk.X)

        tab1.four = Buttons(tab1, controller=self)
        tab1.four.pack(side=tk.TOP, fill=tk.X)

        # content of 2. tab
        tk.Label(tab2, text="This is the second tag!").grid(
            column=0, row=0, padx=30, pady=30)

    def handle_create_map(self, event):
        """
        run when Button "Create" is pressed
        """
        self.o_input_data.region = self.first.cb_continent.get().replace("-", "")
        self.o_input_data.country = self.first.cb_country.get()
        self.o_input_data.max_days_old = int(self.first.input_maxdays.get())

        self.o_input_data.force_download = self.third.checkb_download.get()
        self.o_input_data.force_processing = self.third.checkb_processing.get()
        self.o_input_data.border_countries = self.third.checkb_border_countries.get()
        self.o_input_data.save_cruiser = self.third.checkb_save_cruiser.get()

        self.destroy()

    def switch_reload(self, event):
        """
        switch edit-mode of max-days field
        """
        if self.first.en_max_days_old['state'] == tk.NORMAL:
            self.first.en_max_days_old.configure(state=tk.DISABLED)
        else:
            self.first.en_max_days_old.configure(state=tk.NORMAL)

    def cli_arguments(self):
        """
        process CLI arguments
        """

        o_input_data = InputData()

        # input argument creation and processing
        desc = "Create up-to-date maps for your Wahoo ELEMNT and Wahoo ELEMNT BOLT"
        parser = argparse.ArgumentParser(description=desc)

        # country or file to create maps for
        parser.add_argument("country", help="country to generate maps for")
        # Maximum age of source maps or land shape files before they are redownloaded
        parser.add_argument('-md', '--maxdays', type=int, default=o_input_data.max_days_old,
                            help="maximum age of source maps and other files")
        # Calculate also border countries of input country or not
        parser.add_argument('-bc', '--bordercountries', action='store_true',
                            help="process whole tiles which involve border countries")
        # Force download of source maps and the land shape file
        # If False use Max_Days_Old to check for expired maps
        # If True force redownloading of maps and landshape
        parser.add_argument('-fd', '--forcedownload', action='store_true',
                            help="force download of files")
        # Force (re)processing of source maps and the land shape file
        # If False only process files if not existing
        # If True force processing of files
        parser.add_argument('-fp', '--forceprocessing', action='store_true',
                            help="force processing of files")
        # Save uncompressed maps for Cruiser if True
        parser.add_argument('-c', '--cruiser', action='store_true',
                            help="save uncompressed maps for Cruiser")
        # specify the file with tags to keep in the output // file needs to be in common_resources
        parser.add_argument('-tag', '--tag_wahoo_xml', default=self.o_input_data.tag_wahoo_xml,
                            help="file with tags to keep in the output")
        # specify the file with tags to keep in the output // file needs to be in common_resources
        parser.add_argument('-om', '--only_merge', action='store_true',
                            help="only merge, do no other processing")
        # option to keep the /output/country/ and /output/country-maps folders in the output
        parser.add_argument('-km', '--keep_map_folders', action='store_true',
                            help="keep the country and country-maps folders in the output")
        # option to calculate tiles to process based on Geofabrik index-v1.json file
        parser.add_argument('-gt', '--geofabrik_tiles', action='store_true',
                            help="calculate tiles based on geofabrik index-v1.json file")

        # set instance-attributes of class
        # try:
        args = parser.parse_args()

        o_input_data = InputData()
        o_input_data.country = args.country
        o_input_data.max_days_old = args.maxdays

        o_input_data.force_download = args.forcedownload
        o_input_data.force_processing = args.forceprocessing
        o_input_data.border_countries = args.bordercountries
        o_input_data.save_cruiser = args.cruiser
        o_input_data.tag_wahoo_xml = args.tag_wahoo_xml
        o_input_data.only_merge = args.only_merge
        o_input_data.keep_map_folders = args.keep_map_folders
        o_input_data.geofabrik_tiles = args.geofabrik_tiles

        return o_input_data

        # except SystemExit:
        #     return False


class ComboboxesEntryField(tk.Frame):
    """
    Comboboxes and Entry-Field for max days
    """

    def __init__(self, parent, default_max_days_old):
        tk.Frame.__init__(self, parent)

        # Labels
        self.lab_top = tk.Label(
            self, text="Select continent and country to create a map")
        self.lab_continent = tk.Label(self, text="Select continent:")
        self.lab_country = tk.Label(self, text='Select country:')

        # Comboboxes
        self.cb_continent = ttk.Combobox(
            self, values=constants.continents, state="readonly")
        self.cb_continent.current(0)  # pre-select first entry in combobox
        self.cb_continent.bind("<<ComboboxSelected>>", self.callback_continent)

        self.cb_country = ttk.Combobox(
            self, values=constants.europe, state="readonly")
        # cboCountry.current(0)

        # Positioning
        self.lab_top.grid(column=0, row=0, columnspan=2, padx=5, pady=10)

        self.lab_continent.grid(column=0, row=1, sticky=tk.E, padx=5, pady=2)
        self.cb_continent.grid(column=1, row=1, sticky=tk.W, padx=10, pady=2)

        self.lab_country.grid(column=0, row=2, sticky=tk.E, padx=5, pady=2)
        self.cb_country.grid(column=1, row=2, sticky=tk.W, padx=10, pady=2)

        self.lab_max_days_old = tk.Label(self, text='Max Old Days:')

        self.input_maxdays = tk.StringVar()
        self.input_maxdays.set(str(default_max_days_old))

        self.en_max_days_old = tk.Entry(
            self, textvar=self.input_maxdays, width=5)

        self.lab_max_days_old.grid(
            column=0, row=3, sticky=tk.E, padx=5, pady=2)
        self.en_max_days_old.grid(column=1, row=3, sticky=tk.W, padx=10)

    def callback_continent(self, event):
        """
        set value-list of countries after changing continent
        """
        continent = self.cb_continent.get()
        # get countries for selected region and set for combobox
        self.cb_country["values"] = getattr(
            constants, continent.replace("-", ""))
        self.cb_country.current(0)


class Checkbuttons(tk.Frame):
    """
    Checkbuttons for GUI
    """

    def __init__(self, parent, oInputData, controller):
        tk.Frame.__init__(self, parent)  # , bg="red"
        self.controller = controller

        self.checkb_download = tk.BooleanVar()
        self.checkb_download.set(oInputData.force_download)

        self.chk_force_download = tk.Checkbutton(self, text="Force download",
                                                 var=self.checkb_download)
        self.chk_force_download.bind(
            "<Button-1>", self.controller.switch_reload)

        self.checkb_processing = tk.BooleanVar()
        self.checkb_processing.set(oInputData.force_processing)

        self.checkb_border_countries = tk.BooleanVar()
        self.checkb_border_countries.set(oInputData.border_countries)

        self.checkb_save_cruiser = tk.BooleanVar()
        self.checkb_save_cruiser.set(oInputData.save_cruiser)

        self.chk_force_processing = tk.Checkbutton(self, text="Force processing",
                                                   var=self.checkb_processing)

        self.chk_border_countries = tk.Checkbutton(self, text="Process border countries",
                                                   var=self.checkb_border_countries)

        self.chk_save_cruiser = tk.Checkbutton(self, text="Save uncompressed maps for Cruiser",
                                               var=self.checkb_save_cruiser)

        self.chk_border_countries.grid(
            column=0, row=0, sticky=tk.W, padx=15, pady=5)
        self.chk_force_download.grid(
            column=0, row=1, sticky=tk.W, padx=15, pady=5)
        self.chk_force_processing.grid(
            column=0, row=2, sticky=tk.W, padx=15, pady=5)
        self.chk_save_cruiser.grid(column=0, row=3, columnspan=2, sticky=tk.W,
                                   padx=15, pady=5)


class Buttons(tk.Frame):
    """
    Buttons for GUI
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="light grey")
        self.controller = controller
        self.btn_ok = tk.Button(self, text="Create map")
        self.btn_ok.bind("<Button-1>", self.controller.handle_create_map)

        self.btn_cancel = tk.Button(self, text="Exit", command=parent.destroy)

        self.btn_ok.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_cancel.pack(side=tk.RIGHT, fill=tk.X, expand=True)
