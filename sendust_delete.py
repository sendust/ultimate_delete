import threading, time, os, random, glob, json
from sendustlogger import updatelog

# Delete old files... Created by sendust  2023/5/1
# Modified 2024/3/29    Improve.. (empty folder, root folder)
# 2024/7/25 Add new method (show_list, clear path), improve delete logic



class delete_old():

    list_path=[]
    list_age=[]
    list_recursive = []
    schedule = False
    test_mode = True
    period = 9999
    
    
    def add_path_age(self, dict_paths):
        path = dict_paths["path"]
        age = int(dict_paths["age"]) * 60 * 60
        recursive = int(dict_paths["recursive"])
        
        self.list_path.append(path)
        self.list_age.append(age)     # convert hour to second
        self.list_recursive.append(recursive)
        updatelog(f'Add delete path with age [hour] = {path}   [{age}] [{recursive}]')

    def read_from_json(self, f_json):
        if not os.path.isfile(f_json):
            print("json not exist !! Abort read")
            return

        try:
            with open(f_json, "r") as f:
                json_load = json.load(f)
            header = json_load["header"]
            data = json_load["data"]
            updatelog(f'load table.. [{f_json}]  record length {len(data)}')

            for each in data:
                self.add_path_age(each)
        except Exception as e:
            updatelog(e)
            updatelog('Error read data from json..')
            raise Exception("Error reading json")
            

    def show_list(self):
        for key, value in enumerate(self.list_path):
            print(f'[{value}]   [{self.list_age[key]}]    [{self.list_recursive[key]}]')

    def no_test(self):
        self.test_mode = False

    def clear_path(self):
        self.list_path = []
        self.list_age = []
        self.list_recursive = []
    
    def start_schedule(self, hour):
        self.period = hour
        period_random = self.period * 60 * random.randint(40, 60)   # added 2023/6/7
        self.schedule = True
        self.tmr = threading.Timer(period_random, self.do_delete)  # timer accept second
        self.tmr.name = "DEL_OLD"
        self.tmr.start()
        updatelog(f'delete schedule Timer engaged.. from [start_schedule] function. remain sec.. {period_random}', True)

    def do_delete(self):
        updatelog(f'Test mode is {self.test_mode}')
        if self.schedule:               # Move position here..  (beginning of function)   2023/5/30
            period_random = self.period * 60 * random.randint(40, 60)   # added 2023/6/7
            self.tmr = threading.Timer(period_random, self.do_delete)
            self.tmr.name = "DEL_OLD"
            self.tmr.start()
            updatelog(f'delete schedule Timer engaged.. from [do_delete] function. remain sec.. {period_random}', True)
                
        if not len(self.list_path):
            updatelog("path list is empty... There is  nothing to do..", True)
            return
            
        now = time.time()   # get current time in second
        for idx, path in enumerate(self.list_path):
            updatelog(f'Collect old file list from path = {path}', True)
            isrecursive = self.list_recursive[idx]
            flist = glob.glob(os.path.join(path, "**"), recursive=isrecursive)    # Include subdir
            #flist = glob.glob(os.path.join(path, "*"), recursive=False)     # Exclude subdir

            try:
                flist.remove(path + os.sep)     # Added 2024/3/29   prevent root deletion
            except Exception as e:
                updatelog(e)
                updatelog(path + os.sep)
                
            #print(flist)
            updatelog(f'Number of files = {len(flist)}', True)
            count_file = 0
            count_folder = 0
            for f in flist:
                try:                                # file can be deleted by another engine !!!
                    tm_mod = os.path.getmtime(f)    # Modification time in second
                    tm_cre = os.path.getctime(f)    # Creation time in second, only Windows
                    diff = now - tm_cre             # unit is in second
                except Exception as e:
                    updatelog(f'Error while old collecting old files {f}\n{e}')
                    diff = 0
                    
                if (diff > self.list_age[idx]):
                    #print(f, "  ---- old !!! will delete")
                    #print(datetime.datetime.fromtimestamp(tm_mod))
                    if os.path.isfile(f):
                        try:
                            if not self.test_mode:
                                os.remove(f)
                            count_file += 1
                            updatelog(f'File age is [{diff}] Try to delete old file {f}')
                        except Exception as e:
                            updatelog(f'Error deleting ...   {f}', True)
                    elif (isrecursive and os.path.isdir(f)):
                        try:
                            if not self.test_mode:
                                os.rmdir(f)
                            count_folder += 1
                            updatelog(f'Folder age is [{diff}] Try to delete old folder {f}')
                        except Exception as e:
                            updatelog(f'Error deleting ...   {f}', True)

                    # Added 2024/3/29 -----  delete empty folder..            
                    #if os.path.isdir(f):
                    #    print(f'{f}  is folder !!\nNumber of inside is ')
                    #    n_inside = len(glob.glob(os.path.join(f, "**"), recursive=True))   # Include subdir
                    #    print(n_inside)
                    #    if n_inside < 2:        # empty folder report number 1 length
                    #        updatelog(f'Try to delete empty folder {f}', True)    
                    #        try:
                    #            os.rmdir(f)
                    #            count_folder += 1
                    #        except Exception as e:
                    #            updatelog(f'Error delete empty folder {f}\n{e}', True)    

            updatelog(f'Number of deleted files = {count_file}', True)    
            updatelog(f'Number of deleted folders = {count_folder}', True)    


    def close(self):
        self.schedule = False
        self.tmr.cancel()
        self.schedule = False
        
def get_age(infile):

    try:                                # file can be deleted by another engine !!!
        tm_mod = os.path.getmtime(infile)    # Modification time in second
        tm_cre = os.path.getctime(infile)    # Creation time in second, only Windows
        diff = time.time() - tm_cre             # unit is in second
    except:
        diff = 0

    return diff



#  https://stackoverflow.com/questions/47093561/remove-empty-folders-python
def delete_empty_folders(root):

    deleted = set()
    
    for current_dir, subdirs, files in os.walk(root, topdown=False):

        still_has_subdirs = False
        for subdir in subdirs:
            if os.path.join(current_dir, subdir) not in deleted:
                still_has_subdirs = True
                break
    
        if not any(files) and not still_has_subdirs:
            os.rmdir(current_dir)
            deleted.add(current_dir)

    return deleted
