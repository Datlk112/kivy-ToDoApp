from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from btsh import (
    MDBottomSheet,
    MDBottomSheetDragHandle,
    MDBottomSheetDragHandleButton,
    MDBottomSheetDragHandleTitle,
)
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.pickers import MDDatePicker
import datetime

class DialogContent(MDBoxLayout):
    pass





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

        for button_text in ["Add row", "Remove row"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        # Create a table.
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.48, "center_x": 0.5},
            size_hint=(0.9, 0.71),
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(20)),
                ("Title", dp(30)),
                ("Description", dp(60)),
                ("Due Date", dp(30)),
  
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
            }[instance_button.text]()
        except KeyError:
            pass
        
    def show_confirmation_dialog(self, *args):
        # if not self.dialog:
        #     self.dialog = MDDialog(
        #         title="Address:",
        #         type="custom",
        #         content_cls=MDBoxLayout(
        #             MDTextField(
        #                 id="title",
        #                 hint_text="Title",
        #             ),
        #             MDTextField(
        #                 id="description",
        #                 hint_text="Description",
        #             ),
        #             orientation="vertical",
        #             spacing="12dp",
        #             size_hint_y=None,
        #             height="120dp",
        #         ),
        #         buttons=[
        #             MDFlatButton(
        #                 text="CANCEL",
        #                 theme_text_color="Custom",
        #                 text_color=self.theme_cls.primary_color,
        #                 on_release = lambda x: self.dialog.dismiss()
        #             ),
        #             MDFlatButton(
        #                 text="OK",
        #                 theme_text_color="Custom",
        #                 text_color=self.theme_cls.primary_color,
        #                 on_release = lambda x: self.add_row()
        #             ),
        #         ],
        #     )
        if not self.dialog:
            self.dialog = MDDialog(
                title="Enter Tasks:",
                type="custom",
                content_cls=DialogContent(),
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
            self.dialog.content_cls.ids.Date.text = date_str
        except Exception as e :
            print(f"{e}")
        print(instance, value, date_range)
        print(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass

    def show_calendar(self,*args):
        date_dialog = MDDatePicker(min_date=datetime.date.today(),max_year=2030,title_input="SET DATE",radius=[7, 7, 7, 26],primary_color="purple")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

        
        
    def add_row(self,*args):
        try: 
            title = self.dialog.content_cls.ids.title.text
            Date = self.dialog.content_cls.ids.Date.text
            if self.dialog.content_cls.ids.description.text == "":
                last_num_row = int(self.data_tables.row_data[-1][0])
                self.data_tables.add_row((str(last_num_row + 1), f"{title}", "_" , f"{Date}"))
            else:
                description = self.dialog.content_cls.ids.description.text
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