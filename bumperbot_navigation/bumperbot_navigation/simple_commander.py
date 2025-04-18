#!/usr/bin/env python3
import rclpy
from robot_interfaces.msg import RobotDestination, RobotPose
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from nav2_simple_commander.robot_navigator import BasicNavigator
from rclpy.node import Node
import tkinter as tk
import threading

class RobotGUI:
    """Handles the Tkinter GUI."""
    def __init__(self, ros_node, name, size="600x400"):
        self.ros_node = ros_node

        self.root = tk.Tk()
        self.root.title(name)
        self.root.minsize(width=600, height=400)
        self.root.geometry(size) 


        self.move_label = ""
        self.x_coord = 0.0
        self.y_coord = 0.0

        self.destination_x = 0.0
        self.destination_y = 0.0

        label = tk.Label(self.root, text="Mobile Robot Controller UI", font=('Arial', 24), background="lightgreen", height=2)
        label.pack(fill='both')
        label = tk.Label(self.root, height=2)
        label.pack(fill='both')

        # Main frame with two equal columns
        pageFrame = tk.Frame(self.root, padx=10, pady=10)
        pageFrame.pack(fill='both', expand=True)
        pageFrame.columnconfigure(0, weight=1, minsize=250)  # Left column weight
        pageFrame.columnconfigure(1, weight=1, minsize=250)  # Right column weight
        
        # Left frame (contains a grid)
        leftFrame = tk.Frame(pageFrame)
        leftFrame.grid(row=0, column=0, sticky="nsew")
        leftFrame.columnconfigure(0, weight=1)
        leftFrame.rowconfigure(0, weight=1)

        # Right frame (dummy frame to balance layout)
        rightFrame = tk.Frame(pageFrame, width='2')
        rightFrame.grid(row=0, column=1, sticky="esn")
        rightFrame.rowconfigure(2, minsize=40) 
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BUTTON FRAME
        # Button Frame inside the left frame (3x3 grid)
        buttonFrame = tk.Frame(leftFrame, width='12')
        buttonFrame.grid(row=0, column=0, sticky="w")
    
        # Configure button frame to allow proper resizing
        for i in range(3):  
            buttonFrame.columnconfigure(i, weight=1, minsize=50)  # Evenly distribute columns
            buttonFrame.rowconfigure(i, weight=1, minsize=50)     # Evenly distribute rows
        # Adding buttons
        btnUp = tk.Button(buttonFrame,name='button_up', text='U', height=2, width=4,
                  font=('Arial', 18), bg='lightgreen',
                  command=lambda: self.btn_up_function('button_up'))
        btnUp.grid(row=0, column=1, sticky="nsew")
        btnLeft = tk.Button(buttonFrame, name="button_left", text='L', height=2, width=4,
                  font=('Arial', 18), bg='lightgreen',
                  command=lambda: self.btn_up_function('button_left'))
        btnLeft.grid(row=1, column=0, sticky="nsew")
        btnRight = tk.Button(buttonFrame, name="button_right", text='R', height=2, width=4, font=('Arial', 18), bg='lightgreen', 
                             command=lambda: self.btn_right_function('button_right'))
        btnRight.grid(row=1, column=2, sticky="nsew")
        btnDown = tk.Button(buttonFrame, name="button_down", text='D', height=2, width=4,font=('Arial', 18), bg='lightgreen', 
                            command=lambda: self.btn_down_function('button_down'))
        btnDown.grid(row=2, column=1, sticky="nsew")

        
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@ Coordinate Frame
        coordinate_frame_label = tk.Label(rightFrame, text="Destination Coordinates", font=('Arial', 16), background="lightblue", anchor='w')
        coordinate_frame_label.grid(row=0, column=0, sticky='eswn')
        cord_frame = tk.Frame(rightFrame, padx=0, pady=0, bg="")
        cord_frame.grid(row=1, column=0, sticky='w')
        cord_frame.columnconfigure(0, weight=1)
        cord_frame.columnconfigure(1, weight=10)
        cord_frame.rowconfigure(0, weight=1)
        cord_frame.rowconfigure(1, weight=1)
        x_label = tk.Label(cord_frame, text="X:", height=1, width=3, font=('Arial', 14))
        x_label.grid(row=0, column=0, sticky='w')
        y_label = tk.Label(cord_frame, text="Y:", height=1, width=3, font=('Arial', 14))
        y_label.grid(row=1, column=0, sticky='w')
        self.textbox_x = tk.Text(cord_frame, height=1, width=10, font=('Arial',14), bg="white", exportselection=0)
        self.textbox_x.grid(row=0, column=1, sticky='wsne')
        self.textbox_y = tk.Text(cord_frame, height=1, width =10, font=('Arial',14), bg='white')
        self.textbox_y.grid(row=1, column=1, sticky='wsne')
        btnMove = tk.Button(cord_frame, text="Move", height=2, width=8, font=('Arial', 16), command= self.btn_move_function)
        btnMove.grid(row=0, column=2, sticky='e', rowspan=2)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Button Frame
        position_frame_label = tk.Label(rightFrame, text="Robot Position", font=('Arial', 16), background="lightblue", anchor='w')
        position_frame_label.grid(row=3, column=0, columnspan=2, sticky='snew')
        position_frame = tk.Frame(rightFrame, padx=0, pady=0, bg="")
        position_frame.grid(row=4, column=0, sticky='snew')
        position_frame.columnconfigure(0, weight=1)
        position_frame.columnconfigure(1, weight=10)
        x_label = tk.Label(position_frame, text="X:", height=1, width=3, font=('Arial', 14))
        x_label.grid(row=0, column=0, sticky='w')
        y_label = tk.Label(position_frame, text="Y:", height=1, width=3, font=('Arial', 14))
        y_label.grid(row=1, column=0, sticky='w')
        self.pos_x_text = tk.Text(position_frame, height=1, width=10, font=('Arial',14), bg="white", cursor="arrow", state='disabled')
        self.pos_x_text.grid(row=0, column=1, sticky='w')
        self.pos_y_text = tk.Text(position_frame, height=1, width =10, font=('Arial',14), bg='white',cursor="arrow", state='disabled')
        self.pos_y_text.grid(row=1, column=1, sticky='w')

    def btn_up_function(self, button):
        self.destination_x += 0.1
        self.delete_text(self.textbox_x)
        self.textbox_x.insert('1.0', str(self.destination_x))
        self.movement(button)
    def btn_down_function(self, button):
        self.destination_x -= 0.1
        self.delete_text(self.textbox_x)
        self.textbox_y.insert('1.0', str(self.destination_x))
        self.movement(button)
    def btn_right_function(self, button):
        self.destination_y += 0.1
        self.delete_text(self.textbox_y)
        self.textbox_y.insert('1.0', str(self.destination_y))
        self.movement(button)
    def btn_left_function(self, button):
        self.destination_y -= 0.1
        self.delete_text(self.textbox_y)
        self.textbox_y.insert('1.0', str(self.destination_y))
        self.movement(button)

    def movement(self, button: tk.Button):
        print('Pressed the button:' + button)

    def update_robot_position(self, x, y):
        print ("hi x:" + str(x) + " y:" + str(y))
        self.pos_x_text.configure(state='normal')
        self.pos_y_text.configure(state='normal')
        self.delete_text_box(self.pos_x_text)
        self.delete_text_box(self.pos_y_text)
        self.write_to_text_box(self.pos_x_text, str(x))
        self.write_to_text_box(self.pos_y_text, str(y))
        self.pos_x_text.configure(state='disabled')
        self.pos_y_text.configure(state='disabled')

    def write_to_text_box(self, textbox, message):
        # to write a message to a disabled textbox, reconfigure it to normal and disable it
        textbox.configure(state='normal')
        self.delete_text_box(textbox)
        textbox.insert('1.0', message)
        textbox.configure(state='disabled')

    def delete_text_box(self, textbox):
        textbox.configure(state='normal')
        textbox.delete('1.0', 'end')
        textbox.configure(state='disabled')

    def btn_move_function(self): 
        self.delete_text_box(self.pos_x_text)
        message = str('x:' + self.textbox_x.get('1.0', 'end-1c') + ' y:' + self.textbox_y.get('1.0', 'end-1c'))
        self.write_to_text_box(self.pos_x_text, message)
        self.textbox_x.delete('1.0', 'end')
        self.textbox_y.delete('1.0', 'end')
        print(message)

    # def btn_move_function(self):
    #     message = RobotPose()
    #     message.x = self.x_coord
    #     message.y = self.y_coord
    #     message.theta = 0.0
    #     self.ros_node.send_pose(message)

    def delete_text(self, text):
        text.delete('1.0', 'end')

    def run(self):
        """Starts the Tkinter event loop."""
        self.gui_thread = threading.Thread(target=self.root.mainloop, daemon=True)
        self.gui_thread.start()

class SimpleCommanderNode(Node):
    def __init__(self):
        super().__init__('simple_commander_node')

        self.gui = RobotGUI(self, "myGui")
        self.pose = PoseStamped()
        self.nav = BasicNavigator() # this initialization creates /amcl_pose and /initialpose topics.
                                    # /initialpose topic can be initialized with .setInitialPose() function and can be monitored
                                    # by ros2 topic echo /initialpose (published once)
        
        self.pose_subscription = self.create_subscription(String, 'pose_pose', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(PoseStamped, 'robot_destination',10)
        self.number_publisher_ = self.create_publisher(String, 'number_publisher', 10)
        # self.pose_initializer = self.create_subscription(RobotPose, 'robot_initial_pose', self.pose_callback, 10)

        self.gui.update_robot_position(4.2, 3.5)

        # self.nav.waitUntilNav2Active()
       
        self.gui.run();


    def listener_callback(self, msg):
        string = String()
        string.data = msg.data
        self.number_publisher_.publish(string)
        self.get_logger().info('I heard: "%s"' % msg.data)
        # self.gui.update_robot_position(msg.pose.position.x, msg.pose.position.y)
        # self.gui.update_robot_position(msg.x, msg.y)


    def pose_callback(self, msg):
        self.pose.header.frame_id = "map"
        self.pose.header.stamp = self.get_clock().now().to_msg()
        self.pose.pose.position.x = msg.x
        self.pose.pose.position.y = msg.y
        self.pose.pose.orientation.z = 0.0

        self.nav.setInitialPose(self.pose)
        self.publisher_.publish(self.pose) 

        self.destroy_subscription(self.pose_initializer)


    def send_pose(self, msg: RobotPose):
        destination = PoseStamped()
        destination.header.frame_id = "map"
        destination.header.stamp = self.get_clock().now().to_msg()
        destination.pose.position.x = msg.x
        destination.pose.position.y = msg.y
        destination.pose.orientation.z = msg.theta
        self.nav.goToPose(destination)
        self.get_logger().info("Robot pose has been sent")

    def send_number(self, string):
        message = String()
        message._data = str(string)
        self.number_publisher_.publish(message)

            
        
def main(args=None):
    rclpy.init(args=args)
    node = SimpleCommanderNode()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
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
