#!/usr/bin/env python
import os
import hashlib
import paramiko
import time
import sys

def get_md5(filename):
    file_hash = hashlib.md5()
    f = open(filename, "rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        file_hash.update(b)
    f.close()
    return file_hash.hexdigest()

def send_files(sftp, ssh, filename, abspathfile, server_dir):
    try:
        print("删掉文件", end="")
        print(filename)
        ssh.exec_command("bash /root/put_api.sh %s move"  % filename)
        print("删掉文件成功")
        print("开始上传文件")
        server_file = server_dir + filename
        sftp.put(abspathfile, server_file)
        print("文件上传成功")
    except:
        print("上传文件失败")
def search_file(dir, path, ssh, server_dir):
    suffix = 'md'

    print("开启sftp")
    t = paramiko.Transport(('101.42.107.248', 22))
    t.connect(username='root', password='1749907938')
    sftp = paramiko.SFTPClient.from_transport(t)

    for filename in os.listdir(path):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("开始处理 %s" % (filename))

        # 如果以md结尾，就continue
        if filename.endswith(suffix):
            print("不处理以md结尾")
            continue

        # 定义绝对路径
        abspathfile = dir + '\\' + filename

        # 获取文件的md5
        localfilemd5 = get_md5(abspathfile) + '\n'

        byte_localfilemd5 = localfilemd5.encode(encoding="gb2312")
        print("%s md5值 %s" % (filename, byte_localfilemd5))

        serverfilemd5 = get_server_md5(ssh, filename)

        print("%s 服务器md5值 %s" % (filename, serverfilemd5))

        if byte_localfilemd5 == serverfilemd5:
            print("md5值一致，不需要上传")
        else:
            print("md5值不一致，上传文件")

            #        send_files(sftp,ssh,filename,abspathfile,server_dir)
            try:
                #                send_files(ssh,filename,abspathfile,server_dir)
                send_files(sftp, ssh, filename, abspathfile, server_dir)
            except:
                print("上传失败...")

    print("关闭sftp")
    t.close()


def get_server_md5(ssh, filename):
    stdin, stdout, stderr = ssh.exec_command('bash /root/put_api.sh %s' % filename)
    result = stdout.read()

    return result


def main():
    starttime = time.time()

    print("脚本开始同步")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='101.42.107.248', port='22', username='root', password='1749907938')
    except:
        print("服务器连接失败，异常退出")
        sys.exit(-1)

    # 定义路径
    local_dir = "D:\\scp"
    server_dir = '/root/nginx_02/'

    # 利用函数排除文件
    search_file(local_dir, local_dir, ssh, server_dir)

    #    print (get_server_md5(ssh,'d0180727_install_rabbitmt_png_06.png'))

    ssh.close()
    endtime = time.time()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("服务器断开连接,本次文件更新成功")
    print("本次更新时间为:%.2f s" % (endtime - starttime))
    print("更精确的时间:", end=" ")
    usedtime = endtime - starttime
    print(usedtime, end=" ")
    print("s")


if __name__ == "__main__":
    print("lvlongxin_test")
    main()

