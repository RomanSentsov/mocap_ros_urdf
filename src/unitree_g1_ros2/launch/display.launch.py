import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Получаем директорию пакета
    bringup_dir = get_package_share_directory('unitree_g1_ros2')
    
    # Переменные конфигурации запуска
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    urdf_file = LaunchConfiguration('urdf_file')

    # --- 1. КОНСТАНТА ДЛЯ КАСТОМНОГО ТОПИКА ---
    # Поменяйте строку ниже на нужное вам название топика
    CUSTOM_JOINT_STATES_TOPIC = "/unitree_noitom_teleop/arms_waist_cmd" 

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        'rviz_config_file',
        default_value=os.path.join(bringup_dir, 'rviz', 'rviz.rviz'),
        description='Full path to the RVIZ config file to use')
        
    declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
        'use_robot_state_pub',
        default_value='True',
        description='Whether to start the robot state publisher')
        
    declare_use_rviz_cmd = DeclareLaunchArgument(
        'use_rviz',
        default_value='True',
        description='Whether to start RVIZ')

    declare_urdf_cmd = DeclareLaunchArgument(
        'urdf_file',
        default_value=os.path.join(bringup_dir, 'urdf', 'g1_29dof_with_hand_rev_1_0.urdf'),
        description='URDF file path')

    start_robot_state_publisher_cmd = Node(
        condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        arguments=[urdf_file],
        # --- 2. ПЕРЕНАЗНАЧЕНИЕ (REMAPPING) НА КАСТОМНЫЙ ТОПИК ---
        remappings=[
            ('/joint_states', CUSTOM_JOINT_STATES_TOPIC)
        ]
    )

    # --- 3. УЗЕЛ joint_state_publisher_gui ПОЛНОСТЬЮ УДАЛЕН ---

    rviz_cmd = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen')

    # Создаем и заполняем LaunchDescription
    ld = LaunchDescription()

    # Добавляем аргументы запуска
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_urdf_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)
    ld.add_action(declare_use_rviz_cmd)

    # Добавляем ноды (только robot_state_publisher и rviz)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(rviz_cmd)

    return ld
