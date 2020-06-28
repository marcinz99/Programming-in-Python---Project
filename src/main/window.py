import tkinter as tk
from PIL import ImageTk, Image
import threading
import sys
from topic_tree import Device
from datetime import datetime


class Window(threading.Thread):
    """
    Window class
    As self-explaining as it gets, since so far only one window is envisioned
    > Creates new window instance in its own thread
    > Delivers all methods necessary to cooperate with app itself
    """
    # Default window size (px)
    Width = 1080
    Height = 540
    
    def __init__(self, lock, app):
        """
        Not quite the initialization of the window yet
        One have to deal with threading before that
        Actual window has to run in its own thread

        :param lock: reference to the lock initialized in the main app instance
            for the purpose of synchronizing threads during window building
        :param app: reference to the app being window's parent
            > currently not used but perfectly viable for further app development
        """
        # Save received references in case they become usable
        self.lock = lock
        self.higher_lvl = app

        # Acquire the lock
        # Mind that it will prohibit main app instance from doing trespassing the acquire/release obstacle
        # unless all the work here is done
        lock.acquire()

        # New thread initialization for the window
        # Keep in mind that the next operation to be done is the 'run' method
        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        """
        Actual initialization of the window
        Set everything as is meant to be
        Lots of tkinter stuff here obviously

        :return: nothing
        """
        # Icon image dimensions (px); one number since those are squares
        self.img_dim = 30

        # Device references list for internal use only; indexed by dev_id
        self.device_list = []

        # Icon labels list; indexed by dev_id
        self.icons_list = []

        # Device counter to keep up with the indexation of new devices
        self.device_count = 0

        # Empty init of the list of latest actions
        # Ultimately a list of 5 triplets as presented below:
        #  (timestamp, name of device (info field), state of device (state field))
        self.latestList = [None, None, None, None, None]

        # Initialize tkinter root
        self.root = tk.Tk()

        # Set window title
        self.root.wm_title("Smart home")

        # Get the screen dimensions in order to center the window on the screen correctly
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Set the desired window geometry
        self.root.geometry("{}x{}+{}+{}".format(
            Window.Width,
            Window.Height,
            int((screen_width - Window.Width) / 2),
            int((screen_height - Window.Height) / 2)
        ))

        # Prohibit resizing
        self.root.resizable(width=False, height=False)

        # Initialize canvas and pack it so that it fills all the space inside the window
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Basic window closing handler
        self.root.protocol("WM_DELETE_WINDOW", sys.exit)

        # Building up the contents of the window
        self.__addWindowElements()

        # Run the window
        self.root.mainloop()
    
    def on_closing(self, cleanup):
        """
        Extended window closing handler, able to run the passed function

        :param cleanup: handler to be performed when window is being closed
        :return: nothing
        """
        # Local function to encapsulate the handler
        def extended_cleanup():
            """
            Fancy function to run the passed handler and terminate itself when work is done

            :return: nothing
            """
            # Cleanup log (to terminal by default)
            print("Sweep sweep sweep")
            cleanup()
            sys.exit(0)

        # Set the extended cleanup handling
        self.root.protocol("WM_DELETE_WINDOW", extended_cleanup)
        
    def __addWindowElements(self):
        """
        Start up all the visual elements of the window
        It's a dirty job, but someone has to do it

        :return: nothing
        """
        # Initialize the icons for further use
        # Icons will since now will be accessible via reference
        self.icon_switchable_on = ImageTk.PhotoImage(
            Image.open("../img/switchable_on.bmp")
            .resize((self.img_dim, self.img_dim), Image.ANTIALIAS)
        )
        self.icon_switchable_off = ImageTk.PhotoImage(
            Image.open("../img/switchable_off.bmp")
            .resize((self.img_dim, self.img_dim), Image.ANTIALIAS)
        )
        self.icon_detector_excited = ImageTk.PhotoImage(
            Image.open("../img/detector_excited.bmp")
            .resize((self.img_dim, self.img_dim), Image.ANTIALIAS)
        )
        self.icon_detector_idle = ImageTk.PhotoImage(
            Image.open("../img/detector_idle.bmp")
            .resize((self.img_dim, self.img_dim), Image.ANTIALIAS)
        )

        # House overview frame's size
        plan_width, plan_height = 770, 540

        # Current device preview frame's size
        current_width, current_height = Window.Width - plan_width, 100

        # Info frame's size
        info_width, info_height = current_width, 40

        # Latest actions frame's size
        latest_width = current_width
        latest_height = (Window.Height - current_height - info_height)/5

        # House overview frame initialization and localization
        plan_frame = tk.Frame(self.canvas, width=plan_width,
                              height=plan_height, padx=8, pady=8, bg="#FFC856")
        plan_frame.grid(row=0, column=0)

        # News feed (whole right column) frame initialization and localization
        self.newsfeed = tk.Frame(self.canvas)
        self.newsfeed.grid(row=0, column=1)

        # Rendering house overview from file and its localization
        render = ImageTk.PhotoImage(Image.open("../config/home_plan.bmp"))
        self.plan = tk.Label(plan_frame, image=render, bd=2, bg="#000000")
        self.plan.image = render
        self.plan.place(x=0, y=0)

        # ====
        # Current device preview
        # ====
        self.current = tk.Frame(self.newsfeed, width=current_width, height=current_height,
                                pady=8, bg="#FFC856")
        self.current.grid(row=0, column=0)

        # "c_*" elements are the components of current device preview frame
        # Inner frame
        self.c_frame = tk.Frame(self.current, width=current_width,
                                height=current_height-16, bg="#FFF5D7")
        self.c_frame.pack()
        self.c_frame.pack_propagate(False)

        # Device name label
        self.c_label_name = tk.Label(self.c_frame, text="Device preview",
                                     font=("Consolas", 12), justify=tk.LEFT, bg="#FFDD2C")
        self.c_label_name.pack(anchor="w")

        # Device description label (state of the device)
        self.c_label_desc = tk.Label(self.c_frame, text="Click a device on the screen", pady=8, padx=3,
                                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFF5D7")
        self.c_label_desc.pack(anchor="w")

        # ====
        # Info label frame
        # Header for the latest actions frame
        # ====
        info = tk.Frame(self.newsfeed, width=info_width, height=info_height, bg="#FDFEEC")
        info.grid(row=1, column=0)
        info.pack_propagate(False)
        info_label = tk.Label(info, text="Latest actions:", bg="#FDFEEC", pady=10,
                              font=("Consolas", 14), anchor=tk.CENTER, justify=tk.CENTER)
        info_label.pack()
        info.grid(row=1, column=0)

        # ====
        # Latest actions preview
        # ====
        self.latest = [
            tk.Frame(self.newsfeed, width=latest_width, height=latest_height, bg="#FFEAAA"),
            tk.Frame(self.newsfeed, width=latest_width, height=latest_height, bg="#FFF5D7"),
            tk.Frame(self.newsfeed, width=latest_width, height=latest_height, bg="#FFEAAA"),
            tk.Frame(self.newsfeed, width=latest_width, height=latest_height, bg="#FFF5D7"),
            tk.Frame(self.newsfeed, width=latest_width, height=latest_height, bg="#FFEAAA")
        ]
        self.latest[0].grid(row=2, column=0)
        self.latest[1].grid(row=3, column=0)
        self.latest[2].grid(row=4, column=0)
        self.latest[3].grid(row=5, column=0)
        self.latest[4].grid(row=6, column=0)

        for i in range(5):
            self.latest[i].pack_propagate(False)

        # Latest actions timestamp labels' initialization and their localization
        self.l_timestamp = [
            tk.Label(self.latest[0], text="No actions to be shown", pady=0, padx=5,
                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFDD2C"),
            tk.Label(self.latest[1], text="", pady=0, padx=5,
                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFF5D7"),
            tk.Label(self.latest[2], text="", pady=0, padx=5,
                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFEAAA"),
            tk.Label(self.latest[3], text="", pady=0, padx=5,
                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFF5D7"),
            tk.Label(self.latest[4], text="", pady=0, padx=5,
                     font=("Consolas", 11), justify=tk.LEFT, bg="#FFEAAA")
        ]
        for i in range(5):
            self.l_timestamp[i].pack(anchor="w")

        # Latest actions info labels' initialization and their localization
        self.l_info = [
            tk.Label(self.latest[i], text="", pady=0, padx=5, font=("Consolas", 11),
                     justify=tk.LEFT, bg=("#FFF5D7" if i & 1 else "#FFEAAA"))
            for i in range(5)
        ]
        for i in range(5):
            self.l_info[i].pack(anchor="w")

        # Latest actions state labels' initialization and their localization
        self.l_state = [
            tk.Label(self.latest[i], text="", pady=0, padx=5, font=("Consolas", 11),
                     justify=tk.LEFT, bg=("#FFF5D7" if i & 1 else "#FFEAAA"))
            for i in range(5)
        ]
        for i in range(5):
            self.l_state[i].pack(anchor="w")

        # Release the lock, critical section is over
        self.lock.release()
        
    def addDevice(self, device):
        """
        Add the device to the window
        Instantiate new icon on the house overview

        :param device: reference to device instance
        :return: dev_id - integer device id
        """
        # Synchronization: acquire
        self.lock.acquire()

        # Get next free id for the new device and increment the device counter
        dev_id = self.device_count
        self.device_count += 1

        # Frame for the new icon
        this_dev = tk.Frame(self.plan, width=self.img_dim + 2, height=self.img_dim + 2)
        this_dev.pack_propagate(False)

        # Label for the new icon
        img_label = tk.Label(this_dev, bd=1, bg="#000000")
        img_label.bind("<Button-1>", lambda event: self.updateCurrent(device))
        self.icons_list += [img_label]

        # Set the right icon according to the actual type of device and its state
        self.setIcon(dev_id, device.dev_type, 0)

        # Pack image label
        img_label.pack()

        # Update the device list accordingly
        self.device_list += [this_dev]

        # Place the newly established frame on the house overview
        this_dev.place(x=device.x_pos, y=device.y_pos)

        # Synchronization: release
        self.lock.release()

        # Return the id of just registered device
        return dev_id
    
    def setIcon(self, id, type, state):
        """
        Setting and changing the icons of the devices

        :param id: device id
        :param type: device type
        :param state: newly reached state
        :return: nothing
        """
        # Handle switchables
        if type == Device.Switchable:
            if state == Device.States_Switchable.OFF:
                self.icons_list[id].configure(image=self.icon_switchable_off)
            if state == Device.States_Switchable.ON:
                self.icons_list[id].configure(image=self.icon_switchable_on)

        # Handle detectors
        elif type == Device.Detector:
            if state == Device.States_Detector.IDLE:
                self.icons_list[id].configure(image=self.icon_detector_idle)
            if state == Device.States_Detector.EXCITED:
                self.icons_list[id].configure(image=self.icon_detector_excited)
    
    def updateLatestList(self, device):
        """
        Update the list of latest actions

        :param device: reference to the device that caused some action
        :return: nothing
        """
        # Get the time for the timestamp
        now = datetime.now()

        # Pack the timestamp, device info and its state into one triplet
        actu = (now.__str__(), device.info, device.state)

        # Update the list of latest actions
        # Get rid of the oldest action, and place new tuple at the beginning
        self.latestList = [actu] + self.latestList[:4]

        # Iterate through tuples on the latest actions list
        for i, bundle in enumerate(self.latestList):
            # If initialized, then:
            if bundle:
                # Unpack the triplet and make use of those data
                timestamp, info, state = bundle
                self.l_timestamp[i].config(text=timestamp)
                self.l_info[i].config(text="Device:\t" + info)
                self.l_state[i].config(text="State: \t" + state)

            # Mind that by default 'bundle' is set to None meaning no actions to be recorded
            else:
                # Report that there are no more actions in the recorded history
                # If so, there's no point in further iterations
                self.l_timestamp[i].config(bg="#FFDD2C")
                self.l_timestamp[i].config(text="No more actions to be shown")
                break
    
    def updateCurrent(self, device):
        """
        Update the info about the lately clicked device

        :param device: reference to the device clicked
        :return: nothing
        """
        # Show info about the chosen device in current device frame label
        self.c_label_name.config(text=device.info)
        self.c_label_desc.config(text="State: \t" + device.state)
