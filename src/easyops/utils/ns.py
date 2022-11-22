# -*- coding: utf-8 -*-
import ctypes


class NameService(object):
    IP_LENGTH = 64
    dylib = None

    def __init__(self):
        self._init()

    @classmethod
    def _init(cls):
        if cls.dylib:
            return

        try:
            dll_path = "/usr/local/easyops/ens_client/sdk/libens_sdk.so"
            cls.dylib = ctypes.CDLL(dll_path)
        except Exception as _:
            del _
            try:
                dll_path = "/usr/local/easyops/ens_client/sdk/libens_sdk.dylib"
                cls.dylib = ctypes.CDLL(dll_path)
            except Exception as _:
                del _
                dll_path = "/usr/local/lib/libens_sdk.dylib"
                cls.dylib = ctypes.CDLL(dll_path)

        cls.dylib.get_service_by_name.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                                  ctypes.POINTER(ctypes.c_int)]
        cls.dylib.get_service_by_name.restype = ctypes.c_int64

        cls.dylib.report_stat.argtypes = [ctypes.c_int64, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
                                          ctypes.c_char_p]

    def get_service_by_name(self, src_name, dst_name):
        """
        :param src_name: src
        :param dst_name: dst
        :return:session_id
        """
        out_ip = ctypes.create_string_buffer(b"", self.IP_LENGTH)
        out_port = ctypes.c_int()
        src_name = ctypes.create_string_buffer(src_name.encode())
        dst_name = ctypes.create_string_buffer(dst_name.encode())

        session_id = self.dylib.get_service_by_name(src_name, dst_name, out_ip, self.IP_LENGTH, ctypes.byref(out_port))
        return session_id, out_ip.raw.rstrip(b"\x00").decode(), out_port.value

    def get_all_service_by_name(self, src_name, dst_name):
        """
        批量通过名字拉IP和端口
        :param src_name:主调服务名字
        :param dst_name:被调服务名字
        :return:session_id 小于0为失败
                host_list   主机IP:端口列表
        """
        num = 4096
        self.dylib.get_multi_service_by_name_ip_len_64.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.ARRAY(ctypes.ARRAY(ctypes.c_char, self.IP_LENGTH), num),
            ctypes.ARRAY(ctypes.c_int, num),
            ctypes.POINTER(ctypes.c_int)]
        self.dylib.get_multi_service_by_name_ip_len_64.restype = ctypes.c_int64

        out_ip_arr = ((ctypes.c_char * self.IP_LENGTH) * num)()
        out_port_arr = (ctypes.c_int * num)()
        out_num = ctypes.c_int(num)
        session_id = self.dylib.get_multi_service_by_name_ip_len_64(src_name, dst_name, out_ip_arr, out_port_arr,
                                                                    out_num)
        if session_id <= 0:
            return session_id, []

        host_list = []
        for idx in range(out_num.value):
            host = "{ip}:{port}".format(ip=out_ip_arr[idx].value, port=out_port_arr[idx])
            host_list.append(host)

        return session_id, host_list

    def report_stat(self, session_id, dst_interface, ret_code, delay, code_point="", err_stack=""):
        """
        调用服务是否成功接口
        :param session_id: get_service_by_name返回的session_id
        :param dst_interface: 被调接口名
        :param ret_code: 接口调用的返回码，0为成功
        :param delay: 接口调用延时(毫秒)
        :param code_point: 代码位置
        :param err_stack: 错误堆栈
        :return: ret_code:  返回码，0为成功
        """
        ret_code = self.dylib.report_stat(session_id, dst_interface, ret_code, delay, code_point, err_stack)
        return ret_code
