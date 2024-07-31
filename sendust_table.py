#   Interactive Table manipulator by sendust
#   2024/7/25   First release...
#
#

import os, json, sys

class table:
    def __init__(self):
        self.t = []
        self.header = []
        self.name_file = "table"
       
    def data_put_dict(self, data):
        self.t.append(data)
        print(f'append table with data {data}')
        
    def show(self):
        print("header ----")
        print(self.header)
        print("data ------")
        cnt = 0
        for each in self.t:
            print(f'{cnt} -->  {each}')
            cnt += 1
    
    def header_put(self, header):
        self.header.append(header)
    
    def save(self):
        with open(f'{self.name_file}.json', "w") as f:
            json.dump({"header" : self.header, "data" : self.t}, f, indent=2, default=str)
        print(f'save table..  [{self.name_file}.json]  record length {len(self.t)}')
        
    def load(self):
        if not os.path.isfile(f'{self.name_file}.json'):
            print("file not exist !! abort load")
            return
            
        with open(f'{self.name_file}.json', "r") as f:
            json_load = json.load(f)
        self.header = json_load["header"]
        self.t = json_load["data"]
        print(f'load table.. [{self.name_file}.json]   record length {len(self.t)}')

    def new(self):
        self.t = []
        self.header = []
        print("Table cleared..")
        self.show()
        
    def set_file(self, name):
        self.name_file = name


class interactive:
    def __init__(self):
        self.cmd = []
        self.cmd_fn = {}
        
    def add_cmd(self, cmd):
        self.cmd.append(cmd)
    
    def add_cmd_list(self, l):
        for each in l:
            self.cmd.append(each)

    def map_fn(self, cmd, fn):
        self.cmd_fn[cmd] = fn
    
    def do_cmd(self, cmd, *arg):
        self.cmd_fn[cmd](*arg)
    

def help():
    global cli
    print("command list...")
    for each in cli.cmd:
        print(each)

def header():
    global cli, db
    db.show()
    cnt = 0
    keep_input = True
    while keep_input:
        cnt += 1
        h = input(f'Please input header field [{cnt}]  ')
        if not h:
            keep_input = False
            continue
        db.header_put(h)
    db.show()

def show_all():
    global db
    db.show()

def put_data():
    global cli, db
    db.show()
    keep_input = True
    if not len(db.header):
        print("header is empty..")
        return
        
    while keep_input:
        record_single = {}      # Create dict for single record
        for each_header in db.header:
            record_single[each_header] = ''
        for each_header in db.header:
            data = input(f'Input data for [{each_header}]  ')
            if data:
                record_single[each_header] = data
            else:
                keep_input = False
                break
        if data:    # There is input data
            db.data_put_dict(dict(record_single))
    db.show()       
    

def save():
    global db
    db.save()

def load():
    global db
    db.load()

def new():
    global db
    db.new()


def delete():
    global db
    db.show()
    nbr = int(input("Please input row number for delete  "))
    if (nbr < len(db.t)):
        db.t.pop(nbr)
        print(f'row number {nbr} deleted...')
    db.show()
    

def edit():
    global db
    db.show()
    nbr = int(input("Please input row number for edit  "))
    if ((nbr < len(db.t)) and nbr >= 0):
        for each in db.t[nbr]:
            print(f'get data .. [{each}] --> [{db.t[nbr][each]}]')
        for each in db.t[nbr]:
            data_new = input(f'Input new data for [{each}].. Press Enter for keep data   ')
            if data_new:
                db.t[nbr][each] = data_new
        print(f'New data .. {db.t[nbr]}')
            #new_data = input(f'Input new data for ')

def quit():
    print("Exit app...")
    sys.exit()

def set_file():
    global db
    print(f'Current file name is {db.name_file}.json')
    name_new = str(input(f'Please input new file name (without extension) ')).strip()
    if name_new:
        db.name_file = name_new
        print(f'New file name is {db.name_file}.json')
    else:
        print(f'Abort file name change..')
    

db = table()
cli = interactive()

cli.add_cmd_list(["new", "file", "edit", "quit", "exit", "delete", "help", "save", "load", "header", "show", "data"])

cli.map_fn("load", load)
cli.map_fn("save", save)
cli.map_fn("help", help)
cli.map_fn("header", header)
cli.map_fn("show", show_all)
cli.map_fn("data", put_data)
cli.map_fn("new", new)
cli.map_fn("edit", edit)
cli.map_fn("delete", delete)
cli.map_fn("quit", quit)
cli.map_fn("exit", quit)
cli.map_fn("file", set_file)

print(f'Available command list....\n {cli.cmd}')
print(f'input command')
try:
    while True:
        cmd = input("..> ").strip()
        if cmd in cli.cmd:
            cli.do_cmd(cmd)
        elif len(cmd):
            print("Unknown command...")

except KeyboardInterrupt:
    pass