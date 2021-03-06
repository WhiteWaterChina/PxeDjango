# -*- coding:cp936 -*-

from django.shortcuts import render
import re
import os
import subprocess
import paramiko
import time
from django.contrib import messages

os_type_list = ["redhat", "centos", "suse", "ubuntu", "windows"]
os_version_list = []
bios_ver_list = ["legacy", "uefi"]
os_bit_list = ["64"]
sys_disk_name_list = ["sda", "nvme0n1", "sdb", "sdc", "sdd", "sdf", "sdg", "sdh", "sdi", "sdj",
                      "sdk", "sdl", "sdm", "sdn", "sdo", "sdp", "sdq", "sdr", "sds", "sdt", "sdu",
                      "sdv", "sdw", "sdx", "sdy", "sdz", "nvme1n1", "nvme2n1", "nvme3n1", "nvme4n1"]
ipaddress_dhcp = "100.2.36.2"
ipaddress_windows = '100.2.36.19'
username_dhcp = "root"
password_dhcp = "Testing-123"


def index(request):
    return render(request, "pxe/html.html",
                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list, 'os_bit_list': os_bit_list,
                   'sys_disk_name_list': sys_disk_name_list})


def generate_menu_redhat(os_version_sub, os_sub_version_max_sub, os_sub_version_min_sub, os_bit_sub, bios_mode_sub,
                         ipaddress_dhcp_sub, mac_net_pxe_sub, mac_boot_device_rhel6_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        if os_sub_version_max_sub == "7":
            if os_sub_version_min_sub == "4" or os_sub_version_min_sub == "3":
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.img inst.dd=http://{ipaddress_dhcp}/driver/kmod-megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm inst.dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            elif os_sub_version_min_sub == "2":
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.img inst.dd=http://{ipaddress_dhcp}/driver/kmod-megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm  modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            elif os_sub_version_min_sub == "1":
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.img inst.dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            else:
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.img  modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        elif os_sub_version_max_sub == "6":
            if os_sub_version_min_sub == "9" or os_sub_version_min_sub == "8" or os_sub_version_min_sub == "7":
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img ramdisk_size=8192 dd=http://{ipaddress_dhcp}/driver/megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.iso/dd.iso  ip=dhcp ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
            elif os_sub_version_min_sub == "6":
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img ramdisk_size=8192 dd=http://{ipaddress_dhcp}/driver/mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.iso/dd.iso ip=dhcp ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
            else:
                string_to_write.append(
                    "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img ramdisk_size=8192  ip=dhcp ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        elif os_sub_version_max_sub == "8":
            string_to_write.append(
                "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.img modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd.img".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "menuentry '{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}' --class os ".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + '{' + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append(
            "set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        if os_sub_version_max_sub == "7":
            if os_sub_version_min_sub == "4" or os_sub_version_min_sub == "3":
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz inst.dd=http://{ipaddress_dhcp}/driver/kmod-megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm inst.dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm  modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            elif os_sub_version_min_sub == "2":
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz inst.dd=http://{ipaddress_dhcp}/driver/kmod-megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            elif os_sub_version_min_sub == "1":
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz inst.dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
            else:
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        elif os_sub_version_max_sub == "6":
            if os_sub_version_min_sub == "9" or os_sub_version_min_sub == "8" or os_sub_version_min_sub == "7":
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz ip=dhcp dd=http://{ipaddress_dhcp}/driver/kmod-megaraid_sas-07.705.02.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)

            elif os_sub_version_min_sub == "6":
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz ip=dhcp dd=http://{ipaddress_dhcp}/driver/kmod-mpt3sas-24.00.00.00_el{os_sub_version_max}.{os_sub_version_min}-1.x86_64.rpm ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
            else:
                string_to_write.append(
                    "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz ip=dhcp  ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                        os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                        os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                        mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        elif os_sub_version_max_sub == "8":
            string_to_write.append(
                "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz modprobe.blacklist=qat_c62x ip=dhcp inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd.img".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    print(string_to_write)
    return string_to_write


def generate_menu_suse(os_version_sub, os_sub_version_max_sub, os_sub_version_min_sub, os_bit_sub, bios_mode_sub,
                       ipaddress_dhcp_sub, mac_net_pxe_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/linux initrd=initrd splash=silent showopts edd=off  install=http://{ipaddress_dhcp}/iso/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit} autoyast2=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.xml".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "menuentry '{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}' --class os ".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + "{" + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append(
            "set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        string_to_write.append(
            "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/linux splash=silent showopts install=http://{ipaddress_dhcp}/iso/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit} autoyast2=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.xml".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    return string_to_write


def generate_menu_ubuntu(os_version_sub, os_string_version_sub, os_bit_sub, bios_mode_sub, ipaddress_dhcp_sub,
                         mac_net_pxe_sub, mac_boot_device_rhel6_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/linux initrd=initrd.gz devfs-nomount ramdisksize=16384 vga=normal url=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg netcfg/get_nameservers={ipaddress_dhcp} ks=http://{ipaddress_dhcp}/ks/ks_template/{os_version}/{bios_mode}/{os_version}{os_string_version}_{os_bit}-{bios_mode}.cfg ksdevice={mac_boot_device_rhel6}".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub, mac_net_pxe=mac_net_pxe_sub,
                mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/initrd.gz ".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "menuentry '{os_version}{os_string_version}_{os_bit}' --class os ".format(os_version=os_version_sub,
                                                                                      os_string_version=os_string_version_sub,
                                                                                      os_bit=os_bit_sub) + "{" + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append(
            "set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        string_to_write.append(
            "linux (http)/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/linux devfs-nomount ramdisksize=16384 vga=normal url=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg netcfg/get_nameservers={ipaddress_dhcp} ks=http://{ipaddress_dhcp}/ks/ks_template/{os_version}/{bios_mode}/{os_version}{os_string_version}_{os_bit}-{bios_mode}.cfg ksdevice={mac_boot_device_rhel6}".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub, mac_net_pxe=mac_net_pxe_sub,
                mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append(
            "initrd (http)/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/initrd.gz".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    return string_to_write


def generate_menu_windows(os_version_sub, os_string_version_sub, os_bit_sub, bios_mode_sub, ipaddress_windows_sub):
    string_to_write = ["#!ipxe" + os.linesep, "set timeout=1" + os.linesep,
                       "kernel tftp://{ipaddress_dhcp_temp}/wimboot".format(
                           ipaddress_dhcp_temp=ipaddress_dhcp) + os.linesep]
    if bios_mode_sub == "legacy":
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/bcd BCD".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/bootmgr bootmgr".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/boot.sdi boot.sdi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/sources/boot.wim boot.wim".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot" + os.linesep)
    elif bios_mode_sub == "uefi":
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/EFI/Boot/bootx64.efi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/EFI/Microsoft/Boot/BCD".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/boot.sdi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/sources/boot.wim".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot" + os.linesep)
    return string_to_write


def generate_ks_redhat_centos(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit,
                              os_disk):
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_sub_version_max = os_sub_version.split(".")[0]
    os_sub_version_min = os_sub_version.split(".")[1]
    os_string_version = "-".join(os_sub_version.split("."))
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/{}/{}/'.format(os_version, bios_mode)
    filename_ks_template = "{}{}_{}-{}.cfg".format(os_version, os_string_version, os_bit, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_rhel = "{}.cfg".format(mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_rhel)
    remote_path_ks = '/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)
    local_path_pre = os.path.join(os.getcwd(), "pre.txt")
    filename_remote_pre = "auto-partition-{}.sh".format(bios_mode)
    remote_dir_pre = '/var/www/html/ks/auto_partition/redhat/'
    remote_path_pre = os.path.join(remote_dir_pre, filename_remote_pre)

    # download ks_template & rhel_pre
    down_ks_template = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        print("1")
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            print("2")
            # download_pre
            sftp_down_ks.get(localpath=local_path_pre, remotepath=remote_path_pre)
            print("3")
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
            message_info = "未从TFTP服务器找到对应的OS的KS模板！请检查输入或者联系管理员检查！"
            flag_status = 0
            return flag_status, message_info
        finally:
            sftp_down_ks.close()
            down_ks_template.close()
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        flag_status = 0
        return flag_status, message_info
    finally:
        down_ks_template.close()

        # change ks with pre
    handler_ks_change = open(local_path_pre, mode='rb')
    pattern_os_disk = re.compile(r'firstdisk=sda')
    string_pre = ''
    for item_data_pre in handler_ks_change:
        if re.search(pattern_os_disk, item_data_pre.decode()):
            item_data_pre_1 = re.sub(pattern_os_disk, "firstdisk={}".format(os_disk), item_data_pre.decode())
            string_pre += item_data_pre_1
        else:
            string_pre += item_data_pre.decode()
    handler_ks_change.close()
    handler_ks_change = open(local_path_pre, mode='wb')
    handler_ks_change.write(string_pre.encode())
    handler_ks_change.close()
    handler_ks = open(local_path_ks, mode='rb')
    # change ks bootloader info
    # to 7 serial
    if os_sub_version_max == "7":
        pattern_bootloader = re.compile(r'--boot-drive=sda')
        string_ks = ''
        for item_data_ks in handler_ks:
            if re.search(pattern_bootloader, item_data_ks.decode()):
                item_data_ks_1 = re.sub(pattern_bootloader, "--boot-drive={}".format(os_disk), item_data_ks.decode())
                string_ks += item_data_ks_1
            else:
                string_ks += item_data_ks.decode()
        handler_ks.close()
        handler_ks = open(local_path_ks, mode='wb')
        handler_ks.write(string_ks.encode())
        handler_ks.close()
    elif os_sub_version_max == "6":
        pattern_bootloader = re.compile(r'--driveorder=sda')
        string_ks = ''
        for item_data_ks in handler_ks:
            if re.search(pattern_bootloader, item_data_ks.decode()):
                item_data_ks_1 = re.sub(pattern_bootloader, "--driveorder={}".format(os_disk), item_data_ks.decode())
                string_ks += item_data_ks_1
            else:
                string_ks += item_data_ks.decode()
        handler_ks.close()
        handler_ks = open(local_path_ks, mode='wb')
        handler_ks.write(string_ks.encode())
        handler_ks.close()

    handler_ks = open(local_path_ks, mode='ab+')
    # add pre info to ks file
    handler_pre = open(local_path_pre, mode='rb')
    data_pre_temp = handler_pre.readlines()
    handler_ks.write("%pre --interpreter=/bin/bash\n".encode())
    for item in data_pre_temp:
        handler_ks.write(item)

    handler_ks.write("%end".encode())
    handler_pre.close()
    handler_ks.close()

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_redhat(os_version, os_sub_version_max, os_sub_version_min, os_bit, bios_mode,
                                         ipaddress_dhcp, mac_net_pxe, mac_boot_device_rhel6)
        # print(data_menu)
        for item in data_menu:
            file_menu.write(item.encode())

    # upload menu file & ks
    flag_upload_ks_menu = 1
    remote_path_menu = ''
    if bios_mode == "legacy":
        remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/', mac_boot_device_rhel6 + ".cfg")
    elif bios_mode == "uefi":
        remote_path_menu = os.path.join(r'/opt/config/', mac_boot_device_rhel6 + ".cfg")

    upload_menu = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        # upload_menu
        try:
            sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
            # upload_ks
            sftp_upload_ks.put(localpath=local_path_ks, remotepath=os.path.join(remote_path_ks, filename_ks_local_rhel))
            flag_status = 1
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
            message_info = "无法连接至DHCP服务器，请检查网络连接！"
            flag_status = 0
            return flag_status, message_info
        finally:
            sftp_upload_ks.close()
            upload_menu.close()
            os.remove(local_path_ks)
            os.remove(local_path_menu)
            os.remove(local_path_pre)

        # generate uefi menu for remote server
        if bios_mode == "uefi":
            try:
                ssh_gen_uefi_menu = paramiko.SSHClient()
                ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                ssh_gen_uefi_menu.exec_command(
                    command='cp /opt/config/grub-generate.sh /opt/config/{}.sh'.format(mac_boot_device_rhel6))
                time.sleep(2)
                ssh_gen_uefi_menu.exec_command(command='/opt/config/{mac}.sh {mac}'.format(mac=mac_boot_device_rhel6))
                ssh_gen_uefi_menu.close()
                flag_status = 1
            except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                message_info = "无法连接至DHCP服务器或者对应文件不存在，请检查网络连接!"
                flag_status = 0
                return flag_status, message_info
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        flag_status = 0
        return flag_status, message_info
    finally:
        upload_menu.close()
    message_info = "KS文件产生成功！"
    flag_status = 1
    return flag_status, message_info


def generate_ks_suse(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk):
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_sub_version_max = os_sub_version.split(".")[0]
    os_sub_version_min = os_sub_version.split(".")[1]
    os_string_version = "-".join(os_sub_version.split("."))
    filename_ks_template = "{}{}_{}-{}.xml".format(os_version, os_string_version, os_bit, bios_mode)
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/{}/{}/'.format(os_version, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_suse = "{}.xml".format(mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_suse)
    remote_path_ks = r'/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)
    local_path_pre = os.path.join(os.getcwd(), "pre.txt")
    filename_remote_pre = "auto-partition-{}.sh".format(bios_mode)

    # download ks_template
    down_ks_template = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            # download_pre
            remote_dir_pre = r"/var/www/html/ks/auto_partition/suse/"
            remote_path_pre = os.path.join(remote_dir_pre, filename_remote_pre)
            sftp_down_ks.get(localpath=local_path_pre, remotepath=remote_path_pre)
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
            message_info = "未从TFTP服务器找到对应的OS的KS模板！请检查输入或者联系管理员检查！"
            flag_status = 0
            return flag_status, message_info
        finally:
            sftp_down_ks.close()
            down_ks_template.close()
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException):
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        flag_status = 0
        return flag_status, message_info
    finally:
        down_ks_template.close()

    # change pre file
    handler_ks_change = open(local_path_pre, mode='rb')
    pattern_os_disk = re.compile(r'firstdisk=sda')
    string_pre = ''
    for item_data_pre in handler_ks_change:
        if re.search(pattern_os_disk, item_data_pre.decode()):
            item_data_pre_1 = re.sub(pattern_os_disk, "firstdisk={}".format(os_disk), item_data_pre.decode())
            string_pre += item_data_pre_1
        else:
            string_pre += item_data_pre.decode()
    handler_ks_change.close()
    handler_ks_change = open(local_path_pre, mode='wb')
    handler_ks_change.write(string_pre.encode())
    handler_ks_change.close()

    # upload pre file
    # change pre file name
    filename_pre_suse = "".join(mac_boot_device_rhel6.split(":"))
    flag_upload_pre_menu = 1
    remote_path_pre = os.path.join(r'/var/www/html/ks/ks_all', filename_pre_suse)
    upload_menu = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_pre_suse = paramiko.SFTPClient.from_transport(upload_menu)
        # upload_pre
        sftp_upload_pre_suse.put(localpath=local_path_pre, remotepath=remote_path_pre)
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
        flag_upload_pre_menu = 0
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        return flag_upload_pre_menu, message_info
    finally:
        sftp_upload_pre_suse.close()
        upload_menu.close()
        os.remove(local_path_pre)

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_suse(os_version, os_sub_version_max, os_sub_version_min, os_bit, bios_mode,
                                       ipaddress_dhcp, mac_net_pxe)
        for item in data_menu:
            file_menu.write(item.encode())

    # change ks file
    file_ks_read = open(local_path_ks, mode="rb")
    file_ks_content = file_ks_read.readlines()
    file_ks_read.close()
    pattern_osdisk_suse = re.compile(r'osdisk')
    pattern_pre_suse = re.compile(r'prefile')
    string_pre_suse = ''
    for item_ks_suse in file_ks_content:
        if re.search(pattern_osdisk_suse, item_ks_suse.decode()):
            item_ks_suse_1 = re.sub(pattern_osdisk_suse, "{}".format(os_disk), item_ks_suse.decode())
            string_pre_suse += item_ks_suse_1
        else:
            if re.search(pattern_pre_suse, item_ks_suse.decode()):
                item_ks_suse_1 = re.sub(pattern_pre_suse, "{}".format(filename_pre_suse), item_ks_suse.decode())
                string_pre_suse += item_ks_suse_1
            else:
                string_pre_suse += item_ks_suse.decode()
    os.remove(filename_ks_local_suse)
    # local_path_ks_use = os.path.join(os.getcwd(), filename_ks_local_suse)

    file_ks_write = open(local_path_ks, mode="wb")
    file_ks_write.write(string_pre_suse.encode())
    file_ks_write.close()

    # upload menu file & ks
    flag_upload_ks_menu = 1
    remote_path_menu = ''
    if bios_mode == "legacy":
        remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/',
                                        mac_boot_device_rhel6 + ".cfg")
    elif bios_mode == "uefi":
        remote_path_menu = os.path.join(r'/opt/config/',
                                        mac_boot_device_rhel6 + ".cfg")

    upload_menu = paramiko.Transport("{}:22".format(ipaddress_dhcp))
    try:
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        try:
            # upload_menu
            sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
            # upload_ks
            sftp_upload_ks.put(localpath=local_path_ks,
                               remotepath=os.path.join(remote_path_ks,
                                                       filename_ks_local_suse))
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
            flag_status = 0
            message_info = "同dhcp沟通出现问题，请检查！"
            return flag_status, message_info
        finally:
            sftp_upload_ks.close()
            upload_menu.close()
        # generate uefi menu for remote server
        if bios_mode == "uefi":
            ssh_gen_uefi_menu = paramiko.SSHClient()
            try:
                ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp,
                                          password=password_dhcp)
                ssh_gen_uefi_menu.exec_command(
                    command='cp /opt/config/grub-generate.sh /opt/config/{}.sh'.format(mac_boot_device_rhel6))
                ssh_gen_uefi_menu.exec_command(
                    command='/opt/config/{mac}.sh {mac}'.format(
                        mac=mac_boot_device_rhel6))
            except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                flag_status = 0
                message_info = "无法连接至DHCP服务器，请检查网络连接！"
                return flag_status, message_info
            finally:
                ssh_gen_uefi_menu.close()

    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
        flag_status = 0
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        return flag_status, message_info
    finally:
        upload_menu.close()
        os.remove(local_path_ks)
        os.remove(local_path_menu)
    flag_status = 1
    message_info = "KS文件产生成功！"
    return flag_status, message_info


def generate_ks_ubuntu(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk):
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_string_version = "-".join(os_sub_version.split("."))
    filename_ks_template = "preseed-{}{}_{}-{}.cfg".format(os_version, os_string_version, os_bit, bios_mode)
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/{}/{}/'.format(os_version, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_rhel = "{}.cfg".format(mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_rhel)
    remote_path_ks = r'/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)

    # download ks_template & rhel_pre
    down_ks_template = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            flag_ks_local_exists = 1
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
            flag_status = 0
            message_info = "未从TFTP服务器找到对应的OS的KS模板！请检查输入或者联系管理员检查！"
            return flag_status, message_info
        finally:
            sftp_down_ks.close()
            down_ks_template.close()
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
        flag_status = 0
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        return flag_status, message_info
    finally:
        down_ks_template.close()

    # change ks with pre
    handler_ks_change = open(local_path_ks, mode='rb')
    pattern_os_disk = re.compile(r'/dev/sda')
    string_pre = ''
    for item_data_pre in handler_ks_change:
        if re.search(pattern_os_disk, item_data_pre.decode()):
            data_pre = re.sub(pattern_os_disk, "/dev/{}".format(os_disk), item_data_pre.decode())
            string_pre += data_pre
        else:
            string_pre += item_data_pre.decode()
    handler_ks_change.close()
    handler_ks_change = open(local_path_ks, mode='wb')
    handler_ks_change.write(string_pre.encode())
    handler_ks_change.close()
    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_ubuntu(os_version, os_string_version, os_bit, bios_mode, ipaddress_dhcp, mac_net_pxe,
                                         mac_boot_device_rhel6)
        for item in data_menu:
            file_menu.write(item.encode())

    # upload menu file & ks
    remote_path_menu = ''
    if bios_mode == "legacy":
        remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/', mac_boot_device_rhel6 + ".cfg")
    elif bios_mode == "uefi":
        remote_path_menu = os.path.join(r'/opt/config/', mac_boot_device_rhel6 + ".cfg")

    upload_menu = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        try:
            # upload_menu
            sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
            # upload_ks
            sftp_upload_ks.put(localpath=local_path_ks, remotepath=os.path.join(remote_path_ks, filename_ks_local_rhel))
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
            flag_status = 0
            message_info = "同dhcp沟通出现问题，请检查！"
            return flag_status, message_info
        finally:
            sftp_upload_ks.close()
            upload_menu.close()
        # generate uefi menu for remote server
        if bios_mode == "uefi":
            ssh_gen_uefi_menu = paramiko.SSHClient()
            try:
                ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp,
                                          password=password_dhcp)
                ssh_gen_uefi_menu.exec_command(
                    command='cp /opt/config/grub-generate.sh /opt/config/{}.sh'.format(mac_boot_device_rhel6))
                ssh_gen_uefi_menu.exec_command(
                    command='/opt/config/{mac}.sh {mac}'.format(
                        mac=mac_boot_device_rhel6))
            except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                flag_status = 0
                message_info = "无法连接至DHCP服务器，请检查网络连接！"
                return flag_status, message_info
            finally:
                ssh_gen_uefi_menu.close()
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
        flag_status = 0
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        return flag_status, message_info
    finally:
        upload_menu.close()
        os.remove(local_path_ks)
        os.remove(local_path_menu)
    flag_status = 1
    message_info = "KS文件产生成功！"
    return flag_status, message_info


def generate_ks_windows(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit):
    filename_menu_to_gen = mac_net_pxe_temp + "-menu.cfg"
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_windows(os_version, os_sub_version, os_bit, bios_mode, ipaddress_windows)
        for item in data_menu:
            file_menu.write(item.encode())

    # upload menu file & ks
    remote_path_menu = ''
    if bios_mode == "legacy":
        remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/',
                                        mac_boot_device_rhel6 + ".cfg")
    elif bios_mode == "uefi":
        remote_path_menu = os.path.join(r'/var/www/html/ipxe-uefi.cfg/',
                                        mac_boot_device_rhel6 + ".efi")
    upload_menu = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
    try:
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        try:
            # upload_menu
            sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
        except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
            flag_status = 0
            message_info = "同DHCP服务器连接出现问题，请检查！"
            return flag_status, message_info
        finally:
            sftp_upload_ks.close()
        upload_menu.close()
    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
        flag_status = 0
        message_info = "无法连接至DHCP服务器，请检查网络连接！"
        return flag_status, message_info
    finally:
        upload_menu.close()
        os.remove(local_path_menu)

    flag_status = 1
    message_info = "成功生成KS文件！"
    return flag_status, message_info


def config_pxe(request):
    if request.method == "POST":
        if "gen_os_ver" in request.POST:
            os_type = request.POST.get('os_type', '')
            mac_add = request.POST.get('mac_add', '')
            if os_type == 'redhat':
                os_version_list = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '6.10', '7.0', '7.1', '7.2', '7.3', '7.4',
                                   '7.5', '7.6', '8.0']
            elif os_type == 'centos':
                os_version_list = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0', '7.1', '7.2', '7.3', '7.4', '7.5',
                                   '7.6']
            elif os_type == 'suse':
                os_version_list = ['11.2', '11.3', '11.4', '12.0', '12.1', '12.2', '12.3', '12.4']
            elif os_type == 'ubuntu':
                os_version_list = ['14.04.5', '15.10', '16.04', '16.10', '17.04', '17.10']
            elif os_type == 'windows':
                os_version_list = ['2016-datacenter-cn', '2016-datacenter-en', '2016-standard-en', '2016-standard-cn',
                                   '2012r2-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn',
                                   '2012r2-standard-cn']
            else:
                os_version_list = ['None']
            os_type_list_temp = []
            os_type_list_temp.append(os_type)
            return render(request, "pxe/html.html",
                          {'os_type_list': os_type_list_temp, 'os_version_list': os_version_list,
                           'bios_mode_list': bios_ver_list, 'os_bit_list': os_bit_list,
                           'sys_disk_name_list': sys_disk_name_list, 'mac_add': mac_add})
        elif "gen_ks" in request.POST:
            messages_info_list = []
            os_version = request.POST.get('os_type', '').strip()
            os_sub_version = request.POST.get('os_version', '').strip()
            bios_mode = request.POST.get('bios_mode', '').strip()
            os_bit = request.POST.get('os_bit', '').strip()
            os_disk = request.POST.get('sys_disk_name', '').strip()
            mac_net_pxe_temp = request.POST.get('mac_add', '').strip()
            mac_boot_device_rhel6 = re.sub(r'-', ':', mac_net_pxe_temp.lower())

            if len(mac_net_pxe_temp) == 0:
                flag_ks_status = 0
                message_info = "MAC地址未输入！请重新配置！"
                messages.error(request, message_info)
                return render(request, "pxe/html.html", {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                                         'os_bit_list': os_bit_list,
                                                         'sys_disk_name_list': sys_disk_name_list,
                                                         'mac_add': mac_net_pxe_temp})
            else:
                if len(os_sub_version) == 0:
                    message_info = "OS版本未选择！请重新配置"
                    messages.error(request, message_info)
                    return render(request, "pxe/html.html",
                                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                   'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                   'mac_add': mac_net_pxe_temp})

                else:
                    if os_version == "redhat" or os_version == "centos":
                        flag_status, message_info = generate_ks_redhat_centos(os_version, os_sub_version,
                                                                              mac_net_pxe_temp, mac_boot_device_rhel6,
                                                                              bios_mode, os_bit, os_disk)
                        messages_info_list.append(message_info)
                        if flag_status == 1:
                            return render(request, "pxe/show_success.html", {'messages_success': messages_info_list})
                        elif flag_status == 0:
                            return render(request, "pxe/html.html",
                                          {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                           'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                           'messages': messages_info_list, 'mac_add': mac_net_pxe_temp})
                    elif os_version == "suse":
                        flag_status, message_info = generate_ks_suse(os_version, os_sub_version, mac_net_pxe_temp,
                                                                     mac_boot_device_rhel6, bios_mode, os_bit, os_disk)
                        messages_info_list.append(message_info)
                        if flag_status == 1:
                            return render(request, "pxe/show_success.html", {'messages_success': messages_info_list})
                        elif flag_status == 0:
                            return render(request, "pxe/html.html",
                                          {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                           'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                           'messages': messages_info_list, 'mac_add': mac_net_pxe_temp})
                    elif os_version == "ubuntu":
                        flag_status, message_info = generate_ks_ubuntu(os_version, os_sub_version, mac_net_pxe_temp,
                                                                       mac_boot_device_rhel6, bios_mode, os_bit,
                                                                       os_disk)
                        messages_info_list.append(message_info)
                        if flag_status == 1:
                            return render(request, "pxe/show_success.html", {'messages_success': messages_info_list})
                        elif flag_status == 0:
                            return render(request, "pxe/html.html",
                                          {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                           'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                           'messages': messages_info_list, 'mac_add': mac_net_pxe_temp})
                    elif os_version == "windows":
                        flag_status, message_info = generate_ks_windows(os_version, os_sub_version, mac_net_pxe_temp,
                                                                        mac_boot_device_rhel6, bios_mode, os_bit)
                        messages_info_list.append(message_info)
                        if flag_status == 1:
                            return render(request, "pxe/show_success.html",
                                          {'messages_success': messages_info_list, 'mac_add': mac_net_pxe_temp})
                        elif flag_status == 0:
                            return render(request, "pxe/html.html",
                                          {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                           'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                           'messages': messages_info_list, 'mac_add': mac_net_pxe_temp})
                    else:
                        pass
        elif "del_ks" in request.POST:
            os_version = request.POST.get('os_type', '').strip()
            bios_mode = request.POST.get('bios_mode', '').strip()
            mac_net_pxe_temp = request.POST.get('mac_add', '').strip()
            mac_net_pxe = mac_net_pxe_temp.strip().upper()
            mac_boot_device_rhel6 = re.sub(r'-', ':', mac_net_pxe_temp.lower())
            filename_pre_remove = "".join(mac_boot_device_rhel6.split(":"))

            if len(mac_net_pxe_temp) == 0:
                message_info = "MAC地址未输入！请重新配置！"
                messages.error(request, message_info, )
                return render(request, "pxe/html.html",
                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
            else:
                filename_ks = "{}.*".format(mac_net_pxe)
                try:
                    ssh_del_ks = paramiko.SSHClient()
                    ssh_del_ks.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_del_ks.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                    if bios_mode == "uefi":
                        ssh_del_ks.exec_command(
                            command='rm -rf /var/www/html/ipxe-uefi.cfg/{}.efi'.format(mac_boot_device_rhel6))
                        if os_version != "windows":
                            ssh_del_ks.exec_command(command='rm -rf /opt/config/{}.sh'.format(mac_boot_device_rhel6))
                            ssh_del_ks.exec_command(command='rm -rf /opt/config/{}.cfg'.format(mac_boot_device_rhel6))
                    elif bios_mode == "legacy":
                        ssh_del_ks.exec_command(
                            command='rm -rf /var/www/html/ipxe-legacy.cfg/{}.cfg'.format(mac_boot_device_rhel6))
                    # if os_version != "windows":
                    ssh_del_ks.exec_command(command='rm -rf /var/www/html/ks/ks_all/{}'.format(filename_ks))
                    ssh_del_ks.exec_command(command='rm -rf /var/www/html/ks/ks_all/{}'.format(filename_pre_remove))
                    ssh_del_ks.close()
                    message_info = "KS文件从服务器删除成功"
                    messages_info_list = [message_info]
                    messages.error(request, message_info)
                    return render(request, "pxe/show_success.html", {'messages_success': messages_info_list})
                except TimeoutError:
                    message_info = "TFTP服务器连接失败！请检查网络连接！"
                    messages.error(request, message_info, )
                    return render(request, "pxe/html.html",
                                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                   'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list,
                                   'mac_add': mac_net_pxe_temp})


def search(request):
    if request.method == "POST":
        if "search" in request.POST:
            clientdic_ip_mac = {}
            clientdic_mac_ip = {}
            key_ip_mac = request.POST.get('search_input', '').strip()
            if len(key_ip_mac) == 0:
                message_info = "输入空白！请重新输入"
                messages.error(request, message_info, )
                return render(request, "pxe/html.html",
                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
            else:
                if os.path.exists("dhcpd.leases"):
                    os.remove("dhcpd.leases")
                remote_path = r'/var/lib/dhcpd/dhcpd.leases'
                local_path = os.path.join(os.getcwd(), r'dhcpd.leases')
                try:
                    get_dhcp = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
                    get_dhcp.connect(username=username_dhcp, password=password_dhcp)
                    sftp = paramiko.SFTPClient.from_transport(get_dhcp)
                    sftp.get(localpath=local_path, remotepath=remote_path)
                    sftp.close()
                    get_dhcp.close()
                    try:
                        with open(local_path, 'r') as file_dhcp:
                            contents_temp = file_dhcp.readlines()
                            contents_list = [item for item in contents_temp]
                            contents = "".join(contents_list)
                            # for item_ip_mac in contents:
                            group = re.findall(r'lease\s(\d+.\d+.\d+.\d+)\s.*?ethernet\s(.+?);', contents, re.DOTALL)
                            for each in group:
                                ipaddr = each[0]
                                macaddr_temp = each[1]
                                macaddr = re.sub(r':', '-', macaddr_temp)
                                clientdic_ip_mac[ipaddr] = macaddr.upper()
                                clientdic_mac_ip[macaddr.upper()] = ipaddr
                    except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                        message_info = "DHCP服务器信息下载失败！请检查网络连接！"
                        messages.error(request, message_info, )
                        return render(request, "pxe/html.html",
                                      {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                       'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                    message_info = "无法连接至DHCP服务器，请检查网络连接！"
                    messages.error(request, message_info, )
                    return render(request, "pxe/html.html",
                                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                   'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                try:
                    os.remove(local_path)
                except Exception:
                    pass
                ipdict_ip_mac = clientdic_ip_mac
                ipdict_mac_ip = clientdic_mac_ip

                if key_ip_mac in ipdict_ip_mac:
                    content = key_ip_mac + "  :  " + ipdict_ip_mac[key_ip_mac]
                    ip_mac_string = content
                    print(ip_mac_string)
                elif key_ip_mac.upper() in ipdict_mac_ip:
                    content = ipdict_mac_ip[key_ip_mac.upper()] + "    :    " + key_ip_mac.upper()
                    ip_mac_string = content
                    print(ip_mac_string)
                elif ("-".join(key_ip_mac.split(":"))).upper() in ipdict_mac_ip:
                    content = ipdict_mac_ip[("-".join(key_ip_mac.split(":"))).upper()] + "    :    " + (
                        "-".join(key_ip_mac.split(":"))).upper()
                    ip_mac_string = content
                    print(ip_mac_string)
                else:
                    ip_mac_string = 'No result match! Please check the input!'
            return render(request, "pxe/html.html", {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                                     'os_bit_list': os_bit_list,
                                                     'sys_disk_name_list': sys_disk_name_list,
                                                     'ip_mac_string': ip_mac_string})
        elif "view_all" in request.POST:
            show_string_list = []

            if os.path.exists("dhcpd.leases"):
                os.remove("dhcpd.leases")
            remote_path = r'/var/lib/dhcpd/dhcpd.leases'
            local_path = os.path.join(os.getcwd(), r'dhcpd.leases')
            try:
                get_dhcp = paramiko.Transport('{}:22'.format(ipaddress_dhcp))
                get_dhcp.connect(username=username_dhcp, password=password_dhcp)
                sftp = paramiko.SFTPClient.from_transport(get_dhcp)
                sftp.get(localpath=local_path, remotepath=remote_path)
                sftp.close()
                get_dhcp.close()
                try:
                    with open(local_path, 'r') as file_dhcp:
                        contents_temp = file_dhcp.readlines()
                        contents_list = [item for item in contents_temp]
                        contents = "".join(contents_list)
                        # for item_ip_mac in contents:
                        group = re.findall(r'lease\s(\d+.\d+.\d+.\d+)\s.*?ethernet\s(.+?);', contents, re.DOTALL)
                        list_already_done = []
                        for each in group:
                            ipaddr = each[0]
                            macaddr_temp = each[1]
                            macaddr = re.sub(r':', '-', macaddr_temp)
                            show_string_temp = ipaddr + ": " + macaddr
                            if macaddr not in list_already_done:
                                list_already_done.append(macaddr)
                                show_string_list.append(show_string_temp)
                except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                    message_info = "DHCP服务器信息下载失败！请检查网络连接！"
                    messages.error(request, message_info, )
                    return render(request, "pxe/html.html",
                                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                   'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
            except (IOError, TimeoutError, paramiko.ssh_exception.SSHException, paramiko.SSHException):
                message_info = "无法连接至DHCP服务器，请检查网络连接！"
                messages.error(request, message_info, )
                return render(request, "pxe/html.html",
                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})

            try:
                os.remove(local_path)
            except Exception:
                pass
            show_string_list_list = sorted(show_string_list)
            show_string = "\r\n".join(show_string_list_list)
            return render(request, "pxe/html.html", {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                                     'os_bit_list': os_bit_list,
                                                     'sys_disk_name_list': sys_disk_name_list,
                                                     'ip_mac_string': show_string})
        else:
            pass
    return render(request, "pxe/html.html",
                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list, 'os_bit_list': os_bit_list,
                   'sys_disk_name_list': sys_disk_name_list})


def set_pxe_reboot(request):
    if request.method == "POST":
        if "set_pxe" in request.POST:
            username_bmc = request.POST.get('bmc_user', '').strip()
            password_bmc = request.POST.get('bmc_passwd', '').strip()
            bmcip = request.POST.get('bmc_ip', '').strip()
            if len(bmcip) is not 0 and len(username_bmc) is not 0 and len(password_bmc) is not 0:
                run_ipmitool = subprocess.Popen(
                    "ipmitool -I lanplus -H {} -U {} -P {} chassis bootdev pxe".format(bmcip, username_bmc,
                                                                                       password_bmc), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                run_ipmitool.wait()
                if run_ipmitool.returncode != 0:
                    message_info = "PXE启动设置失败！请检查输入！"
                    messages.error(request, message_info, )
                    return render(request, "pxe/html.html",
                                  {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                   'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                else:
                    check_power_status = subprocess.Popen(
                        "ipmitool -I lanplus -H {} -U {} -P {} chassis power status".format(
                            bmcip, username_bmc, password_bmc), shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    check_power_status.wait()
                    if check_power_status.returncode != 0:
                        message_info = "服务器开关机状态获取失败！请检查BMC设置和连接！"
                        messages.error(request, message_info, )
                        return render(request, "pxe/html.html",
                                      {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                       'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                    else:
                        power_status = check_power_status.stdout.readlines()[0].decode().split(" ")[3].strip()
                        if power_status == "on":
                            set_power_reset = subprocess.Popen(
                                "ipmitool -I lanplus -H {} -U {} -P {} chassis power reset".format(
                                    bmcip, username_bmc, password_bmc), shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
                            set_power_reset.wait()
                            if set_power_reset.returncode != 0:
                                message_info = "服务器重启失败！请检查BMC连接状态！"
                                messages.error(request, message_info, )
                                return render(request, "pxe/html.html",
                                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                            else:
                                message_info = "服务器重启成功"
                                messages.error(request, message_info, )
                                return render(request, "pxe/html.html",
                                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                        elif power_status == "off":
                            set_power_on = subprocess.Popen(
                                "ipmitool -I lanplus -H {} -U {} -P {} chassis power on".format(bmcip, username_bmc,
                                                                                                password_bmc),
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            set_power_on.wait()
                            if set_power_on.returncode != 0:
                                message_info = "服务器开机失败！请检查BMC连接状态！"
                                messages.error(request, message_info, )
                                return render(request, "pxe/html.html",
                                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
                            else:
                                message_info = "服务器启动成功"
                                messages.error(request, message_info, )
                                return render(request, "pxe/html.html",
                                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
            else:
                message_info = "请输入BMC的用户名、密码、IP地址!"
                messages.error(request, message_info, )
                return render(request, "pxe/html.html",
                              {'os_type_list': os_type_list, 'bios_mode_list': bios_ver_list,
                               'os_bit_list': os_bit_list, 'sys_disk_name_list': sys_disk_name_list})
        else:
            pass
