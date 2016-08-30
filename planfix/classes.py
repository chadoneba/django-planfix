import requests
from hashlib import md5
from xml.etree import ElementTree
from django.core.cache import cache

# class Cache(object):
#     params = {}
#
#     def get(self,key):
#         if self.params.has_key(key):
#             return self.params[key]
#         else:
#             return None
#
#     def set(self,key,value,timeout):
#         self.params[key] = value
#
#
# cache = Cache()


class PlanFixBase(object):
    CACHE_TIMELIFE = 20
    request_templ = """<?xml version="1.0" encoding="UTF-8"?>
        <request method="{}">
          {}
          <signature>{}</signature>
        </request>
        """

    name = ''
    scheme = []
    sign = ''

    host = ""
    api_key = ""
    private_key = ""
    project_id = ""
    user = ""
    password = ""
    account = ""
    level = 0
    sid = None

    def __init__(self,*args,**kwargs):
        self.sid = cache.get('planfix_sid')
        attr_list = [i.__str__() for i in dir(self) if not i.startswith('__')]
        if kwargs:
            for item in kwargs.keys():
                if item in attr_list:
                    self.__setattr__(item,kwargs[item])
        if not self.sid:
            self.auth()

    def scheme_sort(self,a,b):
        tmp_a = a.keys()[0] if isinstance(a,dict) else a
        tmp_b = b.keys()[0] if isinstance(b,dict) else b
        if tmp_a == tmp_b: return 0
        if tmp_a > tmp_b:
            return 1
        else:
            return -1

    def get_sign(self,**kwargs):
        params_list = self.name + self.string_by_schemefileds(self.scheme,**kwargs) + self.private_key
        self.sign = md5(params_list.encode('utf-8')).hexdigest()

    def string_by_schemefileds(self,element,**kwargs):
        result_list = []
        element = list(element)
        element.sort(cmp=self.scheme_sort)
        for item in element:
            if not isinstance(item, dict):
                tmp_item = self.get_value(item,)
                result_list.append(self.get_value(item, **kwargs))
            else:
                tmp_key, tmp_val = item.items()[0]
                if not isinstance(tmp_val, list):
                    if tmp_val == 'id':
                        result_list.append(self.get_value(tmp_key, **kwargs))
                    elif tmp_val == 'customValue':
                        res = self.get_value(tmp_key, **kwargs)
                        if not res == '' and isinstance(res, list):
                            result_list.append("".join(["".join([str(i[0]),i[1]]) for i in res]))
                    else:
                        result_list.append(self.get_value(tmp_val, **kwargs))
                else:
                    result_list.append(self.string_by_schemefileds(tmp_val, **kwargs))
        return "".join(result_list)

    def get_value(self,value, **kwargs):
        if kwargs.has_key(value):
            return kwargs.get(value)
        return ''

    def create_xml_by_scheme(self,element, **kwargs):
        result = ""
        template = "<%s>%s</%s>"
        custom_data_template = "<id>%s</id><value>%s</value>"
        for item in element:
            if not isinstance(item, dict):
                result += template % (item, self.get_value(item, **kwargs), item)
            else:
                tmp_key, tmp_val = item.items()[0]
                if not isinstance(tmp_val, list):
                    if tmp_val == 'id':
                        sub_result = template % (tmp_val, self.get_value(tmp_key, **kwargs), tmp_val)
                    elif tmp_val == 'customValue':
                        res = self.get_value(tmp_key, **kwargs)
                        if not res == '' and isinstance(res,list):
                            sub_result = "".join([template % (tmp_val,(custom_data_template % i),tmp_val) for i in res])
                    else:
                        sub_result = template % (tmp_val, self.get_value(tmp_key, **kwargs), tmp_val)
                else:
                    sub_result = self.create_xml_by_scheme(tmp_val, **kwargs)
                result += template % (tmp_key, sub_result, tmp_key)
        return result

    def connect(self,**kwargs):
        if not kwargs.has_key('sid') and self.sid:
            kwargs['sid'] = self.sid
        self.get_sign(**kwargs)
        body = self.create_xml_by_scheme(self.scheme, **kwargs)
        data = self.request_templ.format(self.name,body.encode('utf-8'),self.sign)
        r = requests.post(self.host, data=data, auth=(self.api_key, ""))
        if self.name != 'auth.login':
            if self.is_session_valid(r.content):
                return r.content
            else:
                tmp_params = dict(name=self.name,scheme=self.scheme)
                self.auth(renew=True)
                self.scheme,self.name = tmp_params['scheme'],tmp_params['name']
                return self.connect(**kwargs)
        else:
            return r.content

    def is_session_valid(self,res):
        response = ElementTree.fromstring(res)
        if response.attrib['status'] == 'ok':
            return True
        else:
            if response.find('code').text == '0005':
                return False
            else:
                raise AttributeError(response.find('code').text)


    def auth(self,renew=False):
        if renew or self.sid == None:
            self.name = 'auth.login'
            self.scheme = \
                [ 'account'
                , 'login'
                , 'password'
                 ]
            params = \
                { 'account':self.account
                , 'login':self.user
                , 'password':self.password
                }
            response = ElementTree.fromstring(self.connect(**params))
            res = response.find('sid')
            self.sid = res.text
            cache.set('planfix_sid',self.sid,self.CACHE_TIMELIFE*60)