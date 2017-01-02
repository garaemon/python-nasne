#!/usr/bin/env python
'''Library for nasne API over http protocol.

nasne.py library provides Nasne class as a wrapper of
nasne API.
'''

import logging
import sys

import coloredlogs
import requests


class NasneRequestException(Exception):
    'Exception class which is raised when failed to call API'
    pass


class EndPoint(object):
    'Simple class to store endpoint information'

    def __init__(self, method, port, path):
        '''Create EndPoint instance.

        Arguments:
        - method: GET or POST
        - port: integer number of port.
        - path: path to endpoint such as '/status/areaInfoGet'
        '''
        self.method = method
        self.port = port
        self.path = path

# Dictionary of method_name and EndPoint instance.
NASNE_URL_ENDPOINTS = {
    'get_channel_logo_data': EndPoint('GET', 64210, '/chEpg/channelLogoDataGet'),
    'get_epg': EndPoint('POST', 64210, '/chEpg/EPGGet'),
    'start_epg_store': EndPoint('POST', 64210, '/chEpg/EPGStoreStart'),
    'get_connection_online_id': EndPoint('GET', 64210, '/cma/connectionOnlineIdGet'),
    'get_reconstruct_database_progress':
        EndPoint('GET', 64210, '/cma/reconstructDatabaseProgressGet'),
    'get_reconstruct_database_prograss':
        EndPoint('GET', 64210, '/config/reconstructDatabaseProgressGet'),
    'get_nas_meta_data_analyze_progress':
        EndPoint('GET', 64210, '/config/NASMetaDataAnalyzeProgressGet'),
    'get_title_list': EndPoint('GET', 64220, '/recorded/titleListGet'),
    'get_recorded_content_thumbnail':
        EndPoint('GET', 64210, '/recorded/recordedContentThumbnailGet'),
    'get_matching_id_info': EndPoint('GET', 64210, '/remoteAccess/dr/matchingIdInfoGet'),
    'get_outdoor_client_list2':
        EndPoint('GET', 64210, '/remoteAccess/dr/outdoorClientListGet2'),
    'get_register_request_list':
        EndPoint('GET', 64210, '/remoteAccess/dr/registerRequestListGet'),
    'get_registerd_folder_name_by_receiver':
        EndPoint('GET', 64210, '/remoteAccess/sync/registerdFolderNameGetByReceiver'),
    'get_reserved_folder_name_by_initiator':
        EndPoint('GET', 64210, '/remoteAccess/sync/reservedFolderNameGetByInitiator'),
    'get_sync_dtv_tuner_list2':
        EndPoint('GET', 64210, '/remoteAccess/sync/syncDTVTunerListGet_2'),
    'get_conflict_list': EndPoint('GET', 64220, '/schedule/conflictListGet'),
    'get_reserved_info_bitrate': EndPoint('GET', 64220, '/schedule/reservedInfoBitrateGet'),
    'create_reserved_info': EndPoint('POST', 64220, '/schedule/reservedInfoCreate'),
    'delete_reserved_info': EndPoint('POST', 64220, '/schedule/reservedInfoDelete'),
    'get_reserved_list': EndPoint('GET', 64220, '/schedule/reservedListGet'),
    'get_area_info': EndPoint('GET', 64210, '/status/areaInfoGet'),
    'get_bcas_info': EndPoint('GET', 64210, '/status/BCASInfoGet'),
    'get_box_name': EndPoint('GET', 64210, '/status/boxNameGet'),
    'get_box_status_list': EndPoint('GET', 64210, '/status/boxStatusListGet'),
    'get_bd_power_supply': EndPoint('GET', 64210, '/status/bdPowerSupplyGet'),
    'get_channel_physical_info': EndPoint('GET', 64210, '/status/channelPhysicalInfoGet'),
    'get_end_of_channel_physical_info':
        EndPoint('POST', 64210, '/status/channelPhysicalInfoGetEnd'),
    'get_start_of_channel_physical_info':
        EndPoint('POST', 64210, '/status/channelPhysicalInfoGetStart'),
    'get_channel_info': EndPoint('GET', 64210, '/status/channelInfoGet'),
    'get_channel_info2': EndPoint('GET', 64210, '/status/channelInfoGet2'),
    'get_channel_list': EndPoint('GET', 64210, '/status/channelListGet'),
    'get_curr_date': EndPoint('GET', 64210, '/status/currDateGet'),
    'get_dlna_media_server_icon': EndPoint('GET', 64210, '/status/DLNAMediaServerIconGet'),
    'get_dlna_media_server_icon_list': EndPoint('GET', 64210, '/status/DLNAMediaServerIconListGet'),
    'get_dmp_auto_register_info': EndPoint('GET', 64210, '/status/DMPAutoRegisterInfoGet'),
    'get_dmp_list': EndPoint('GET', 64210, '/status/DMPListGet'),
    'get_downloading_permission': EndPoint('GET', 64210, '/status/downloadingPermissionGet'),
    'get_dtcpip_client_list': EndPoint('GET', 64210, '/status/dtcpipClientListGet'),
    'get_epg_version_info': EndPoint('GET', 64210, '/status/EPGVersionInfoGet'),
    'get_event_relay_info': EndPoint('GET', 64210, '/status/eventRelayInfoGet'),
    'get_hdd_info': EndPoint('GET', 64210, '/status/HDDInfoGet'),
    'get_hdd_list': EndPoint('GET', 64210, '/status/HDDListGet'),
    'get_hdd_power_saving_mode': EndPoint('GET', 64210, '/status/HDDPowerSavingModeGet'),
    'setup_is_finish': EndPoint('GET', 64210, '/status/isFinishSetup'),
    'get_nas_info': EndPoint('GET', 64210, '/status/NASInfoGet'),
    'get_mobile_bitrate_info': EndPoint('GET', 64210, '/status/mobileBitrateInfoGet'),
    'get_network_if_info': EndPoint('GET', 64210, '/status/networkIfInfoGet'),
    'get_parental_rating_info': EndPoint('GET', 64210, '/status/parentalRatingInfoGet'),
    'get_parental_rating_password': EndPoint('GET', 64210, '/status/parentalRatingPasswordGet'),
    'get_rec_ng_list': EndPoint('GET', 64210, '/status/recNgListGet'),
    'get_remote_list': EndPoint('GET', 64210, '/status/remoteListGet'),
    'get_request_client_info': EndPoint('GET', 64210, '/status/requestClientInfoGet'),
    'get_software_version': EndPoint('GET', 64210, '/status/softwareVersionGet'),
    'get_tot_status': EndPoint('GET', 64210, '/status/TOTStatusGet'),
    'check_update': EndPoint('GET', 64210, '/status/updateCheck'),
    'check_update2': EndPoint('GET', 64210, '/status/updateCheck2')}


class Nasne(object):
    'Wrapper of nasne API.'

    def __init__(self, ip, endpoints=NASNE_URL_ENDPOINTS):
        '''Initialize nasne object based on ip address.

        Arguments:
        - ip: IP address of nasne.
        - endpoints: dictionary of method_name and EndPoint instance.
        '''
        self.ip = ip
        self.methods = []
        self.define_method_from_endpoints(endpoints)

    def define_method_from_endpoints(self, endpoints):
        '''Define methods according to endpoints

        Arguments:
        - endpoints: dictionary of method_name and EndPoint instance.
        '''
        for method_name, endpoint in endpoints.items():
            self.define_method_from_endpoint(method_name, endpoint)
            self.methods.append(method_name)

    def define_method_from_endpoint(self, method_name, endpoint):
        '''Define a method according to endpoint information.

        Arguments:
        - method_name: String of method name
        - endpoint: EndPoint instance.
        '''
        if endpoint.method == 'GET':
            setattr(self, method_name, self.create_get_method(endpoint))
        elif endpoint.method == 'POST':
            setattr(self, method_name, self.create_post_method(endpoint))

    def create_get_method(self, endpoint):
        '''Create lambda for GET api.

        Arguments:
        - endpoint: Intance of EndPoint

        Returns: lambda
        '''
        return lambda: self.call_api_get(endpoint.path, endpoint.port)

    def create_post_method(self, endpoint):
        '''Create lambda for POST api.

        Arguments:
        - endpoint: Intance of EndPoint

        Returns: lambda
        '''
        return lambda: self.call_api_post(endpoint.path, endpoint.port)

    def build_url_endpoint(self, endpoint_path, port):
        '''Return string of endpoint as full url.

        Aeguments:
        - endpoint_path: endpoint to url
        - port: port of the endpoint
        '''
        if endpoint_path.startswith('/'):
            return 'http://{}:{}{}'.format(self.ip, port, endpoint_path)
        else:
            return 'http://{}:{}/{}'.format(self.ip, port, endpoint_path)

    def call_api_get(self, path, port):
        '''Call nasne API with GET method and parse result as JSON.

        Arguments:
        - path: url path to endpoint.
        - port: port number of endpoint.

        Returns:
          JSON parsed as Dictionary object.

        Raises:
          NasneRequestException: raised when status code is not 200.
        '''
        url = self.build_url_endpoint(path, port)
        logging.info('call {}'.format(url))
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            raise NasneRequestException(
                'Failed to call GET api {}, status code: {}'.format(url, r.status_code))

    def call_api_post(self, path, port):
        '''Call nasne API with POST method and parse result as JSON.

        Arguments:
        - path: url path to endpoint.
        - port: port number of endpoint.

        Returns:
          JSON parsed as Dictionary object.

        Raises:
          NasneRequestException: raised when status code is not 200.
        '''
        url = self.build_url_endpoint(path, port)
        logging.info('call {}'.format(url))
        r = requests.post(url)
        if r.status_code == 200:
            return r.json()
        else:
            raise NasneRequestException(
                'Failed to call POST api {}, status code: {}'.format(url, r.status_code))


if __name__ == '__main__':
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES
    field_styles['levelname'] = {'color': 'white', 'bold': True}
    log_format = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
    coloredlogs.install(level=logging.INFO,
                        fmt=log_format,
                        field_styles=field_styles)
    if len(sys.argv) > 1:
        nasne = Nasne(sys.argv[1])
    else:
        nasne = Nasne('192.168.11.2')
    success_methods = []
    for method in nasne.methods:
        try:
            logging.info('{}: {}'.format(method, getattr(nasne, method)()))
            success_methods.append(method)
        except Exception as e:
            logging.error('Failed to call {}'.format(method))
    logging.info('success methods are: \n{}'.format(
        '\n'.join(['    ' + method for method in sorted(success_methods)])))
