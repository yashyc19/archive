import tkinter
import os
import tkinter.messagebox
import tkinter.filedialog as filedialog
import customtkinter
import sys
from PIL import Image

from Tasks.task_login import LoginTask
from Tasks.task_portal_availability import Task_Portal_Availability
from Tasks.task_check_arn_status import Task_ARN_Status


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Use the current working directory for development
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        # configure window
        self.title("ABOP Tool (Additional Places of Business)")
        self.geometry(f"{950}x{580}")
        self.iconbitmap(resource_path("icon.ico"))


        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Load the image using PIL
        logo_path = resource_path("deloittelogo.jpg")
        self.logo_image = customtkinter.CTkImage(Image.open(logo_path), size=(140, 70))
        self.logo_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, anchor="center", text="")
        self.logo_image_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="APOB Tool", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=400)
        self.tabview.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="nsew")
        self.tabview.add("Track ARN Status")
        self.tabview.add("Portal Availability")
        self.tabview.add("Add places of business")
        self.tabview.tab("Track ARN Status").grid_columnconfigure([0, 1, 2, 3], weight=1)
        self.tabview.tab("Portal Availability").grid_columnconfigure([0], weight=1) 
        self.tabview.tab("Add places of business").grid_columnconfigure([0], weight=1)
        

        # create availability tab
        self.availability_excel_path = customtkinter.CTkEntry(self.tabview.tab("Portal Availability"), placeholder_text="Upload login excel file")
        self.availability_excel_path.grid(row=0, column=0, columnspan=3, padx=(20, 10), pady=(30, 20), sticky="ew")  # Adjust the sticky parameter to "ew" to make it full width
        self.upload_availability_excel = customtkinter.CTkButton(self.tabview.tab("Portal Availability"), text="Upload", command=lambda: self.upload_file_event("availability"))
        self.upload_availability_excel.grid(row=0, column=3, padx=(10, 20), pady=(30, 20))

        self.run_portal_availability = customtkinter.CTkButton(self.tabview.tab("Portal Availability"), text="Run availability check", command=self.call_availability_task)
        self.run_portal_availability.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=5)
        self.run_portal_availability.configure(width=20)
        self.run_portal_availability.configure(font=("Helvetica", 16))


        # create track arn status tab
        self.arn_excel_path = customtkinter.CTkEntry(self.tabview.tab("Track ARN Status"), placeholder_text="Upload ARN excel list")
        self.arn_excel_path.grid(row=0, column=0, columnspan=3, padx=(20, 10), pady=(30, 20), sticky="ew")  # Adjust the sticky parameter to "ew" to make it full width
        self.upload_arn_excel = customtkinter.CTkButton(self.tabview.tab("Track ARN Status"), text="Upload", command=lambda: self.upload_file_event("arn"))
        self.upload_arn_excel.grid(row=0, column=3, padx=(10, 20), pady=(30, 20))

        self.run_arn_status_check = customtkinter.CTkButton(self.tabview.tab("Track ARN Status"), text="Track ARN Status", command=self.call_arn_task)
        self.run_arn_status_check.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=5)
        self.run_arn_status_check.configure(width=20)
        self.run_arn_status_check.configure(font=("Helvetica", 16))


        # create APOB tab
        self.apob_excel_path = customtkinter.CTkEntry(self.tabview.tab("Add places of business"), placeholder_text="Upload APOB excel file")
        self.apob_excel_path.grid(row=1, column=0, columnspan=3, padx=(20, 10), pady=(20, 10), sticky="ew")

        self.upload_apob_excel = customtkinter.CTkButton(self.tabview.tab("Add places of business"), text="Upload", command=lambda: self.upload_file_event("apob"))
        self.upload_apob_excel.grid(row=1, column=3, padx=(10, 20), pady=(20, 10))

        self.run_arn_status_check = customtkinter.CTkButton(self.tabview.tab("Add places of business"), text="Add places of business", command=self.call_apob_task)
        self.run_arn_status_check.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=5)
        self.run_arn_status_check.configure(width=20)
        self.run_arn_status_check.configure(font=("Helvetica", 16))


        
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=200)
        self.textbox.grid(row=0, column=2, padx=(10, 20), pady=20, sticky="nsew")

        # set default settings
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def upload_file_event(self, task: str):
        if task == "availability":
            self.handle_upload(self.availability_excel_path)
        elif task == "arn":
            self.handle_upload(self.arn_excel_path)
        elif task == "apob":
            self.handle_upload(self.apob_excel_path)
        else:
            raise Exception("Invalid task")

    def handle_upload(self, file_path_entry):
        # Open a file dialog and allow the user to select a file to upload
        file_path_entry.delete(0, 'end')
        file_path = customtkinter.filedialog.askopenfilename()

        # Do something with the selected file
        file_path_entry.insert(0, file_path)
    
    def update_textbox(self, text: str):
        self.textbox.delete('0.0', 'end')
        self.textbox.insert('0.0', text)

    # selenium scripts triggers (test commands)
    def call_availability_task(self):
        # availability_command = "pytest Tests/test_4_check_submission_status.py"
        # os.system(availability_command)
        # driver = LoginTask.init_driver()
        self.update_textbox("Running availability check...")
        portal_file_path = self.availability_excel_path.get()
        if not portal_file_path:
            self.update_textbox("No file uploaded. Please upload a file.")
            return
        self.update_textbox(f"Selected file: {os.path.basename(portal_file_path)}")
        portal_task = Task_Portal_Availability(portal_file_path)
        try:
            portal_task.task_portal_availability()
        except Exception as e:
            portal_task.driver.quit()
            self.update_textbox(f"Error in function '{self.call_availability_task.__name__}': {str(e)}")
            return
        self.update_textbox("Availability check completed.")
        

    def call_arn_task(self):
        self.update_textbox("Running ARN status check...")
        arn_file_path = self.arn_excel_path.get()
        if not arn_file_path:
            self.update_textbox("No file uploaded. Please upload a file.")
            return
        self.update_textbox(f"Selected file: {os.path.basename(arn_file_path)}")
        arn_task = Task_ARN_Status(arn_file_path)
        try:
            arn_task.arn_status()
        except Exception as e:
            arn_task.driver.quit()
            self.update_textbox(f"Error in function '{self.call_arn_task.__name__}': {str(e)}")
            return
        self.update_textbox("ARN status check completed.")


    def call_apob_task(self):
        self.update_textbox("This feature is currently unavailable.")
        # apob_command = "pytest Tests/test_2_adding_places_of_business.py"
        # os.system(apob_command)
        # self.update_textbox("APOB check completed.")
        # username = self.apob_username_entry.get()
        # password = self.apob_password_entry.get()

        # login_task = LoginTask()
        # login_task.task_loginpage(username, password)

        
        

# def main():
#     app = App()
#     app.mainloop()


# if __name__ == "__main__":
#     main()


# create an executible file
# pyinstaller --name PDFTool --onefile --windowed --noconsole --icon=icon.ico pdftool.py