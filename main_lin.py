# import psutil
# # Iterate over all running process
# for proc in psutil.process_iter():
#     try:
#         # Get process name & pid from process object.
#         processName = proc.name()
#         processID = proc.pid
#         print(processName , ' ::: ', processID)
#         i = 0
#         print("hey", i)
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass


# f = open('.status_log.txt', 'r')
# lines = f.readlines()

# for line in lines:
#     print(str(line.split()[1]))

