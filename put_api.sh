#!/bin/bash

#判断参数的个数是否大于等于1
if [ $# -ge 1 ];then

    #定义文件夹
    root_dir="/root/nginx_02/"
    backdir="/root/.backup/"
    abs_filename=$root_dir$1

    #判断是否有这个文件
    if [ -f $abs_filename ];then

        #利用md5sum工具获取文件的md5值
        getfilemd5=`md5sum $abs_filename | awk '{print $1}'`
        echo "$getfilemd5"

        #判断第二个参数是否是move
        if [ $2 == "move" ];then
            #判断是否存在备份目录，没有则存在，有则挪至备份目录
            if [ -d $backdir ];then
                nowtime=`date +"%F_%H:%M:%S"`

                mv $abs_filename $backdir$1_$nowtime

                if [ 0 -eq $? ];then
                    echo "move successful"
                else
                    echo "move failed"
                fi

            else
                mkdir -p $backdir
            fi
        fi

    else
        #报错，没有这个文件
        echo "$1 No such file or directory"
    fi

else
#报错，参数错误
    echo "Parameter error"
fi