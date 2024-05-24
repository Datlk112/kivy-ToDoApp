from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton,MDIconButton,MDFloatingActionButton
from kivymd.uix.relativelayout import MDRelativeLayout
from librariess.datepicker import MDDatePicker
import datetime
from datetime import date
from kivy.utils import get_color_from_hex
from kivymd.uix.menu import MDDropdownMenu
from persiantools.jdatetime import JalaliDate
from kivymd.uix.selectioncontrol import MDCheckbox,MDSwitch
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard,MDSeparator
from kivy.properties import StringProperty
from kivy.core.window import Window
from typing import Union
from kivy.clock import Clock
from kivy.core.window.window_sdl2 import WindowSDL
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
import humanize
from kivymd.uix.segmentedcontrol import (
    MDSegmentedControl, MDSegmentedControlItem
)
from kivy.utils import platform
from kivymd.toast import toast 
import sqlite3

# If keyboard is going on the text boxes
Window.keyboard_anim_args = {'d':.2 , 't':'in_out_expo'}
Window.softinput_mode = "below_target"
Window.keyboard = 'numeric'

class DialogContent(MDBoxLayout):
    orientation= "vertical",
    spacing= "12dp",
    size_hint_y= None,
    height= "200dp",



class MD3Card(MDCard):
    text = StringProperty()
    subtext = StringProperty()

class ToDoApp(MDApp):
    dialogs = None
    dialoggs = None

    def __init__(self, **kwargs):
        self.selected_rows = []
        self.all_data_list = []
        self.Done_data_list = []
        self.n = 0
        super().__init__(**kwargs)
        
    def build(self):
        self.theme_cls.material_style = "M3"
        self.screen = Builder.load_file("todo.kv")
        # screen = Builder.load_file("todo.kv")
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        """ Creating DataBase or connect to one """
        conn = sqlite3.connect("Taks.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists tasks (   
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Num INTEGER NOT NULL,
            Title VARCHAR(255) NOT NULL,
            Description VARCHAR(255) NULL,
            DueDate datetime NOT NULL,
            Priority boolean NOT NULL DEFAULT 'False',
            Done VARCHAR(255) NOT NULL DEFAULT 'False'
        )""")
        conn.commit()
        conn.close()

        layout = MDFloatLayout()  # root layout
        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        # add/delete/edit Buttons
        for button_text in ["Add row", "Remove row","edit"]:
            if button_text == "Add row":
                icons = "plus"
                color = "#00FF00"
            elif button_text == "Remove row":
                icons = "delete"
                color = "#FF0000"
            else:
                icons = "pencil"
                color= self.theme_cls.primary_color
            button_box.add_widget(
                MDFloatingActionButton(
                    icon=icons,text=button_text, on_release=self.on_button_press,type="small",theme_icon_color="Custom",md_bg_color = color
                )
            )
        # Create datatable to showing task dashboard
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.48, "center_x": 0.5},
            size_hint=(0.9, 0.7),
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(20)),
                ("Title", dp(30)),
                ("Description", dp(60)),
                ("Due Date", dp(25)),
                ("Priority", dp(15)),
                ("Done", dp(15)),
  
            ],
            row_data=[
                      ],
            
        )
        
        # Connection for return all datas saved in data base
        conn = sqlite3.connect("Taks.db")
        c = conn.cursor()
        sql = f""" SELECT * FROM tasks"""
        c.execute(sql)
        ids = c.fetchall()
        for id in ids :
            """ 
            id[0] = id, id[1] = Num , id[2] = Title , id[3] = Description , id[4] = DueDate , id[5] = Priority , id[6] = Done 
            """
            # I prefer to use id for showing number and it means you can delete 'Num' from database
            self.data_tables.row_data.append([str(id[0]),id[2],id[3],id[4],id[5],id[6]])
        
        self.data_tables.bind(on_check_press=self.on_check_press)
        # Creating card layout by MDGridLayout and dynamic size 
        self.cards_layout = MDGridLayout(cols=1, spacing=10,  padding = [10,10]  , size_hint_min_y= dp(100)*len(self.data_tables.row_data) + dp(200), top=20 )
        self.scroll = MDScrollView(do_scroll_y = True , bar_width = "4dp", size=(Window.width, 1) , always_overscroll=True)     # Here is scroll settings
 
        today = MDLabel(
                text="Today Tasks",
                color="grey",
                markup = True,
                font_style="H5",
                bold=True,
                adaptive_size=True,
                font_name = "assets/fonts/Itim-Regular.ttf"
                )
        self.cards_layout.add_widget(today)
        for data in self.data_tables.row_data:
            datee = data[3].split("-")
            year = int(datee[0])
            month = int(datee[1])
            day = int(datee[2])
            print(datee)
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.to_gregorian()
            humanized_date = humanize.naturalday(gregorian_date)
            if gregorian_date == date.today():
                print("yes")
                print(humanized_date)
                card = MD3Card(
                    size_hint=(1, None),
                    size=(Window.width-20, dp(100)), 
                    md_bg_color= "#EFDBF1" if data[5] == "False" else "#D6D6D6",
                    pos_hint={"top": 1},
                    style = "elevated" if data[4] == "False" else "outlined",
                    line_color="#ED685E" if data[4] == "True" else (0,0,0,0),
                    line_width = 2,
                    shadow_softness=5,
                    shadow_offset=(0, 1),
                )
                rel = MDRelativeLayout()
                current_data = data
                
                myicon = MDIconButton(
                    icon="check-bold" if data[5]=="False" else "close-thick",
                    theme_text_color="Custom",  
                    text_color= [0, .8, .6, 1] if data[5]=="False" else [.8,0,.5,1] ,
                    pos_hint={"top": 1, "right": 1},
                    on_release=lambda x, current_data=current_data: self.Done(current_data)
                )
                
                card_layout = MDBoxLayout(
                    orientation="vertical", 
                    spacing=dp(40),
                    padding=[15,0,0,15]

                )
                
                label1 = MDLabel(
                    text=data[1] if data[5]=="False" else f"[s]{data[1]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    adaptive_size=True,
                    font_name = "assets/fonts/SedanSC-Regular.ttf"
                )

                label2 = MDLabel(
                    text=data[2] if data[5]=="False" else f"[s]{data[2]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    font_style="Body2",
                    adaptive_size=True,
                    font_name = "assets/fonts/ARLRDBD.TTF"
                )
                
                label3 = MDLabel(
                    text=humanized_date.capitalize(),
                    markup = True,
                    theme_text_color = 'Custom',
                    text_color="grey",
                    # bold=True,
                    font_style="Caption",
                    adaptive_size=True,
                    font_name = "assets/fonts/SansSerifCollection.ttf",
                    pos_hint={"top": .25, "right": .98},
                    
                )
                     
                card_layout.add_widget(label1)
                card_layout.add_widget(label2)
                rel.add_widget(myicon)
                rel.add_widget(label3)
                rel.add_widget(card_layout)
                card.add_widget(rel)
                
                self.cards_layout.add_widget(card)
            
        
        
        future = MDLabel(
            text="Future Tasks",
            color="grey",
            markup = True,
            font_style="H5",
            bold=True,
            adaptive_size=True,
            font_name = "assets/fonts/SedanSC-Regular.ttf"
        )
        sep = MDSeparator(
            color = (0.8, 0.8, 0.8, 0.5),
        )
        self.cards_layout.add_widget(sep)
        self.cards_layout.add_widget(future)
        for data in self.data_tables.row_data:
            datee = data[3].split("-")
            year = int(datee[0])
            month = int(datee[1])
            day = int(datee[2])
            print(datee)
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.to_gregorian()
            humanized_date = humanize.naturalday(gregorian_date)
            if gregorian_date != date.today():
                print("Yes")
                        
                print(humanized_date)
                card = MD3Card(
                    size_hint=(1, None),
                    size=(Window.width-20, dp(100)), 
                    md_bg_color= "#EFDBF1" if data[5]=="False" else "#D6D6D6",
                    pos_hint={"top": 1},
                    style = "elevated" if data[4] == "False" else "outlined",
                    line_color="#ED685E" if data[4] == "True" else (0,0,0,0),
                    line_width = 2,
                    shadow_softness=5,
                    shadow_offset=(0, 1),
                )
                rel = MDRelativeLayout()
                current_dataaaa = data
                myicon = MDIconButton(
                    icon="check-bold" if data[5]=="False" else "close-thick",
                    theme_text_color="Custom",  
                    text_color= [0, .8, .6, 1] if data[5]=="False" else [.8,0,.5,1] ,
                    pos_hint={"top": 1, "right": 1},
                    on_release=lambda x, current_data=current_dataaaa: self.Done(current_data)
                )
                        
                card_layout = MDBoxLayout(
                    orientation="vertical",
                    spacing=dp(40),
                    padding=[15,0,0,15]


                )
                        
                label1 = MDLabel(
                    text=data[1] if data[5]=="False" else f"[s]{data[1]}[/s]",
                    color="grey",
                    markup = True,
                    
                    bold=True if data[5]=="False" else False,
                    adaptive_size=True,
                    font_name = "assets/fonts/SedanSC-Regular.ttf"
                )

                label2 = MDLabel(
                    text=data[2] if data[5]=="False" else f"[s]{data[2]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    font_style="Body2",
                    adaptive_size=True,
                    font_name = "assets/fonts/ARLRDBD.TTF"
                )
                        
                label3 = MDLabel(
                    text=humanized_date.capitalize(),
                    markup = True,
                    theme_text_color = 'Custom',
                    text_color="grey",
                    # bold=True,
                    font_style="Caption",
                    adaptive_size=True,
                    font_name = "assets/fonts/SansSerifCollection.ttf",
                    pos_hint={"top": .25, "right": .98},
                            
                )
                        
                card_layout.add_widget(label1)
                card_layout.add_widget(label2)
                        
                # card.add_widget(card_layout)
                        
                rel.add_widget(myicon)
                rel.add_widget(label3)
                rel.add_widget(card_layout)
                card.add_widget(rel)
                        
                self.cards_layout.add_widget(card)
                
        self.scroll.add_widget(self.cards_layout)
        
        self.screen.ids.scrollDash.add_widget(self.scroll)  
        self.screen.ids.table_holder.add_widget(self.data_tables)
        self.screen.ids.table_holder.add_widget(button_box)
        return self.screen
    
    def segment_control(
                            self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ) -> None:
        """ 
        This section was for sehment selection for filtering datas
        It has bug that after 3  or 4 times selection it will not show anything in table
        """
        '''Called when the segment is activated.'''
        
        print(self.n)
        try:
            conn = sqlite3.connect("Taks.db")
            c = conn.cursor()
            sql2 = f""" SELECT * FROM tasks """
            c.execute(sql2)
            all = c.fetchall()
            sql3 = f""" SELECT * FROM tasks WHERE Done = 'True' """
            c.execute(sql3)
            Done = c.fetchall()
            if self.data_tables.row_data :
                
                filter_type = segmented_item.text
                if filter_type == "All tasks":
                    list_all = []
                    for id in all :
                        list_all.append([str(id[0]),id[2],id[3],id[4],id[5],id[6]])
                        self.data_tables.row_data = list_all
                elif filter_type == "Completed tasks":
                    print("HI")
                    list_done = []
                    for id in Done :
                        list_done.append([str(id[0]),id[2],id[3],id[4],id[5],id[6]])
                        self.data_tables.row_data = list_done


            else:
                print("data table is empty!")
                if platform == 'android':
                    toast("Table is empty!",gravity=80 ,length_long = 1.5)
                else:
                    toast("Table is empty!", duration=1.5 ,background=[1,0,0,1])
        
        except Exception as e :
            print(f"{e}")
            if platform == 'android':
                toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])
            

    def update_cards(self, new_data):
        self.cards_layout.clear_widgets()
        self.scroll.clear_widgets()
        self.cards_layout.size_hint_min_y= dp(100)*len(self.data_tables.row_data) + dp(200)
        todayy = MDLabel(
                text="Today Tasks",
                color="grey",
                markup = True,
                font_style="H5",
                bold=True,
                adaptive_size=True,
                font_name = "assets/fonts/SedanSC-Regular.ttf")
        self.cards_layout.add_widget(todayy)
        for data in new_data:
            dateee = data[3].split("-")
            year = int(dateee[0])
            month = int(dateee[1])
            day = int(dateee[2])
            print(dateee)
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.to_gregorian()
            humanized_date = humanize.naturalday(gregorian_date)
            print(humanized_date)
            if gregorian_date == date.today():
                print("yes")
                card = MD3Card(
                    size_hint=(1, None),
                    size=(Window.width-20, dp(100)),  
                    md_bg_color= "#EFDBF1" if data[5] == "False" else "#D6D6D6",
                    pos_hint={"top": 1},
                    ripple_behavior = True,
                    style = "elevated" if data[4] == "False" else "outlined",
                    line_color="#ED685E" if data[4] == "True" else (0,0,0,0),
                    line_width = 2,
                    shadow_softness=5,
                    shadow_offset=(0, 1),
                )

                rel = MDRelativeLayout()
                
                current_dataa = data
                myicon = MDIconButton(
                    icon="check-bold" if data[5]=="False" else "close-thick",
                    theme_text_color="Custom",  
                    text_color= [0, .8, .6, 1] if data[5]=="False" else [.8,0,.5,1],
                    pos_hint={"top": 1, "right": 1},
                    on_release=lambda x, current_data=current_dataa: self.Done(current_data)
                )
                
                card_layout = MDBoxLayout(
                    orientation="vertical", 
                    spacing=dp(40),
                    padding=[15,0,0,15]


                )
                
                label1 = MDLabel(
                    text=data[1] if data[5]=="False" else f"[s]{data[1]}[/s]",
                    color="grey",
                    
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    adaptive_size=True,
                    font_name = "assets/fonts/SedanSC-Regular.ttf"
                )

                label2 = MDLabel(
                    text=data[2] if data[5]=="False" else f"[s]{data[2]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    font_style="Body2",
                    adaptive_size=True,
                    font_name = "assets/fonts/ARLRDBD.TTF"
                )

                label3 = MDLabel(
                    text=humanized_date.capitalize(),
                    markup = True,
                    theme_text_color = 'Custom',
                    text_color="grey",
                    # bold=True,
                    font_style="Caption",
                    adaptive_size=True,
                    font_name = "assets/fonts/SansSerifCollection.ttf",
                    pos_hint={"top": .25, "right": .98},
                    
                )
                card_layout.add_widget(label1)
                card_layout.add_widget(label2)

                rel.add_widget(myicon)
                rel.add_widget(label3)
                rel.add_widget(card_layout)
                card.add_widget(rel)

                self.cards_layout.add_widget(card)
        futuree = MDLabel(
            text="Future Tasks",
            color="grey",
            markup = True,
            font_style="H5",
            bold=True,
            adaptive_size=True,
            font_name = "assets/fonts/SedanSC-Regular.ttf"
        )
        sepe = MDSeparator(
            color = (0.8, 0.8, 0.8, 0.5),
        )
        self.cards_layout.add_widget(sepe)
        self.cards_layout.add_widget(futuree)
        for data in new_data:
            dateee = data[3].split("-")
            year = int(dateee[0])
            month = int(dateee[1])
            day = int(dateee[2])
            print(dateee)
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.to_gregorian()
            humanized_date = humanize.naturalday(gregorian_date)
            print(humanized_date)
            if gregorian_date != date.today():
                print("yes")
                card = MD3Card(
                    size_hint=(1, None),
                    size=(Window.width-20, dp(100)),  
                    md_bg_color= "#EFDBF1" if data[5] == "False" else "#D6D6D6",
                    pos_hint={"top": 1},
                    ripple_behavior = True,
                    style = "elevated" if data[4] == "False" else "outlined",
                    line_color="#ED685E" if data[4] == "True" else (0,0,0,0),
                    line_width = 2,
                    shadow_softness=5,
                    shadow_offset=(0, 1),
                )

                rel = MDRelativeLayout()
                
                current_dataaa = data
                myicon = MDIconButton(
                    icon="check-bold" if data[5]=="False" else "close-thick",
                    theme_text_color="Custom",  
                    text_color= [0, .8, .6, 1] if data[5]=="False" else [.8,0,.5,1],
                    pos_hint={"top": 1, "right": 1},
                    on_release=lambda x, current_data=current_dataaa: self.Done(current_data)
                )
                
                card_layout = MDBoxLayout(
                    orientation="vertical", 
                    spacing=dp(40),
                    padding=[15,0,0,15]


                )
                
                label1 = MDLabel(
                    text=data[1] if data[5]=="False" else f"[s]{data[1]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    adaptive_size=True,
                    font_name = "assets/fonts/SedanSC-Regular.ttf"
                )

                label2 = MDLabel(
                    text=data[2] if data[5]=="False" else f"[s]{data[2]}[/s]",
                    color="grey",
                    markup = True,
                    bold=True if data[5]=="False" else False,
                    font_style="Body2",
                    adaptive_size=True,
                    font_name = "assets/fonts/ARLRDBD.TTF"
                )

                label3 = MDLabel(
                    text=humanized_date.capitalize(),
                    markup = True,
                    theme_text_color = 'Custom',
                    text_color="grey",
                    # bold=True,
                    font_style="Caption",
                    adaptive_size=True,
                    font_name = "assets/fonts/SansSerifCollection.ttf",
                    pos_hint={"top": .25, "right": .98},
                    
                )
                card_layout.add_widget(label1)
                card_layout.add_widget(label2)

                rel.add_widget(myicon)
                rel.add_widget(label3)
                rel.add_widget(card_layout)
                card.add_widget(rel)

                self.cards_layout.add_widget(card)
        self.scroll.add_widget(self.cards_layout)
      
      
            
    def Done(self,data):
        """ Here is a function for checking the done button in dashboard """
        try:
            print(f"data = {data}")
            print(self.data_tables.row_data)
            conn = sqlite3.connect("Taks.db")
            c = conn.cursor()
            selected_row_index = self.data_tables.row_data.index(data)
            num,title,description,date,Priority=data[0],data[1],data[2],data[3],data[4]
            Done = str("False") if data[5]=="True" else str("True")
            sql = f'''UPDATE tasks SET Done = '{Done}' WHERE id = {num}'''
            c.execute(sql)
            conn.commit()
            conn.close()
            self.data_tables.update_row(
                    self.data_tables.row_data[selected_row_index],  # old row data
                    [num,title,description,date,Priority,Done],          # new row data
                )
            if platform == 'android':
                toast("Your task was completed!",gravity=80 ,length_long = 1.5)
            else:
                toast("Your task was completed!", duration=1.5 ,background=[1,0,0,1])
            self.update_cards(new_data=self.data_tables.row_data)
        except Exception as e:
            print(f"{e}")
            if platform == 'android':
                toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])    
            
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Add row": self.add,
                "Remove row": self.remove_row,
                "edit":self.edit_row,
            }[instance_button.text]()
        except KeyError:
            pass
        
    def show_confirmation_dialog(self, *args):
        dialog_content = MDBoxLayout(orientation= "vertical",spacing= "12dp",size_hint_y= None,height= "200dp")
        date_layout = MDBoxLayout(orientation='horizontal', size_hint_x=1, adaptive_height=True)
        self.Title_Field= MDTextField(
                        id="Title",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Title",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=1,
                        height=dp(700),
                        multiline=False,
                        
                        text="",
                    )
        self.Description_Field= MDTextField(
                        id="Description",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Description",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=1,
                        height=dp(700),
                        multiline=False,
                        
                        text="",
                    )
        self.Date_Field= MDTextField(
                        id="Date",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Date",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=.4,
                        height=dp(700),
                        multiline=False,
                        helper_text= "yyyy/mm/dd",
                        text="",
                    )
        self.Date_icon = MDIconButton (
            icon= "calendar-clock",
            theme_text_color= "Custom",
            # pos_hint= {"center_x": 0.325, "y": 1},
            icon_color= get_color_from_hex("4b5f80"),
            on_release=self.show_calendar
            
        )
        self.Important_label = MDLabel(text = "Prioritised" , font_name ="assets/fonts/Itim-Regular.ttf" ,font_style = "Subtitle1" , halign="left", size= ("10dp", "48dp"))

        self.Important_check = MDCheckbox(size_hint= (None, None) ,size= ("48dp", "48dp"),color_inactive= "gray")
        priority_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.2, adaptive_height=True, )
        
        dialog_content.add_widget(self.Title_Field)
        dialog_content.add_widget(self.Description_Field)
        date_layout.add_widget(self.Date_Field)
        date_layout.add_widget(self.Date_icon)
        priority_layout.add_widget(self.Important_check)
        priority_layout.add_widget(self.Important_label)
        date_layout.add_widget(priority_layout)
        dialog_content.add_widget(date_layout)
        if not self.dialogs:
            self.dialog = MDDialog(
                title="Enter Tasks:",
                type="custom",
                content_cls=dialog_content,
                
                # content_cls = DialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK",
                        on_release=self.add_row
                    ),
                ],
            )
        self.dialog.open()    


    def show_edit_dialog(self, *args , current_row , row_index):
        dialog_contentt = MDBoxLayout(orientation= "vertical",spacing= "12dp",size_hint_y= None,height= "200dp")
        date_layoutt = MDBoxLayout(orientation='horizontal', size_hint_x=1, adaptive_height=True)
        self.Title_Field_edit= MDTextField(
                        id="Title",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Title",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=1,
                        height=dp(700),
                        multiline=False,
                        
                        text="",
                    )
        self.Description_Field_edit= MDTextField(
                        id="Description",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Description",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=1,
                        height=dp(700),
                        multiline=False,
                        
                        text="",
                    )
        self.Date_Field_edit= MDTextField(
                        id="Date",
                        # color_mode="Custom",
                        # theme_text_color="Custom",
                        mode="rectangle",
                        active_line=False,
                        line_color_normal=get_color_from_hex("4b5f80"),
                        radius=[25, 25, 25, 25],
                        line_color_focus=get_color_from_hex("4b5f80"),
                        fill_color_normal=(1, 1, 1, 0),
                        text_color_focus=(0, 0, 0, 1),
                        text_color_normal=get_color_from_hex("4b5f80"),
                        hint_text_color_focus=(0, 0, 0, 1),
                        hint_text="     Date",
                        # pos_hint={"center_x": 0.325, "center_y": 0.84},
                        size_hint_x=.4,
                        height=dp(700),
                        multiline=False,
                        helper_text= "yyyy/mm/dd",
                        text="",
                    )
        self.Date_icon = MDIconButton (
            icon= "calendar-clock",
            theme_text_color= "Custom",
            # pos_hint= {"center_x": 0.325, "y": 1},
            icon_color= get_color_from_hex("4b5f80"),
            on_release=self.show_calendars    
        )
        self.Important_label = MDLabel(text = "Prioritised" , font_name ="assets/fonts/Itim-Regular.ttf" ,font_style = "Subtitle1" , halign="left", size= ("10dp", "48dp"))

        self.Important_checkk = MDCheckbox(size_hint= (None, None) ,size= ("48dp", "48dp"),color_inactive= "gray",)
        priority_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.2, adaptive_height=True, )
        
        
        priority_layout.add_widget(self.Important_checkk)
        priority_layout.add_widget(self.Important_label)
        
        
        if current_row[4] == "True":
            self.Important_checkk.active = True
        else:
            self.Important_checkk.active = False
        self.Title_Field_edit.text = current_row[1]
        self.Description_Field_edit.text = current_row[2]
        self.Date_Field_edit.text = current_row[3]
        dialog_contentt.add_widget(self.Title_Field_edit)
        dialog_contentt.add_widget(self.Description_Field_edit)
        date_layoutt.add_widget(self.Date_Field_edit)
        date_layoutt.add_widget(self.Date_icon)
        date_layoutt.add_widget(priority_layout)
        dialog_contentt.add_widget(date_layoutt)
        if not self.dialoggs:
            self.dialog = MDDialog(
                title="Edit Tasks:",
                type="custom",
                content_cls=dialog_contentt,
                
                # content_cls = DialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK",
                        on_release=self.edit_data
                    ),
                ],
            )
        self.dialog.open()
        

        
    def on_save(self, instance, value, date_range,*args):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        try:
            date_str = value.strftime('%Y-%m-%d')
            # self.dialog.content_cls.ids.Date.text = date_str
            self.Date_Field.text = date_str
            print(date_str)
        except Exception as e :
            print(f"{e}")
        print(instance, value, date_range)
        print(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass

    def show_calendar(self, *args):
        """ This section is for showing datepicker for adding datas (Notice that its not common kivymd date picker and i changed it to jalali date picker)"""
        date_dialog = MDDatePicker(min_year=JalaliDate.today().year,min_date=JalaliDate.today(),max_year=JalaliDate.today().year+10,title="SET DATE",radius=[7, 7, 7, 26],primary_color="purple")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        
        
        
    def on_saves(self, instance, value, date_range,*args):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        try:
            self.Date_Field_edit.text = ""
            date_str = value.strftime('%Y-%m-%d')
            # self.dialog.content_cls.ids.Date.text = date_str
            self.Date_Field_edit.text = date_str
        except Exception as e :
            print(f"{e}")
        print(instance, value, date_range)
        print(value)

    def on_cancels(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass

    def show_calendars(self, *args):
        """ This section is for showing datepicker for edit datas (Notice that its not common kivymd date picker and i changed it to jalali date picker)"""
        date_dialog = MDDatePicker(min_year=JalaliDate.today().year,min_date=JalaliDate.today(),max_year=JalaliDate.today().year+10,title="EDIT DATE",radius=[7, 7, 7, 26],primary_color="purple")
        date_dialog.bind(on_save=self.on_saves, on_cancel=self.on_cancels)
        date_dialog.open()

        
        
    def add_row(self, *args):
        """ This section is for adding row in the last line of datatable"""
        try: 
            title = self.Title_Field.text
            Date = self.Date_Field.text
            Priority = "False"
            Done = "False"
            if self.Important_check.active:
                Priority = "True"
            else :
                Priority = "False"
            if len(self.data_tables.row_data) > 0 :      #Checking if we have data in table (number1)
                last_num_row = int(self.data_tables.row_data[-1][0])
            else :                                       #Checking if we have not data in table
                last_num_row = 0
            if self.Description_Field.text == "":
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", "_" , f"{Date}") , f"{Priority}" , f"{Done}")
            else:
                description = self.Description_Field.text
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", f"{description}" , f"{Date}" , f"{Priority}" , f"{Done}" ))
            """ Openning sql connection for save tasks"""
            conn = sqlite3.connect("Taks.db")
            c = conn.cursor()
            sql = 'INSERT INTO tasks (Num, Title, Description, DueDate, Priority, Done) VALUES (?, ?, ?, ?, ?, ?)'
            c.execute(sql, (last_num_row + 1, title, description, Date, Priority, Done))
            conn.commit()
            sql2 = f""" SELECT * FROM tasks """
            c.execute(sql2)
            data = c.fetchall()
            print(f"data = {data}")
            conn.commit()
            conn.close()
            self.dialog.dismiss()
            self.Title_Field.text = ""
            self.Description_Field.text = ""
            self.Date_Field.text = ""
            if platform == 'android':
                toast("Your task has been added",gravity=80 ,length_long = 1.5)
            else:
                toast("Your task has been added", duration=1.5 ,background=[1,0,0,1])
            self.update_cards(new_data=self.data_tables.row_data)  # this is for updating card in dashboard
        except Exception as e :
            print(f"{e}")
            if platform == 'android':
                toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])


    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
            
        print(instance_table, self.selected_rows)
        
        
    def edit_row(self, **args ):
        """ This section is a function that showing edit dialog with sending row index and row-data"""
        try:
            row = self.selected_rows[-1]
            print(self.data_tables.row_data)
            selected_row_index = self.data_tables.row_data.index(list(self.selected_rows[-1]))
            print(selected_row_index)
            print(row)
            self.show_edit_dialog(current_row=row, row_index=selected_row_index)
        except Exception as e:
            print(self.data_tables.row_data)
            print(f"{e}")
            if platform == 'android':
                toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])
        
        
    def edit_data(self ,instance_button, **args ):
        """ This section is for editing data and working by update_row() method in datatables.py"""
        try: 
            if self.Important_checkk.active:
                Priority = "True"   
            else :
                Priority = "False"
            print(self.data_tables.row_data)
            selected_row_index = self.data_tables.row_data.index(list(self.selected_rows[-1]))
            title = self.Title_Field_edit.text
            date = self.Date_Field_edit.text
            num = self.data_tables.row_data[selected_row_index][0]
            conn = sqlite3.connect("Taks.db")
            c = conn.cursor()
            sql = f""" SELECT * FROM tasks WHERE id = {num}"""
            c.execute(sql)
            id = c.fetchone()[0]
            print(f"id = {id}")
            Done = self.data_tables.row_data[selected_row_index][5]
            if self.Description_Field_edit.text == "":
                description = "_"
                
            else:
                description = self.Description_Field_edit.text
            """
            Here is main function to change datas text in table 
            """
            self.data_tables.update_row(
                self.data_tables.row_data[selected_row_index],  # old row data
                [num,title,description,date,Priority,Done],          # new row data
            )
            
            """ Openning sql connection for save tasks"""
            sql1 = f'''UPDATE tasks 
                    SET Num = ?, Title = ?, Description = ?, DueDate = ?, Priority = ?, Done = ?
                    WHERE id = {id}'''
            c.execute(sql1, (num, title, description, date, Priority, Done))
            sql2 = f""" SELECT * FROM tasks """
            c.execute(sql2)
            data = c.fetchall()
            print(f"data = {data}")
            conn.commit()
            conn.close()
            self.selected_rows.clear()
            self.update_cards(new_data=self.data_tables.row_data)  # this is for updating card in dashboard
            
            self.selected_rows.clear()
            self.dialog.dismiss()  # Closing the dialog
            self.dialogs = None
            self.dialoggs = None
            self.Title_Field_edit.text = ""
            self.Description_Field_edit.text = ""
            self.Date_Field_edit.text = ""
            if platform == 'android':
                toast("Your task has been editted",gravity=80 ,length_long = 1.5)
            else:
                toast("Your task has been editted", duration=1.5 ,background=[1,0,0,1])
            self.update_cards(new_data=self.data_tables.row_data)
            
        except Exception as e :
            print(self.data_tables.row_data)
            print(f"{e}")
            if platform == 'android':
                toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])
                    
    
    def add(self) -> None:
        self.show_confirmation_dialog()

    def remove_row(self) -> None:
        """ This section is for a function to remove row
            First of all we should find the selection checkbox index row to remove it row """
        try:
            conn = sqlite3.connect("Taks.db")
            c = conn.cursor()
            if len(self.data_tables.row_data) >= 1:  #If we have more than one tasks in table
                print(self.data_tables.row_data)
                selected_row_index = self.data_tables.row_data.index(list(self.selected_rows[-1]))
                print(selected_row_index)
                num = self.data_tables.row_data[selected_row_index][0]
                self.data_tables.remove_row(self.data_tables.row_data[selected_row_index]) # Main remove section
                

                sql1 = f'DELETE FROM tasks WHERE id = {num}'
                c.execute(sql1)
                sql2 = f""" SELECT * FROM tasks """
                c.execute(sql2)
                data = c.fetchall()
                print(f"data = {data}")
                conn.commit()
                conn.close()
                self.selected_rows.clear()
                
                
                try:
                    self.selected_rows.append(self.data_tables.row_data[selected_row_index])  # Its because of checkbox doesnt delete after removing row and it checked so I write this line to change it to next line and person can uncheck that
                except Exception as e:
                    print(f"{e}")
                
            else: 
                self.data_tables.remove_row(self.data_tables.row_data[0]) # If we have only on task in table
                sql1 = f'DELETE FROM tasks WHERE Num = 1'
                c.execute(sql1)
                conn.commit()
                conn.close()
            if platform == 'android':
                toast("Your task has been removed",gravity=80 ,length_long = 1.5)
            else:
                toast("Your task has been removed", duration=1.5 ,background=[1,0,0,1])
            self.update_cards(new_data=self.data_tables.row_data)  # this is for updating card in dashboard
        except Exception as e:
            print(f"{e}")
            if platform == 'android':
                    toast("Please try again!",gravity=80 ,length_long = 1.5)
            else:
                toast("Please try again!", duration=1.5 ,background=[1,0,0,1])

if __name__ == "__main__":    
    ToDoApp().run()






############## 
"""
For tomarrow i should do these changes to my app:
1.Make screens looks pretty / DONE!
2.adding Done and Delete button based on row checkmarks / DONE!
3.changing the style of Add tasks button / DONE!
4.Searching for notifications / FAILED!
5.Adding a sqllite Database to my app / FINAL TASK! / DONE!
6.changing the texts fonts / DONE!
7.make the lottie file for presplash screen
8.Make filters segments settings / DONE! 
9.make Prioroty sections in md dialog / DONE!
10.make one screen to list items like they are listed by : tomarrow,today or ...   / DONE!  
11.writing comments for each sections / ALMOST DONE!
12.Adding toasts for error handleres / DONE!
"""
##############