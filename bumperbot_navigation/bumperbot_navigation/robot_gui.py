#!/usr/bin/env python3
import rclpy
from robot_interfaces.msg import RobotDestination, RobotPose
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from rclpy.node import Node
import tkinter as tk
import threading



class SimpleCommanderNode(Node):
    def __init__(self):
        super().__init__('simple_commander_node')

        # GUI INITIALIZATION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # GUI INITIALIZATION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.pose = PoseStamped()
        self.nav = BasicNavigator() # this initialization creates /amcl_pose and /initialpose topics.
                                    # /initialpose topic can be initialized with .setInitialPose() function and can be monitored
                                    # by ros2 topic echo /initialpose (published once)

        # Reserved for notes -----------------------------------------------------------------------------------
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # End of notes ---------------------------------------------------------------------------------------

        self.publisher_ = self.create_publisher(PoseStamped, 'robot_destination',10)
        self.pose_initializer = self.create_subscription(RobotPose, 'robot_initial_pose', self.pose_callback, 10)

        self.gui_thread = threading.Thread(target=self.run_gui, daemon=True)
        self.gui_thread.start()


    def pose_callback(self, msg):
        self.pose.header.frame_id = "map"
        self.pose.header.stamp = self.get_clock().now().to_msg()
        self.pose.pose.position.x = msg.x
        self.pose.pose.position.y = msg.y
        self.pose.pose.orientation.z = 0.0


        self.nav.setInitialPose(self.pose)
        self.publisher_.publish(self.pose) 

        self.destroy_subscription(self.pose_initializer)

    def run_gui(self):
        name = "MyGUI"
        size = "500x400"

        self.root = tk.Tk()
        self.root.title(name)
        self.root.geometry(size)
        self.root.minsize(width='300', height='300')

        self.move_label = ""
        self.x_coord = 0.0
        self.y_coord = 0.0


        label = tk.Label(self.root, text="Mobile Robot Controller UI", font=('Arial', 24), background="lightgreen", height=2)
        label.pack(fill='both')

        label = tk.Label(self.root, height=2)
        label.pack(fill='both')

        # Main frame with two equal columns
        pageFrame = tk.Frame(self.root, padx=10, pady=10)
        pageFrame.pack(fill='both', expand=True)
        pageFrame.columnconfigure(0, weight=1)  # Left column weight
        pageFrame.columnconfigure(1, weight=1)  # Right column weight
        
        # Left frame (contains a grid)
        leftFrame = tk.Frame(pageFrame)
        leftFrame.grid(row=0, column=0, sticky="nsew")
        leftFrame.columnconfigure(0, weight=1)
        leftFrame.rowconfigure(0, weight=1)

        # Right frame (dummy frame to balance layout)
        rightFrame = tk.Frame(pageFrame, width='2')
        rightFrame.grid(row=0, column=1, sticky="esn")

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BUTTON FRAME

        # Button Frame inside the left frame (3x3 grid)
        buttonFrame = tk.Frame(leftFrame, width='12')
        buttonFrame.grid(row=0, column=0, sticky="w")
        
        # Configure button frame to allow proper resizing
        for i in range(3):  
            buttonFrame.columnconfigure(i, weight=1, minsize=50)  # Evenly distribute columns
            buttonFrame.rowconfigure(i, weight=1, minsize=50)     # Evenly distribute rows

        # Adding buttons
        btnUp = tk.Button(buttonFrame, text='U', height=2, width=4 ,font=('Arial', 18), bg='lightgreen', command=self.btn_up_function)
        btnUp.grid(row=0, column=1, sticky="nsew")

        btnLeft = tk.Button(buttonFrame, text='L', height=2, width=4, font=('Arial', 18), bg='lightgreen', command=self.btn_left_function)
        btnLeft.grid(row=1, column=0, sticky="nsew")

        btnRight = tk.Button(buttonFrame, text='R', height=2, width=4, font=('Arial', 18), bg='lightgreen', command=self.btn_right_function)
        btnRight.grid(row=1, column=2, sticky="nsew")

        btnDown = tk.Button(buttonFrame, text='D', height=2, width=4,font=('Arial', 18), bg='lightgreen', command=self.btn_down_function)
        btnDown.grid(row=2, column=1, sticky="nsew")

        
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Coordinate Frame



        coordinate_frame_label = tk.Label(rightFrame, text="Destination Coordinates", font=('Arial', 16), background="lightblue")
        coordinate_frame_label.grid(row=0, column=0)
        
        cord_frame = tk.Frame(rightFrame, padx=0, pady=0)
        cord_frame.grid(row=1, column=0, sticky='w')
        cord_frame.columnconfigure(0, weight=1)
        cord_frame.columnconfigure(1, weight=10)


        x_label = tk.Label(cord_frame, text="X:", height=1, width=4, font=('Arial', 16))
        x_label.grid(row=0, column=0, sticky='w')
        y_label = tk.Label(cord_frame, text="Y:", height=1, width=4, font=('Arial', 16))
        y_label.grid(row=1, column=0, sticky='w')
        self.textbox_x = tk.Text(cord_frame, height=1, width=14, font=('Arial',16), bg="white")
        self.textbox_x.grid(row=0, column=1, sticky='e')
        self.textbox_y = tk.Text(cord_frame, height=1, width =14, font=('Arial',16), bg='white')
        self.textbox_y.grid(row=1, column=1, sticky='e')

        textbox_situation = tk.Text(cord_frame, height=1, width=10, font=('Arial',16))
        textbox_situation.grid(row=2, column=0)
        btnMove = tk.Button(cord_frame, text="Move", height=2, width=8, font=('Arial', 16), command=self.btn_move_function)
        btnMove.grid(row=2, column=1, sticky='e')
        
        self.root.mainloop()

    def btn_up_function(self):
        print('Pressed button up')
        self.x_coord += 0.5
        self.delete_text(self.textbox_x)
        self.textbox_x.insert('1.0', str(self.x_coord))
    def btn_left_function(self):
        print('Pressed button left')
        self.y_coord -= 0.5
        self.delete_text(self.textbox_y)
        self.textbox_y.insert('1.0', str(self.y_coord))
    def btn_right_function(self):
        print('Pressed button right')
        self.y_coord += 0.5
        self.delete_text(self.textbox_y)
        self.textbox_y.insert('1.0', str(self.y_coord))
    def btn_down_function(self):
        print('Pressed button down')
        self.x_coord -= 0.5
        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.close_app)
        self.quit_button.pack()
        self.delete_text(self.textbox_x)
        self.textbox_x.insert('1.0', str(self.x_coord))

    def btn_move_function(self, text):
        text.delete('1.0', 'end')
        self.move_label = str('x: ' + str(self.x_coord) + 'y: ' + str(self.y_coord))
        text.insert('1.0', self.move_label)
        self.delete_text(self.textbox_x)
        self.delete_text(self.textbox_y)

    def delete_text(self, text):
        text.delete('1.0', 'end')

        
            
        
def main(args=None):
    rclpy.init(args=args)
    node = SimpleCommanderNode()
    
    # Run ROS2 event loop without blocking
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
