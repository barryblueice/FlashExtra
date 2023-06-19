import os,hashlib,psutil,time,wmi,keyboard

def write_data(file_path, size):
    with open(file_path, 'wb') as file:
        global start_time
        start_time = time.time()
        data = os.urandom(size)
        file.write(data)

def verify_data(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        hash_value = hashlib.sha256(data).hexdigest()
        global end_time
        end_time = time.time()
        return hash_value

def get_disk_info():
    c = wmi.WMI()
    disk_info = []
    for disk in c.Win32_DiskDrive():
        name = disk.Caption.strip()
        for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                disk_info.append((name, logical_disk.DeviceID))
    return disk_info

def main():
    disk_info = get_disk_info()
    print("硬盘名称和盘符列表:")
    for name, device_id in disk_info:
        print(f"硬盘名称: {name}")
        print(f"盘符: {device_id}")
        print()


    disk_path_handle = input("请输入待测盘符（只要字母，不要冒号）：").upper()
    if str(disk_path_handle+":") not in device_id:
        exit()
    correct_times = int(input("请输入校验圈数（只要整数）："))

    global_start_time = time.time()

    print ("正在校验中，请稍后……")
    disk_path = f"{disk_path_handle}:/"
    verify_error = 0
    verify_pass = 0

    disk_info = psutil.disk_usage(disk_path)
    disk_capacity = disk_info.total
    file_size = 2 * 1024 * 1024 * 1024

    total_files = disk_capacity // file_size

    for times in range(0,correct_times):
        times += 1
        if times <= correct_times:
            try:
                for i in range(total_files):
                    file_name = f"file{i}.dat"
                    file_path = os.path.join(disk_path, file_name)
                    if (disk_capacity - file_size) < (2 * 1024 * 1024 * 1024):
                        write_data(file_path, ((disk_capacity - file_size) - 2 * 1024))
                    else:
                        write_data(file_path, file_size)
                    hash_value = verify_data(file_path)

                    if hash_value != verify_data(file_path):
                        print(f"数据错误：文件{file_name}位置 {hash_value} 不匹配")
                        verify_error += 1
                    else:
                        print(f"已写入文件{file_name}并校验成功，用时{end_time - start_time}秒……")
                        verify_pass += 1
            except:
                print("程序出错，无法写入文件！（按下回车键以退出程序……）")
                keyboard.wait('enter')
                exit()

            if verify_error != 0:
                print(f"检测完毕！本次检测用时：{global_end_time-global_start_time}；当前已校验圈数：{times}；数据包校验通过数：{verify_pass}；数据包校验未通过数：{verify_error}。请注意数据安全！")
            else:
                print(f"检测完毕！本次检测用时：{global_end_time-global_start_time}；当前已校验圈数：{times}；数据包校验全部通过！")

        else:
            break

    global_end_time = time.time()

    if verify_error != 0:
        print(f"检测完毕！本次检测用时：{global_end_time-global_start_time}；总校验圈数：{correct_times}；数据包校验通过数：{verify_pass}；数据包校验未通过数：{verify_error}。请注意数据安全！")
    else:
        print(f"检测完毕！本次检测用时：{global_end_time-global_start_time}；总校验圈数：{correct_times}；数据包校验全部通过！")

if __name__ == "__main__":
    main()
