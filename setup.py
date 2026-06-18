from setuptools import find_packages, setup

package_name = 'ros_bumper_serial_reader'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'rclpy',
        'std_msgs',
        'pyserial'
    ],
    zip_safe=True,
    maintainer='bernhard',
    maintainer_email='bernhard-hoerl@gmx.at',
    description='TODO: Package description',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'serial_reader_node = ros_bumper_serial_reader.serial_reader_node:main',
        ],
    },
)
