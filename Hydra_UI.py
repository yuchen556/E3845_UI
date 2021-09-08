# https://datatofish.com/entry-box-tkinter/
import tkinter as tk
# import PLC
import Camera_Hydra_UI
import Keyboard_Function
import os
from os import path
import logging
import smtplib
import ssl
import PLC
from Camera_Hydra_UI import remove_space
import cv2
import re
import numpy as np
import pytesseract
import time
from datetime import datetime


# 调用图形界面
root = tk.Tk()
# 图形界面的大小 400*300
canvas1 = tk.Canvas(root, width=1300, height=700, relief='raised')
canvas1.pack()
# 图形界面里显示的文字、及位置
label1 = tk.Label(root, text='UI_E3845 Test Platform')
label1.config(font=('helvetica', 20))
canvas1.create_window(200, 45, window=label1)
# 图形界面里显示的文字、及位置
label2 = tk.Label(root, text='请扫描条形码:')
label2.config(font=('helvetica', 15))
canvas1.create_window(200, 100, window=label2)
# 图形界面里SN 的输入框、及位置
entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


# 点击button，运行get_spinel_sn()函数:
def get_spinel_sn():
    global spinel_sn
    spinel_sn = entry1.get()

    # check the previous broken log file existed or not.
    if path.exists(r'D:\Hydra_UI_Test_Log\20212021.log'):
        print("Delete the previous file.")
        os.remove(r'D:\Hydra_UI_Test_Log\20212021.log')
    else:
        print("No file existed!")

    time.sleep(2)
    ui_temp_name = "20212021" + ".log"
    logging.basicConfig(filename=r'D:\Hydra_UI_Test_Log\{:s}'.format(ui_temp_name), filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S',
                        level=logging.DEBUG)

    logging.debug(':Start testing')

    # 若sn 是13位的，则使输入框disable.
    if (len(spinel_sn) == 13):
        # 图形界面里显示的文字
        t1 = time.time()
        label3 = tk.Label(root, text='SN of this board is:', font=('helvetica', 10))
        canvas1.create_window(200, 210, window=label3)

        label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 20, 'bold'))
        canvas1.create_window(200, 250, window=label4)
        # 图形界面里button 变为绿色，输入框变为不能输入
        button1.configure(background="green")
        entry1.config(state='disabled')

        # 从主BIOS 启动
        # J8，J9 都是断开状态，将PLC（网络继电器控制器）的Realy—2 设置为常开。
        PLC.Secondary_BIOS_off()
        # 给系统上电
        PLC.AC_Power_off()
        PLC.AC_Power_on()

        # 启动后进入 BIOS
        logging.debug(':Send_Delete_1st_time!')
        print("Send_Delete_1st_time!")
        for xx11 in range(50):
            Keyboard_Function.Keyboard_send("Send_Delete")
            print("Send_Delete_1st" + "_" + str(xx11))
            time.sleep(1)

        # Go to Save & Exit page:
        time.sleep(1)
        Keyboard_Function.Keyboard_send("Send_Left_Arrow")
        logging.debug(':Send_Left_Arrow_1st')
        print("Send_Left_Arrow_1st")
        time.sleep(1)
        UI_Camera = Camera_Hydra_UI.initial_camera()
        R11, D1 = Camera_Hydra_UI.capture_EFI_Shell(UI_Camera)


        if D1 == 3:

            logging.debug(':' + '_Shell at row:_' + str(R11) + '_Device QTY:_' + str(D1))
            print(R11, D1)
            time.sleep(1)
            Keyboard_Function.judge_EFI_Shell_row(R11)
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_1")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_2")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_3")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_4")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_5")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_6")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("Del+Ctrl+Alt_7")
            logging.debug(':Send_Delete_Ctrl_Alt_1st')
            print("Send_Delete_Ctrl_Alt_1st")
            time.sleep(5)
            logging.debug(':Send_Delete_2nd_time')
            print("Send_Delete_2nd_time")
            for xx11 in range(20):
                Keyboard_Function.Keyboard_send("Send_Delete")
                print("Send_Delete_2nd" + "_" + str(xx11))
                time.sleep(1)

            # Go to Save & Exit page:
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Left_Arrow")
            logging.debug(':Send_Left_Arrow_2nd')
            print("Send_Left_Arrow_2nd")
            time.sleep(1)
            UI_Camera1 = Camera_Hydra_UI.initial_camera()
            R22, D2 = Camera_Hydra_UI.capture_EFI_Shell(UI_Camera1)

            if D2 == 3:
                logging.debug(':' + '_Shell at row:_' + str(R22) + '_Device QTY:_'+ str(D2))
                Keyboard_Function.judge_EFI_Shell_row(R22)

                # Wait 180 seconds to auto-upgrade United-image BIOS.
                for wait300 in range(300):
                    print("Upgrading_BIOS" + "_" + str(wait300))
                    time.sleep(1)

                # Reboot machine.
                Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
                logging.debug(':Send_Delete_Ctrl_Alt_2nd_time')
                print("Send_Delete_Ctrl_Alt_2nd_time")

                time.sleep(2)
                logging.debug(':Send_Delete_3rd_time')
                print("Send_Delete_3rd_time")
                for xx11 in range(20):
                    Keyboard_Function.Keyboard_send("Send_Delete")
                    print("Send_Delete_3rd" + "_" + str(xx11))
                    time.sleep(1)

                UI_Camera22 = Camera_Hydra_UI.initial_camera()
                UI_test_result_1 = Camera_Hydra_UI.check_united_image_bios_version(UI_Camera22)

                if UI_test_result_1 == True:
                    logging.debug('1st_BIOS is Successfully!')
                    print("1st_BIOS is Successfully!")
                    time.sleep(2)
                else:
                    logging.critical('1st_BIOS_Error')
                    print("1st_BIOS_Error")
                    time.sleep(4)


            elif D2 == 2:
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
            else:
                print("Machine error 2nd")
                print("Machine error 2nd")
                print("Machine error 2nd")

        elif D1 == 2:
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
        else:
            print("Machine error!")
            print("Machine error!")
            print("Machine error!")

        # 更新2nd BIOS，开始重新启动系统
        # 更新2nd BIOS，开始重新启动系统
        # 更新2nd BIOS，开始重新启动系统
        #
        # 从副BIOS 启动
        # J8短接，J9 断开，将PLC（网络继电器控制器）的Realy—2 设置为常闭。
        PLC.Secondary_BIOS_on()
        time.sleep(4)
        Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
        print("2-1_Del+Ctrl+Alt_")
        time.sleep(1)
        Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
        print("2-2_Del+Ctrl+Alt_")

        # 启动后进入 BIOS
        logging.debug('2-:Send_Delete_1st_time!')
        print("2-Send_Delete_1st_time!")
        for xx11 in range(50):
            Keyboard_Function.Keyboard_send("Send_Delete")
            print("2-Send_Delete_1st" + "_" + str(xx11))
            time.sleep(1)

        # Go to Save & Exit page:
        time.sleep(1)
        Keyboard_Function.Keyboard_send("Send_Left_Arrow")
        logging.debug('2-:Send_Left_Arrow_1st')
        print("2-Send_Left_Arrow_1st")
        time.sleep(1)
        UI_Camera = Camera_Hydra_UI.initial_camera()
        R11, D1 = Camera_Hydra_UI.capture_EFI_Shell(UI_Camera)


        if D1 == 3:

            logging.debug('2-:' + '_Shell at row:_' + str(R11) + '_Device QTY:_' + str(D1))
            print(R11, D1)
            time.sleep(1)
            Keyboard_Function.judge_EFI_Shell_row(R11)
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_1")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_2")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_3")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_4")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_5")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_6")
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
            print("2-Del+Ctrl+Alt_7")
            logging.debug('2-:Send_Delete_Ctrl_Alt_1st')
            print("2-Send_Delete_Ctrl_Alt_1st")
            time.sleep(5)
            logging.debug('2-:Send_Delete_2nd_time')
            print("2-Send_Delete_2nd_time")
            for xx11 in range(20):
                Keyboard_Function.Keyboard_send("Send_Delete")
                print("2-Send_Delete_2nd" + "_" + str(xx11))
                time.sleep(1)

            # Go to Save & Exit page:
            time.sleep(1)
            Keyboard_Function.Keyboard_send("Send_Left_Arrow")
            logging.debug('2-:Send_Left_Arrow_2nd')
            print("2-Send_Left_Arrow_2nd")
            time.sleep(1)
            UI_Camera1 = Camera_Hydra_UI.initial_camera()
            R22, D2 = Camera_Hydra_UI.capture_EFI_Shell(UI_Camera1)

            if D2 == 3:
                logging.debug('2-:' + '_Shell at row:_' + str(R22) + '_Device QTY:_'+ str(D2))
                Keyboard_Function.judge_EFI_Shell_row(R22)

                # Wait 180 seconds to auto-upgrade United-image BIOS.
                for wait300 in range(300):
                    print("2-Upgrading_BIOS" + "_" + str(wait300))
                    time.sleep(1)

                # Reboot machine.
                Keyboard_Function.Keyboard_send("Send_Delete_Ctrl_Alt")
                logging.debug('2-:Send_Delete_Ctrl_Alt_2nd_time')
                print("2-Send_Delete_Ctrl_Alt_2nd_time")

                time.sleep(2)
                logging.debug('2-:Send_Delete_3rd_time')
                print("2-Send_Delete_3rd_time")
                for xx11 in range(20):
                    Keyboard_Function.Keyboard_send("Send_Delete")
                    print("2-Send_Delete_3rd" + "_" + str(xx11))
                    time.sleep(1)

                UI_Camera222 = Camera_Hydra_UI.initial_camera()

                UI_test_result_2 = Camera_Hydra_UI.check_united_image_bios_version(UI_Camera222)

                if UI_test_result_2 == True:
                    logging.debug('2nd_BIOS is Successfully!')
                    print("2nd_BIOS is Successfully!")
                    time.sleep(2)
                else:
                    logging.critical('2nd_BIOS_Error')
                    print("2nd_BIOS_Error")
                    time.sleep(4)


                UI_BIOS_result =UI_test_result_1 and UI_test_result_2

                if UI_BIOS_result == True:
                    logging.debug('Primary and Secondary BIOS are Successfully!')
                    t2 = time.time()
                    duration = t2 - t1
                    logging.critical(': test duration:_' + str(duration))
                    print(duration)
                    print("BIOS is Successful_Primary and Secondary")
                    print("BIOS is Successful_Primary and Secondary")
                    print("BIOS is Successful_Primary and Secondary")
                    print("BIOS is Successful_Primary and Secondary")
                    print("BIOS is 1.3.1-UI")

                    test_time = datetime.now()
                    test_time1 = test_time.strftime("%c")
                    test_time2 = test_time1.replace(':', '-')

                    logging.shutdown()
                    os.rename(r'D:\Hydra_UI_Test_Log\20212021.log', r'D:\Hydra_UI_Test_Log\SN_{}.log'.format(spinel_sn + '_' + test_time2 + '_' + 'Passed'))

                    time.sleep(4)
                    # Mail result
                    smtp_server = 'smtp.sina.com'
                    port = 465
                    sender = 'yuchen556@sina.com'
                    receiver = ['556wangzhen@163.com', 'jiandong_bao@163.com']
                    message = "Subject:Passed__Hydra_UI_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver)

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender, '7a97e1a7467ba258')
                        server.sendmail(sender, receiver, message)
                        print('Mail_sent')

                else:
                    logging.critical('Primary and Secondary_Error!!!')
                    t2 = time.time()
                    duration = t2 - t1
                    logging.critical(': test duration:_' + str(duration))
                    print(duration)
                    print("Primary and Secondary_BIOS__Error!")

                    test_time = datetime.now()
                    test_time1 = test_time.strftime("%c")
                    test_time2 = test_time1.replace(':', '-')

                    logging.shutdown()
                    os.rename(r'D:\Hydra_UI_Test_Log\20212021.log', r'D:\Hydra_UI_Test_Log\SN_{}.log'.format(spinel_sn + '_' + test_time2 + '_' + 'Failed'))

                    time.sleep(4)
                    # Mail result
                    smtp_server = 'smtp.sina.com'
                    port = 465
                    sender = 'yuchen556@sina.com'
                    receiver = ['556wangzhen@163.com', 'jiandong_bao@163.com']
                    message = "Subject:Failed_Hydra_UI_{}!\r\nThis message was sent from Python!\r\nFrom:{}\r\nTo: {}\r\n".format(spinel_sn, sender, receiver)

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender, '7a97e1a7467ba258')
                        server.sendmail(sender, receiver, message)
                        print('Mail_sent')

            elif D2 == 2:
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
                print("2nd_time_Please power off machine and insert Sandisk USB disk! ___Retest!")
            else:
                print("Machine error 2nd")
                print("Machine error 2nd")
                print("Machine error 2nd")

        elif D1 == 2:
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
            print("1st_Please power off machine and insert Sandisk USB disk! ___Retest!")
        else:
            print("Machine error!")
            print("Machine error!")
            print("Machine error!")

        # J8，J9 都设置成断开状态，将PLC（网络继电器控制器）的Realy—2 设置为常开。
        PLC.Secondary_BIOS_off()
        PLC.AC_Power_off()
        quit()

    # 若sn 不是13位的，则提示sn is incorrect；
    else:
        label3 = tk.Label(root, text='SN is incorrect', fg='red', font=('helvetica', 10,))
        canvas1.create_window(200, 210, window=label3)

        label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 10, 'bold'))
        canvas1.create_window(200, 230, window=label4)

        button1.configure(background="black")


# 点击button，运行get_spinel_sn() 函数:
button1 = tk.Button(text='Testing', command=get_spinel_sn, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 190, window=button1)

root.mainloop()
