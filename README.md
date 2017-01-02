# nasne

nasne is a python package to get information from nasne.
This package is greatly inspired by [node-nasne](https://github.com/naokiy/node-nasne).

## How to use

```python
import nasne
nasne = Nasne(<ip to nasne>)
nasne.get_software_version()
# => {u'errorcode': 0, u'backdatedVersion': u'0000', u'softwareVersion': u'0251'}
```

## Supported methods
  - `check_update`
  - `check_update2`
  - `get_area_info`
  - `get_bcas_info`
  - `get_box_name`
  - `get_box_status_list`
  - `get_curr_date`
  - `get_dlna_media_server_icon`
  - `get_dlna_media_server_icon_list`
  - `get_dmp_auto_register_info`
  - `get_dmp_list`
  - `get_downloading_permission`
  - `get_dtcpip_client_list`
  - `get_event_relay_info`
  - `get_hdd_list`
  - `get_hdd_power_saving_mode`
  - `get_matching_id_info`
  - `get_mobile_bitrate_info`
  - `get_nas_info`
  - `get_nas_meta_data_analyze_progress`
  - `get_network_if_info`
  - `get_outdoor_client_list2`
  - `get_parental_rating_info`
  - `get_parental_rating_password`
  - `get_rec_ng_list`
  - `get_reconstruct_database_progress`
  - `get_register_request_list`
  - `get_registerd_folder_name_by_receiver`
  - `get_remote_list`
  - `get_request_client_info`
  - `get_reserved_folder_name_by_initiator`
  - `get_reserved_info_bitrate`
  - `get_software_version`
  - `get_sync_dtv_tuner_list2`
  - `get_tot_status`
  - `setup_is_finish`
