"""
    A simple program made to control the IP cameras using the IPCAM CGI SDK 2.1
"""

import argparse
import logging
import os
import sys
import time
import webbrowser
import pygame
import pygame.locals as pylocals
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def show_banner():
    """
    Clears the console and shows the program's banner.

    :return:
        None
    """
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith("linux") or \
            sys.platform.startswith("darwin") or \
            sys.platform.startswith("darwin"):
        os.system("clear")
    print(r" __      __  ______  __       __       ____      ")
    print(r"/\ \  __/\ \/\  _  \/\ \     /\ \     /\  _`\    ")
    print(r"\ \ \/\ \ \ \ \ \L\ \ \ \    \ \ \    \ \ \L\_\  ")
    print(r" \ \ \ \ \ \ \ \  __ \ \ \  __\ \ \  __\ \  _\L  ")
    print(r"  \ \ \_/ \_\ \ \ \/\ \ \ \L\ \\ \ \L\ \\ \ \L\ \\ ")
    print(r"   \ `\___x___/\ \_\ \_\ \____/ \ \____/ \ \____/")
    print(r"    '\/__//__/  \/_/\/_/\/___/   \/___/   \/___/ ")
    print("\n\n")


def get_video(user: str, password: str, address: str, port: str):
    """
    Opens a web browser page displaying the video stream of the IP camera.

    :param user: The username of the IP camera
    :param password: The password of the provided user
    :param address: The IP address of the IP camera
    :param port: The TCP port used by the IP camera
    :return:
        None
    """
    print("[*] Starting video stream...")
    logging.debug("Starting video stream...")

    url = ("http://" + address + ":" + port + "/videostream.cgi?user=" + user + "&pwd=" + password)
    webbrowser.open(url, new=2, autoraise=False)
    show_menu(user, password, address, port)


def reboot(address: str, port: str):
    """
    Sends a HTTP GET request to reboot the IP camera.

    :param address: The IP address of the IP camera
    :param port: The TCP port used by the IP camera
    :return:
        None
    """
    url = ("http://" + address + ":" + port + "/reboot.cgi?")
    requests.get(url, headers=HEADERS)


def show_menu(user: str, password: str, address: str, port: str):
    """
    Displays the program's menu.

    :param user: The user of the IP camera
    :param password: The password of the provided user
    :param address: The IP address of the IP camera
    :param port: The TCP port used by the IP camera
    :return:
        None
    """
    show_banner()

    print("MENU\n")
    print("1-Control webcam")
    print("2-Reboot webcam")
    print("3-Quit program")

    menu = str(input("> "))

    if menu == "1":
        control(user, password, address, port)
    elif menu == "2":
        reboot(address, port)
    elif menu == "3":
        sys.exit(0)


def control(user: str, password: str, address: str, port: str):
    """
    Allows the user to move the IP camera using WASD (QWERTY keyboard),
    to take a screenshot using the space bar, and to quit the program using the escape key.

    :param user: The user og the IP camera
    :param password: The password of the provided user
    :param address: The IP address of the IP camera
    :param port: The TCP port used by the IP camera
    :return:
        None
    """
    running = True
    black = (0, 0, 0)
    width = 1
    height = 1

    pygame.quit()
    pygame.init()

    response = None
    url = None

    windowsurface = pygame.display.set_mode((width, height), pygame.NOFRAME)
    windowsurface.fill(black)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pylocals.K_SPACE:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/snapshot.cgi?user=" + user +
                                       "&pwd=" + password)
                    logging.debug("Space pressed : %s", url)
                elif event.key == pylocals.K_w:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "0")
                    logging.debug("Up pressed : %s", url)
                elif event.key == pylocals.K_s:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "2")
                    logging.debug("Down pressed : %s", url)
                elif event.key == pylocals.K_a:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "4")
                    logging.debug("Left pressed : %s", url)
                elif event.key == pylocals.K_d:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "6")
                    logging.debug("Right pressed : %s", url)
                elif event.key == pylocals.K_ESCAPE:
                    print("[*] Exiting")
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pylocals.K_w:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "1")
                    logging.debug("Up released : %s", url)
                elif event.key == pylocals.K_s:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "3")
                    logging.debug("Down released : %s", url)
                elif event.key == pylocals.K_a:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "5")
                    logging.debug("Left released : %s", url)

                elif event.key == pylocals.K_d:
                    response = connect("http://" + address +
                                       ":" + port +
                                       "/decoder_control.cgi?user=" + user +
                                       "&pwd=" + password +
                                       "&command=" + "7")
                    logging.debug("Right released : %s", url)

            if (response is not None) and (url is not None) and (response.status_code != 200):
                logging.warning("Error while making request" +
                                " : HTTP %d : %s", response.status_code, url)


def connect(address: str):
    """
    Tries to connect to the IP camera, prints and logs the error if it fails.

    :param address: The IP address of the IP camera
    :return:
        The response object returned by requests.get()
    """

    try:
        response = requests.get(address, headers=HEADERS)
        return response
    except requests.exceptions.ConnectionError as error:
        print(error)
        logging.error(error, exc_info=True)
        logging.shutdown()
        sys.exit(0)


def init():
    """
    Initializes the main variables using the CLI.

    :return:
        None
    """
    logging.basicConfig(filename="camera_controller.log",
                        filemode='w',
                        format='%(process)d - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument("--user",
                        dest="user",
                        default="admin",
                        help="The IP camera user",
                        action='store_true')
    parser.add_argument("--password",
                        dest="password",
                        default="0000",
                        help="The IP camera password",
                        action='store_true')
    parser.add_argument("--port",
                        dest="port",
                        default="81",
                        help="The port used to connect to the IP camera",
                        action='store_true')
    parser.add_argument("--ip",
                        dest="ip",
                        help="The IP address of the IP camera",
                        required=True)

    arguments = parser.parse_args()

    if not arguments.user:
        print("[*] No user provided, using the default one.")
        logging.debug("No user provided, using the default one.")
    if not arguments.password:
        print("[*] No password provided, using the default one.")
        logging.debug("No password provided, using the default one.")
    if not arguments.port:
        print("[*] No port provided, using the default one.")
        logging.debug("No port provided, using the default one.")

    get_video(arguments.user, arguments.password, arguments.ip, arguments.port)
    time.sleep(3)
    show_menu(arguments.user, arguments.pwd, arguments.ip, arguments.port)


if __name__ == "__main__":
    init()
