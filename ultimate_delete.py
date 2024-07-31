import sendust_delete, sys, time
from sendustlogger import updatelog


if len(sys.argv) not in [2, 3]:
    print("Usage....\n   ultimate_delete list.json\n   ultimate_delete list.json notest")
    sys.exit()

cleaner = sendust_delete.delete_old()

try:
    cleaner.read_from_json(sys.argv[1])
except Exception as e:
    print(e)
    sys.exit()
    

try:
    if sys.argv[2] == "notest":
        cleaner.no_test()
except:
    updatelog("Default is test mode")


cleaner.show_list()
try:
    while True:
        cleaner.do_delete()
        for tmr in [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
            print(tmr, end=" -> ", flush=True)
            time.sleep(60)
except KeyboardInterrupt:
    pass
