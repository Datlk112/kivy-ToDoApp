from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
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


# from pcalender.datepicker_fa import DatePickerFa


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
        super().__init__(**kwargs)
        
    def build(self):
        self.theme_cls.material_style = "M3"
        self.screen = Builder.load_file("todo.kv")
        # screen = Builder.load_file("todo.kv")
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        layout = MDFloatLayout()  # root layout
        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

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
            row_data=[("1","Hi","Welcome",'1403-03-03',"True","True")
                      ,("2","Hi","Welcome",'1403-03-02',"False","True")
                      ],
            
        )
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.cards_layout = MDBoxLayout(orientation='vertical', spacing=10,  padding = [10,10]  , size_hint_min_y= Window.height ,top=20 )
        self.scroll = MDScrollView(do_scroll_y = True , do_scroll_x = False  , bar_width = "4dp")

        today = MDLabel(
                text="Today Tasks",
                color="grey",
                markup = True,
                font_style="H5",
                bold=True,
                adaptive_size=True,
                font_name = "assets/fonts/SedanSC-Regular.ttf")
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
                    size=(Window.width-20, dp(100)),  # تنظیم عرض هر کارت برابر با عرض صفحه و ارتفاع 100dp
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
                    orientation="vertical",  # تعیین جهت عمودی برای MDBoxLayout
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
                    size=(Window.width-20, dp(100)),  # تنظیم عرض هر کارت برابر با عرض صفحه و ارتفاع 100dp
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
                    orientation="vertical",  # تعیین جهت عمودی برای MDBoxLayout
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
    


    def update_cards(self, new_data):
        self.cards_layout.clear_widgets()
        self.scroll.clear_widgets()
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
        selected_row_index = self.data_tables.row_data.index(data)
        num,title,description,date,Priority=data[0],data[1],data[2],data[3],data[4]
        Done = "False" if data[5]=="True" else "True"
        self.data_tables.update_row(
                self.data_tables.row_data[selected_row_index],  # old row data
                [num,title,description,date,Priority,Done],          # new row data
            )
        
        self.update_cards(new_data=self.data_tables.row_data)
        
            
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

        self.Important_checkk = MDCheckbox(size_hint= (None, None) ,size= ("48dp", "48dp"),color_inactive= "gray")
        priority_layout = MDBoxLayout(orientation='horizontal', size_hint_x=.2, adaptive_height=True, )
        
        
        priority_layout.add_widget(self.Important_checkk)
        priority_layout.add_widget(self.Important_label)
        
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
        date_dialog = MDDatePicker(min_year=JalaliDate.today().year,min_date=JalaliDate.today(),max_year=JalaliDate.today().year+10,title_input="EDIT DATE",radius=[7, 7, 7, 26],primary_color="purple")
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
        date_dialog = MDDatePicker(min_year=JalaliDate.today().year,min_date=JalaliDate.today(),max_year=JalaliDate.today().year+10,title_input="SET DATE",radius=[7, 7, 7, 26],primary_color="purple")
        date_dialog.bind(on_save=self.on_saves, on_cancel=self.on_cancels)
        date_dialog.open()

        
        
    def add_row(self, *args):
        try: 
            # title = self.dialog.content_cls.ids.title.text
            # Date = self.dialog.content_cls.ids.Date.text
            title = self.Title_Field.text
            Date = self.Date_Field.text
            Priority = "False"
            Done = "False"
            if self.Important_check.active:
                Priority = "True"
            else :
                Priority = "False"
            if len(self.data_tables.row_data) > 0 :
                last_num_row = int(self.data_tables.row_data[-1][0])
            else :
                last_num_row = 0
            if self.Description_Field.text == "":
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", "_" , f"{Date}") , f"{Priority}" , f"{Done}")
            else:
                description = self.Description_Field.text
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", f"{description}" , f"{Date}" , f"{Priority}" , f"{Done}" ))
            self.dialog.dismiss()
            self.Title_Field.text = ""
            self.Description_Field.text = ""
            self.Date_Field.text = ""
            self.update_cards(new_data=self.data_tables.row_data)
        except Exception as e :
            print(f"{e}")


    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
            
        print(instance_table, self.selected_rows)
        
    def edit_row(self, **args ):
    # Implement the edit functionality here
        try:
            row = self.selected_rows[-1]
            print(self.data_tables.row_data)
            selected_row_index = self.data_tables.row_data.index(tuple(self.selected_rows[-1]))
            print(selected_row_index)
            print(row)
            # self.Title_Field_edit.text = row[1]
            # self.Description_Field_edit.text = row[2]
            # self.Date_Field_edit.text = row[3]
            self.show_edit_dialog(current_row=row, row_index=selected_row_index)
        except Exception as e:
            print(self.data_tables.row_data)
            print(f"{e}")
        
        
    def edit_data(self ,instance_button, **args ):
        try: 
            Priority = "False"
            Done = "False"
            if self.Important_checkk.active:
                Priority = "True"
            else :
                Priority = "False"
            print(self.data_tables.row_data)
            selected_row_index = self.data_tables.row_data.index(tuple(self.selected_rows[-1]))
            title = self.Title_Field_edit.text
            date = self.Date_Field_edit.text
            
            num = self.data_tables.row_data[selected_row_index][0]
            if self.Description_Field_edit.text == "":
                description = "_"
                
            else:
                description = self.Description_Field_edit.text
            self.data_tables.update_row(
                self.data_tables.row_data[selected_row_index],  # old row data
                [num,title,description,date,Priority,Done],          # new row data
            )
            self.selected_rows.clear()
            self.dialog.dismiss()
            self.dialogs = None
            self.dialoggs = None
            self.Title_Field_edit.text = ""
            self.Description_Field_edit.text = ""
            self.Date_Field_edit.text = ""
            self.update_cards(new_data=self.data_tables.row_data)
        except Exception as e :
            print(self.data_tables.row_data)
            print(f"{e}")
                    
    
    def add(self) -> None:
        self.show_confirmation_dialog()

    def remove_row(self) -> None:
        try:
            if len(self.data_tables.row_data) > 1:
                print(self.data_tables.row_data)
                selected_row_index = self.data_tables.row_data.index(tuple(self.selected_rows[-1]))
                print(selected_row_index)
                self.data_tables.remove_row(self.data_tables.row_data[selected_row_index])
                self.selected_rows.clear()
                self.update_cards(new_data=self.data_tables.row_data)
                try:
                    self.selected_rows.append(self.data_tables.row_data[selected_row_index])
                except Exception as e:
                    print(f"{e}")
                
            else: 
                self.data_tables.remove_row(self.data_tables.row_data[0])
        except Exception as e:
            print(f"{e}")
    
ToDoApp().run()






############## 
"""
For tomarrow i should do these changes to my app:
1.Make screens looks pretty / ALMOST DONE!
2.adding Done and Delete button based on row checkmarks / DONE!
3.changing the style of Add tasks button / DONE!
4.Searching for notifications / FAILED!
5.Adding a sqllite Database to my app
6.changing the texts fonts / DONE!
7.make the lottie file for presplash screen
8.Make filters settings 
9.make Prioroty sections in md dialog / DONE!
10.make one screen to list items like they are listed by : tomarrow,today or ...   / ALMOST DONE!  
"""
##############