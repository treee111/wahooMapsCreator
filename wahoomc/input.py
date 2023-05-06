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
from wahoomc.geofabrik_json import GeofabrikJson
from wahoomc.geofabrik_json import CountyIsNoGeofabrikCountry
from wahoomc.geofabrik import CountryGeofabrik


def process_call_of_the_tool():
    """
    process CLI arguments
    """
    # input argument creation and processing
    desc = "Create up-to-date maps for your Wahoo ELEMNT and Wahoo ELEMNT BOLT"
    parser_top = argparse.ArgumentParser(description=desc)

    subparsers = parser_top.add_subparsers(title='Choose mode',
                                           description='choose the mode of using wahooMapsCreator. Either GUI or CLI.',
                                           help='sub-command help', dest='subparser_name')

    # create the parser for the "gui" command
    parser_gui = subparsers.add_parser(  # pylint: disable=unused-variable
        'gui', help='Start graphical user interface to select options')

    # create the parser for the "cli" command
    parser_cli = subparsers.add_parser(
        'cli', help='Run the tool via command line interface', formatter_class=argparse.RawTextHelpFormatter)

    # group: primary input parameters to create map for. One needs to be given
    primary_args = parser_cli.add_argument_group(
        title='Primary input', description='Generate maps for...')
    primary_args_excl = primary_args.add_mutually_exclusive_group(
        required=True)
    # country to create maps for
    primary_args_excl.add_argument(
        "-co", "--country", help="country to generate maps for.\nExample: -co malta, multiple countries separated by comma: -co malta,italy")
    # X/Y coordinates to create maps for
    primary_args_excl.add_argument(
        "-xy", "--xy_coordinates", help="x/y coordinates to generate maps for.\nExample: -xy 133/88, multiple xy coordinates separated by comma: -xy 133/88,134/89")

    # group: options for map generation
    options_args = parser_cli.add_argument_group(
        title='Options', description='Options for map generation')
    # Maximum age of source maps or land shape files before they are redownloaded
    options_args.add_argument('-md', '--maxdays', type=int, default=InputData().max_days_old,
                              help="maximum age of source maps and other files")
    # Do not calculate border countries of input country
    options_args.add_argument('-nbc', '--bordercountries', action='store_false',
                              help="do not process border countries of tiles involving more than one country")
    # calculate contour lines
    options_args.add_argument('-con', '--contour', action='store_true',
                              help="process contour lines (elevation data)")
    # use srtm1 for contour lines
    options_args.add_argument('-srtm1', '--use_srtm1', action='store_true',
                              help="use srtm1 as source for contour lines (elevation data)")
    # Force download of source maps and the land shape file
    # If False use Max_Days_Old to check for expired maps
    # If True force redownloading of maps and landshape
    options_args.add_argument('-fd', '--forcedownload', action='store_true',
                              help="force download of files")
    # Force (re)processing of source maps and the land shape file
    # If False only process files if not existing
    # If True force processing of files
    options_args.add_argument('-fp', '--forceprocessing', action='store_true',
                              help="force processing of files")
    # Save uncompressed maps for Cruiser if True
    options_args.add_argument('-c', '--cruiser', action='store_true',
                              help="save uncompressed maps for Cruiser")
    # specify the file with tags to keep in the output // file needs to be in wahoo_mc/resources/tag_wahoo_adjusted
    options_args.add_argument('-tag', '--tag_wahoo_xml', default=InputData().tag_wahoo_xml,
                              help="file with tags to keep in the output")
    # zip the country (and country-maps) folder
    options_args.add_argument('-z', '--zip', action='store_true',
                              help="zip the country (and country-maps) folder")
    options_args.add_argument('-v', '--verbose', action='store_true',
                              help="output debug logger messages")

    args = parser_top.parse_args()

    # process depending on GUI or CLI processing.
    # returns the input parameters in both cases
    if args.subparser_name == 'gui':
        # Prevents the initialisation of the graphical GUI on WSL.
        if 'microsoft' in uname().release:
            sys.exit("GUI can not be startet because no graphical interface is available. Start with 'python -m wahoo_mc cli -h' or 'python -m wahoo_mc -h' to see command line options.")

        o_input_data = GuiInput().start_gui()
        return o_input_data

    # cli processing
    o_input_data = InputData()
    o_input_data.country = args.country
    o_input_data.xy_coordinates = args.xy_coordinates
    o_input_data.max_days_old = args.maxdays

    o_input_data.process_border_countries = args.bordercountries
    o_input_data.contour = args.contour
    o_input_data.use_srtm1 = args.use_srtm1

    o_input_data.force_download = args.forcedownload
    o_input_data.force_processing = args.forceprocessing

    o_input_data.tag_wahoo_xml = args.tag_wahoo_xml
    o_input_data.save_cruiser = args.cruiser
    o_input_data.zip_folder = args.zip

    o_input_data.verbose = args.verbose

    return o_input_data


def cli_init():
    """
    Provides cli for initialization of user directory
    """

    parser = argparse.ArgumentParser(
        description='Copy config files to user directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="output debug logger messages")

    args = parser.parse_args()

    # cli processing
    o_input_data = InputData()
    o_input_data.verbose = args.verbose

    return o_input_data


def create_checkbox(self, default_value, description, row):
    """
    this is a reuse function for creating checkboxes.
    it
    - creates the checkbox in the given context "self"
    - returns the variable which can be accessed to get the value
      of the checkbox after clicking a button
    """
    bool_var = tk.BooleanVar()
    bool_var.set(default_value)

    # set checkbutton "anonymous". bool_var is later accessed to get the checkbox-value
    self.check_button = tk.Checkbutton(self, text=description,
                                       var=bool_var)
    self.check_button.grid(column=0, row=row, sticky=tk.W, padx=15, pady=5)

    return bool_var


def get_countries_of_continent_from_geofabrik(continent):
    """
    returns all countries of a continent to be selected in UI
    """
    countries = []
    for region, value in GeofabrikJson().geofabrik_overview.items():
        try:
            if value['parent'] == continent:
                countries.append(region)
        # regions/ continents do not have a parent
        except KeyError:
            pass

    return countries


class InputData():  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    object with all parameters to process maps and default values
    """

    def __init__(self):
        self.country = ""
        self.xy_coordinates = ""
        self.max_days_old = 14

        self.force_download = False
        self.force_processing = False
        self.process_border_countries = True
        self.contour = False
        self.use_srtm1 = False

        self.tag_wahoo_xml = "tag-wahoo-poi.xml"
        self.zip_folder = False
        self.save_cruiser = False

        self.verbose = False

    def is_required_input_given_or_exit(self, issue_message):
        """
        check, if the minimal required arguments is given:
        - country
        - x/y coordinates
        - file with tile coordinates
        If not, depending on the import parameter, the
        """
        if (self.country in ('None', '') and self.xy_coordinates in ('None', '')):
            if issue_message:
                sys.exit("Nothing to do. Start with -h or --help to see command line options."
                         "Or in the GUI select a country to create maps for.")
            else:
                sys.exit()
        elif self.country and self.xy_coordinates:
            sys.exit(
                "Country and X/Y coordinates are given. Only one of both is allowed!")
        elif self.country:
            # countries =
            try:
                CountryGeofabrik.split_input_to_list(self.country)
            except CountyIsNoGeofabrikCountry as exception:
                sys.exit(exception)

            # if we made it until here, sys.exit() was not called and therefore all countries OK ;-)
            return True
        else:
            return True


class GuiInput(tk.Tk):
    """
    This is the class to proces user-input via GUI
    """

    def __init__(self, *args, **kwargs):
        self.o_input_data = InputData()

        tk.Tk.__init__(self, *args, **kwargs)

    def start_gui(self):
        """
        start GUI
        """
        self.build_gui()

        # start GUI
        self.mainloop()

        self.o_input_data.is_required_input_given_or_exit(issue_message=True)
        return self.o_input_data

    def build_gui(self):
        """
        builds GUI consisting of several parts
        """
        # build GUI
        self.title("Wahoo map creator")
        self.configure(bg="white")

        # create notebook + tabs
        tab_control = ttk.Notebook(self, name="notebook")
        tab1 = tk.Frame(tab_control, name="tab1")
        tab2 = tk.Frame(tab_control, name="tab2")

        # add tabs to notebook & position
        tab_control.add(tab1, text="General settings")
        tab_control.add(tab2, text="Advanced settings")
        tab_control.pack(expand=1, fill="both")

        # content of 1. tab
        tab1.first = ComboboxesEntryField(
            tab1, self.o_input_data)
        tab1.first.pack(side=tk.TOP, fill=tk.X)

        tab1.third = CheckbuttonsTab1(
            tab1, self.o_input_data, controller=self)
        tab1.third.pack(side=tk.TOP, fill=tk.X)

        tab1.four = Buttons(tab1, controller=self)
        tab1.four.pack(side=tk.TOP, fill=tk.X)

        # content of 2. tab
        tab2.second = Text(tab2, self.o_input_data)
        tab2.second.pack(side=tk.TOP, fill=tk.X)

        tab2.first = CheckbuttonsTab2(
            tab2, self.o_input_data)
        tab2.first.pack(side=tk.TOP, fill=tk.X)

    def handle_create_map(self, event):  # pylint: disable=unused-argument
        """
        run when Button "Create" is pressed
        """
        # get tab1 and tab2 using "name" of the tkinker objects
        tab1 = self.children["notebook"].children["tab1"]
        tab2 = self.children["notebook"].children["tab2"]

        # you can get children of tkinker objects using ".winfo_children()"
        # other possibility for the above tab1 assignment:
        # tab1 = self.winfo_children()[0].winfo_children()[0]

        self.o_input_data.country = tab1.first.cb_country.get()
        self.o_input_data.max_days_old = int(tab1.first.input_maxdays.get())

        self.o_input_data.force_download = tab1.third.checkb_download.get()
        self.o_input_data.force_processing = tab1.third.checkb_processing_val.get()
        self.o_input_data.process_border_countries = tab1.third.checkb_border_countries_val.get()
        self.o_input_data.contour = tab1.third.checkb_contour_val.get()
        self.o_input_data.use_srtm1 = tab1.third.checkb_srtm1_val.get()

        self.o_input_data.save_cruiser = tab2.first.checkb_save_cruiser_val.get()
        self.o_input_data.zip_folder = tab2.first.checkb_zip_folder_val.get()
        self.o_input_data.verbose = tab2.first.checkb_verbose_val.get()

        # get text without \n in the end
        self.o_input_data.tag_wahoo_xml = tab2.second.input_tag_wahoo_xml.get()

        self.destroy()

    def switch_reload(self, event):  # pylint: disable=unused-argument
        """
        switch edit-mode of max-days field
        """
        tab1 = self.children["notebook"].children["tab1"]

        if tab1.first.en_max_days_old['state'] == tk.NORMAL:
            tab1.first.en_max_days_old.configure(state=tk.DISABLED)
        else:
            tab1.first.en_max_days_old.configure(state=tk.NORMAL)


class ComboboxesEntryField(tk.Frame):  # pylint: disable=too-many-instance-attributes
    """
    Comboboxes and Entry-Field for max days
    """

    def __init__(self, parent, oInputData):
        tk.Frame.__init__(self, parent)

        # Labels
        self.lab_top = tk.Label(
            self, text="Select continent and country to create a map")
        self.lab_continent = tk.Label(self, text="Select continent:")
        self.lab_country = tk.Label(self, text='Select country:')

        # Comboboxes
        self.cb_continent = ttk.Combobox(
            self, values=GeofabrikJson().geofabrik_regions, state="readonly")
        self.cb_continent.current(0)  # pre-select first entry in combobox
        self.cb_continent.bind("<<ComboboxSelected>>", self.callback_continent)

        self.cb_country = ttk.Combobox(
            self, state="readonly")

        # Positioning
        self.lab_top.grid(column=0, row=0, columnspan=2, padx=5, pady=10)

        self.lab_continent.grid(column=0, row=1, sticky=tk.E, padx=5, pady=2)
        self.cb_continent.grid(column=1, row=1, sticky=tk.W, padx=10, pady=2)

        self.lab_country.grid(column=0, row=2, sticky=tk.E, padx=5, pady=2)
        self.cb_country.grid(column=1, row=2, sticky=tk.W, padx=10, pady=2)

        self.lab_max_days_old = tk.Label(self, text='Max Old Days:')

        self.input_maxdays = tk.StringVar()
        self.input_maxdays.set(str(oInputData.max_days_old))

        self.en_max_days_old = tk.Entry(
            self, textvar=self.input_maxdays, width=5)

        self.lab_max_days_old.grid(
            column=0, row=3, sticky=tk.E, padx=5, pady=2)
        self.en_max_days_old.grid(column=1, row=3, sticky=tk.W, padx=10)

    def callback_continent(self, event):  # pylint: disable=unused-argument
        """
        set value-list of countries after changing continent
        """
        continent = self.cb_continent.get()
        # get countries for selected region and set for combobox
        self.cb_country["values"] = get_countries_of_continent_from_geofabrik(
            continent)
        self.cb_country.current(0)


class CheckbuttonsTab1(tk.Frame):
    """
    Checkbuttons for GUI - tab 2
    """

    def __init__(self, parent, oInputData, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.checkb_download = tk.BooleanVar()
        self.checkb_download.set(oInputData.force_download)

        self.chk_force_download = tk.Checkbutton(self, text="Force download",
                                                 var=self.checkb_download)
        self.chk_force_download.bind(
            "<Button-1>", self.controller.switch_reload)

        self.checkb_border_countries_val = create_checkbox(self, oInputData.process_border_countries,
                                                           "Process border countries", 0)
        self.checkb_contour_val = create_checkbox(self, oInputData.contour,
                                                  "process contour lines (elevation data)", 1)
        self.checkb_srtm1_val = create_checkbox(self, oInputData.use_srtm1,
                                                "use srtm1 as source for contour lines (elevation data)", 2)

        self.chk_force_download.grid(
            column=0, row=3, sticky=tk.W, padx=15, pady=5)
        self.checkb_processing_val = create_checkbox(self, oInputData.force_processing,
                                                     "Force processing", 4)


class Buttons(tk.Frame):
    """
    Buttons for GUI
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.btn_ok = tk.Button(self, text="Create map")
        self.btn_ok.bind("<Button-1>", self.controller.handle_create_map)

        self.btn_cancel = tk.Button(
            self, text="Exit", command=parent.master.master.destroy)

        self.btn_ok.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_cancel.pack(side=tk.RIGHT, fill=tk.X, expand=True)


class Text(tk.Frame):
    """
    Text for GUI - 2. tab
    """

    def __init__(self, parent, oInputData):
        tk.Frame.__init__(self, parent)

        self.lab_tag_wahoo_xml = tk.Label(self, text='Tag wahoo XML file:')

        self.input_tag_wahoo_xml = tk.StringVar()
        self.input_tag_wahoo_xml.set(oInputData.tag_wahoo_xml)

        self.en_max_days_old = tk.Entry(
            self, textvar=self.input_tag_wahoo_xml, width=20)

        self.lab_tag_wahoo_xml.grid(
            column=0, row=1, sticky=tk.E, padx=5, pady=2)
        self.en_max_days_old.grid(column=1, row=1, sticky=tk.W, padx=10)


class CheckbuttonsTab2(tk.Frame):
    """
    Checkbuttons for GUI - 2. tab
    """

    def __init__(self, parent, oInputData):
        tk.Frame.__init__(self, parent)

        self.checkb_save_cruiser_val = create_checkbox(self, oInputData.save_cruiser,
                                                       "Save uncompressed maps for Cruiser", 2)
        self.checkb_zip_folder_val = create_checkbox(self, oInputData.zip_folder,
                                                     "Zip folder with generated files", 3)
        self.checkb_verbose_val = create_checkbox(self, oInputData.verbose,
                                                  "output debug logger messages", 4)
