import time
import os
from ftplib import FTP


class FTPRetrFiles(object):
    def __init__(self, base_url, data_path, files_keywords):
        self.base_url = base_url
        self.data_path = data_path
        self.files_needed = files_keywords
        self.files_found = list()  # the list store the files found in the target ftp folder
        self.files_ready = list()  # the list store the ready files
        self.files_ready_flag = False  # True if the files we want is all ready

    def connect(self):
        '''Login to the target remote ftp server and cd to folder'''
        self.ftp = FTP(self.base_url)
        self.ftp.login()
        self.ftp.cwd(self.data_path)

    def get_files_list(self):
        '''Get the files list in the target folder'''
        self.files_found = []
        def get_list_callback(line):
            '''As retrlines() callback function to store the files founded'''
            line_clean = line.strip()
            self.files_found.append(line_clean)
        self.ftp.retrlines('NLST', callback=get_list_callback)

    def is_files_ready(self):
        '''To check if the files we want has been uploaded to the target folder '''
        if not self.files_found:  # if the get_files_list() has not been ran
            self.get_files_list()
        for file_needed in self.files_needed:
            for file_found in self.files_found:
                if file_needed in file_found:
                    self.files_ready.append(file_found)
        # Files needed is not all ready
        if len(self.files_ready) != len(self.files_needed):
            self.files_ready = list()
            self.files_ready_flag = False
            print('Files are not ready yet!')
            return False
        self.files_ready_flag = True
        print('Files are all ready')
        return True

    def retr_files(self, save_path=None):
        if not self.files_ready_flag:
            print('Files needed is not ready!')
            return
        # retrieve every files we need
        t_begin_retr = time.time()
        for index, file_ready in enumerate(self.files_ready):
            self.file_retrieving = file_ready  # let retr_files_callback function know which file is retrieving now
            # generate the saved files path, if not given, save to the current folder
            if save_path is not None:
                file_ready_path = os.path.join(save_path, file_ready)
                print('%d. Save path: %s' % (index+1, save_path))
            else:
                file_ready_path = file_ready
                print('%d. Save path: %s' % (index+1, os.getcwd()))
            print('Begin retrieve -> %s' % file_ready)
            # Start to retrieve file from ftp server using binary mode
            self.ftp.retrbinary('RETR %s' % file_ready, open(file_ready_path, 'wb').write)
            print('Success save -> %s' % file_ready)
        t_end_retr = time.time()
        print('-'*20)
        print('Task finished!')
        print('# Time consumed: %f' %(t_end_retr-t_begin_retr))

    def quit(self):
        self.ftp.quit()


if __name__ == '__main__':
    base_url = '10.55.250.190'  # the FTP server address
    data_path = 'GroupDownload/FTC-C919-10101-0036/20171108SADRI/'  # The folder we need to enter
    files_keywords = ('CAOWEN-429002', 'CAOWEN-429003', 'CAOWEN-664002', 'CAOWEN-664003', 'CAOWEN-664004')  # the key words of files we needed
    save_path = r'\\Yf-js01259\C919 SnC Work Platform\5.6 试飞分析\试飞数据\test'

    while True:
        ftp = FTPRetrFiles(base_url=base_url, data_path=data_path, files_keywords=files_keywords)
        ftp.connect()
        ftp.get_files_list()
        if ftp.is_files_ready():
            # ftp.retr_files(r'F:\ftp_get')
            ftp.retr_files(save_path)
            break
        ftp.quit()
        print('Wait next query')
        time.sleep(60*60)
