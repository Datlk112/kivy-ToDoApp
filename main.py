from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton,MDIconButton,MDFloatingActionButton
from kivymd.uix.relativelayout import MDRelativeLayout
from librariess.datepicker import MDDatePicker
import datetime
from kivy.utils import get_color_from_hex
from kivymd.uix.menu import MDDropdownMenu
from persiantools.jdatetime import JalaliDate
# from pcalender.datepicker_fa import DatePickerFa


class DialogContent(MDBoxLayout):
    orientation= "vertical",
    spacing= "12dp",
    size_hint_y= None,
    height= "200dp",





class ToDoApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.material_style = "M3"
        screen = Builder.load_file("todo.kv")
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

        # Create a table.
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
  
            ],
            row_data=[("1", "1", "2","3")],
        )
        # Adding a table and buttons to the toot layout.
        # screen.add_widget(button_box)

        

    
        
        screen.ids.table_holder.add_widget(self.data_tables)
        screen.ids.table_holder.add_widget(button_box)
        return screen
    
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Add row": self.add,
                "Remove row": self.remove_row,
                "edit":self.add,
            }[instance_button.text]()
        except KeyError:
            pass
        
    def show_confirmation_dialog(self, *args):
        dialog_content = MDBoxLayout(orientation= "vertical",spacing= "12dp",size_hint_y= None,height= "250dp")
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
        
        dialog_content.add_widget(self.Title_Field)
        dialog_content.add_widget(self.Description_Field)
        date_layout.add_widget(self.Date_Field)
        date_layout.add_widget(self.Date_icon)
        dialog_content.add_widget(date_layout)
        if not self.dialog:
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
        except Exception as e :
            print(f"{e}")
        print(instance, value, date_range)
        print(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass

    def show_calendar(self, *args):
        date_dialog = MDDatePicker(min_year=JalaliDate.today().year,min_date=JalaliDate.today(),max_year=JalaliDate.today().year+10,title_input="SET DATE",radius=[7, 7, 7, 26],primary_color="purple")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

        
        
    def add_row(self, *args):
        try: 
            # title = self.dialog.content_cls.ids.title.text
            # Date = self.dialog.content_cls.ids.Date.text
            title = self.Title_Field.text
            Date = self.Date_Field.text
            if self.Description_Field.text == "":
                last_num_row = int(self.data_tables.row_data[-1][0])
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", "_" , f"{Date}"))
            else:
                description = self.Description_Field.text
                last_num_row = int(self.data_tables.row_data[-1][0])
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", f"{description}" , f"{Date}"))
            self.dialog.dismiss()
        except Exception as e :
            print(f"{e}")

    def add(self) -> None:
        self.show_confirmation_dialog()

    def remove_row(self) -> None:
        if len(self.data_tables.row_data) > 1:
            self.data_tables.remove_row(self.data_tables.row_data[-1])
    def remove_row(self):
                if len(self.data_tables.row_data) > 1:
                    self.data_tables.remove_row(self.data_tables.row_data[-1])
ToDoApp().run()






############## 
"""
For tomarrow i should do these changes to my app:
1.Make screens looks pretty 
2.adding Done and Delete button based on row checkmarks /
3.changing the style of Add tasks button /
4.Searching for notifications 
5.Adding a sqllite Database to my app
6.changing the texts fonts
7.make the lottie file for presplash screen
8.Make filters settings
9.make Prioroty sections in md dialog
10.make one screen to list items like they are listed by : tomarrow,today or ...     
"""
##############