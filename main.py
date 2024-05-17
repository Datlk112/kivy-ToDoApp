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
from kivymd.uix.selectioncontrol import MDCheckbox,MDSwitch
from kivymd.uix.label import MDLabel
# from pcalender.datepicker_fa import DatePickerFa


class DialogContent(MDBoxLayout):
    orientation= "vertical",
    spacing= "12dp",
    size_hint_y= None,
    height= "200dp",





class ToDoApp(MDApp):
    dialogs = None
    dialoggs = None

    def __init__(self, **kwargs):
        self.selected_rows = []
        super().__init__(**kwargs)
        
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
        self.data_tables.bind(on_check_press=self.on_check_press)
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
        self.Title_Field_edit.text = current_row[1]
        self.Description_Field_edit.text = current_row[2]
        self.Date_Field_edit.text = current_row[3]
        dialog_contentt.add_widget(self.Title_Field_edit)
        dialog_contentt.add_widget(self.Description_Field_edit)
        date_layoutt.add_widget(self.Date_Field_edit)
        date_layoutt.add_widget(self.Date_icon)
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
            if self.Description_Field.text == "":
                last_num_row = int(self.data_tables.row_data[-1][0])
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", "_" , f"{Date}"))
            else:
                description = self.Description_Field.text
                last_num_row = int(self.data_tables.row_data[-1][0])
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", f"{description}" , f"{Date}"))
            self.dialog.dismiss()
            self.Title_Field.text = ""
            self.Description_Field.text = ""
            self.Date_Field.text = ""
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
                [num,title,description,date],          # new row data
            )
            self.selected_rows.clear()
            self.dialog.dismiss()
            self.dialogs = None
            self.dialoggs = None
            self.Title_Field_edit.text = ""
            self.Description_Field_edit.text = ""
            self.Date_Field_edit.text = ""
        except Exception as e :
            print(self.data_tables.row_data)
            print(f"{e}")
                    
    
    def add(self) -> None:
        self.show_confirmation_dialog()

    def remove_row(self) -> None:
        if len(self.data_tables.row_data) > 1:
            print(self.data_tables.row_data)
            selected_row_index = self.data_tables.row_data.index(tuple(self.selected_rows[-1]))
            print(selected_row_index)
            self.data_tables.remove_row(self.data_tables.row_data[selected_row_index])
            self.selected_rows.clear()
            try:
                self.selected_rows.append(self.data_tables.row_data[selected_row_index])
            except Exception as e:
                print(f"{e}")
            
        else: 
            self.data_tables.remove_row(self.data_tables.row_data[0])
    
ToDoApp().run()






############## 
"""
For tomarrow i should do these changes to my app:
1.Make screens looks pretty 
2.adding Done and Delete button based on row checkmarks / DONE!
3.changing the style of Add tasks button / DONE!
4.Searching for notifications 
5.Adding a sqllite Database to my app
6.changing the texts fonts / DONE!
7.make the lottie file for presplash screen
8.Make filters settings 
9.make Prioroty sections in md dialog
10.make one screen to list items like they are listed by : tomarrow,today or ...     
"""
##############