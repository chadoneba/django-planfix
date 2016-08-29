from classes import PlanFixBase
from xml.etree import ElementTree


class PlanFix(PlanFixBase):
    def add_task(self, *args, **kwargs):
        self.name = "task.add"
        self.scheme = \
            ['account'
                , 'sid'
                , {'task': \
                       ['template'
                           , 'title'
                           , 'description'
                           , 'importance'
                           , 'status'
                           , {'owner':'id'}
                           , 'statusSet'
                           , 'checkResult'
                           , {'project': 'id'}
                           , 'startDateIsSet'
                           , 'startDate'
                           , 'startTimeIsSet'
                           , 'startTime'
                           , 'endDateIsSet'
                           , 'endDate'
                           , 'endTimeIsSet'
                           , 'endTime'
                           , {'customData':'customValue'}
                        ]
                   }
             ]

        try:
            self.connect(**kwargs)
        except AttributeError as e:
            print e.message

    def change_status_task(self, id, status):
        self.name = ""
        self.scheme = []

    def project_get_list(self,cur_page=1,target='all'):
        result = []
        if not str(cur_page).isdigit():
            cur_page = 1
        self.name = 'project.getList'
        self.scheme = \
            {
                'account'
                , 'sid'
                , 'pageCurrent'
                , 'target'
            }
        params = \
            { 'account':self.account
            , 'sid':self.sid
            , 'pageCurrent':str(cur_page)
            , 'target':target
            }
        try:
            response = ElementTree.fromstring(self.connect(**params))
            rt = response.find('projects')
            for item in rt:
                result.append((item.find('id').text,item.find('title').text))
            return result
        except AttributeError as e:
            print e.message

    def contact_get_list(self,cur_page=1):
        result = []
        if not str(cur_page).isdigit():
            cur_page = 1
        self.name = 'contact.getList'
        self.scheme = \
            {
              'account'
            , 'sid'
            , 'pageCurrent'
            , 'pageSize'
            }
        params = \
            { 'account': self.account
            , 'sid': self.sid
            , 'pageCurrent': str(cur_page)
            , 'pageSize': '100'
             }
        try:
            response = ElementTree.fromstring(self.connect(**params))
            rt = response.find('contacts')
            total = rt.attrib['totalCount']
            for item in rt:
                result.append((item.find('userid').text, item.find('email').text))
            return result
        except AttributeError as e:
            print e.message

    def contact_add(self,**kwargs):
        result = []
        self.name = 'contact.add'
        self.scheme = \
            ['account'
                , 'sid'
                , {'contact': \
                       [  'template'
                        , 'name'
                        , 'lastName'
                        , 'post'
                        , 'email'
                        , 'mobilePhone'
                        , 'workPhone'
                        , 'homePhone'
                        , 'address'
                        , 'description'
                        , 'sex'
                        , 'skype'
                        , 'icq'
                        , 'birthdate'
                        , 'lang'
                        , 'isCompany'
                        , 'canBeWorker'
                        , 'canBeClient'
                        ]
                   }
             ]

        try:
            response = ElementTree.fromstring(self.connect(**kwargs))
            return [(response.find('contact').find('id').text,response.find('contact').find('general').text)]
        except AttributeError as e:
            print e.message

    def task_get_list(self,target='template'):
        result = []
        self.name = 'task.getList'
        self.custom_scheme = []
        self.scheme = \
            {
                'account'
                , 'sid'
                , 'target'
                , 'pageCurrent'
            }
        params = \
            {'account': self.account
                , 'sid': self.sid
                , 'pageCurrent': '1'
                , 'target': target
             }
        try:
            response = ElementTree.fromstring(self.connect(**params))
            rt = response.find('tasks')
            for item in rt:
                result.append((item.find('id').text,item.find('title').text))
            return result
        except AttributeError as e:
            print e.message

