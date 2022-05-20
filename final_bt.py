
import datetime
import argparse
import json
import pandas as pd
from bluepy.btle import Scanner, DefaultDelegate
from upload import Sheets



class Resturant(DefaultDelegate):
    
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.number = 0

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass

    def number(self):
        print(self.number)


class BluetoothProject:
    
    def __init__(self, T=60, rssi_threshold=-80, U=300):
        self.scanner = Scanner().withDelegate(Resturant())
        self.loop_time = T
        self.rssi_threshold = rssi_threshold
        self.U = U
        self.df = pd.DataFrame(
            columns=['addr', 'first_detect_time', 'minute_spent'])
        self.memory = {}
        self.cred_path = "utils/credentials.json"
        self.Sheets = Sheets(self.cred_path)
        self.worksheet = self.Sheets.open_sheet_by_name("crowdbt")

    def start_scan(self):
        self.devices = self.scanner.scan(self.loop_time)

    def clear_scal(self):
        self.scanner.clear()

    def drop_rssi(self):
        self.devices = list(self.devices)
        gt_devices = []

        for i, dev in enumerate(self.devices):
            if dev.rssi > self.rssi_threshold:
                gt_devices.append(dev)
        self.devices = gt_devices

    def add_to_memory(self, dev_addr):
        self.memory[dev_addr] = {
            'first_detect_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'minute_spent': 0}

    def check_memory_test(self):
        head_count = 0

        # Checking the current devices if present in memory
        
        for dev in self.devices:
            
            # If device is present in memory add a minute to time spent
            if dev.addr in self.memory.keys():
                self.memory[dev.addr]['minute_spent'] += 1
            
            # If device is not present in memory add it to the memory
            else:
                self.add_to_memory(dev.addr)

        return True

    def final_summary(self):
        
        self.summary = self.df[self.df.minute_spent > 0]
        # out = self.summary.to_json(orient='records')
        # x = json.loads(out)
        # print(self.summary)
        output = {'Current Time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  'Detected_devices': list(self.summary.addr.values),
                  'Total Head Count': len(self.summary),
                  'dwell time (minutes)': list(self.summary.minute_spent.values)}
        return output

    def reporting(self):

        for devs, value in self.memory.items():

            tmp = pd.DataFrame({'addr': [devs], 'first_detect_time': [
                               value['first_detect_time']], 'minute_spent': [value['minute_spent']]})
            self.df = pd.concat([self.df, tmp])

    def main_loop(self):
        # Infinite Loop for the program, Use Cntl + C to stop
        while True:
            
            ## Reseting Memory and Output Dataframe
            self.memory={}
            self.df = pd.DataFrame(
            columns=['addr', 'first_detect_time', 'minute_spent'])            
            self.run()

    def update_sheets(self, final_output):
        Total_Headcount = len(final_output['Detected_devices'])
        # final_output['Detected_devices'] = ['a','b','c']
        # a = '['+ ' '.join(final_output['Detected_devices']) + ']'
        # print(a)
        if Total_Headcount != 0:
            dwell_time = max(final_output['dwell time (minutes)'])
                             
        else:
            dwell_time = 0
        
        to_append =  [final_output['Current Time'], Total_Headcount, dwell_time]
        print(to_append)
        self.worksheet.append_rows([to_append])
        
        
    def run(self):
        total_iteration = int(self.U/self.loop_time)
        
        for i in range(total_iteration):
            print(f'---------------- Iteration {i+1} ----------------')
            self.start_scan()
            self.drop_rssi()

            ks = []
            
            for dev in self.devices:
                ks.append(dev.addr)

            # print('Previous Memory', self.memory)
            # print('Devices Found in current iteration', ks)

            _ = self.check_memory_test()

        self.reporting()
        final_output = self.final_summary()
        Total_Headcount = len(final_output['Detected_devices']) 
        
        # print("Full Summary of Devices Detected \n ", self.summary)
        # print("--------------------------------------------------")
        print("Output for Spreadsheet final_output\n", final_output)
        print("--------------------------------------------------")
        self.update_sheets(final_output)
        self.clear_scal()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    
    parser.add_argument('-r', default=-80, type=float,
                        help=' rssi_threshold')
    parser.add_argument('-t',  default=60, type=int, 
                    help='Single Iteration Time')
    parser.add_argument('-u',  default=300, type=int, 
                    help='Reporting Time')

    args = parser.parse_args()
    
    
    myobj = BluetoothProject(T=args.t, rssi_threshold=args.r, U=args.u)

    myobj.main_loop()
