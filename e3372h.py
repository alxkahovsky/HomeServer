# check author Github https://github.com/dubanoze/hilink
import requests
import logging
import xmltodict

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class Client:

    HOME_URL = 'http://{host}/html/home.html'
    API_URL = 'http://{host}/api/'

    def __init__(self, host='192.168.8.1'):
        self.home_url = self.HOME_URL.format(host=host)
        self.api_url = self.API_URL.format(host=host)
        self.session = requests.Session()
        self.connected = False

        try:
            self.session.get(self.home_url, timeout=(0.5, 0.5))
            self.connected = True
        except requests.exceptions.ConnectTimeout as e:
            self.connected = False
            print(e)

    def is_connected(f):
        def wrapper(self, *args, **kwargs):
            if self.connected is False:
                return None

            return f(self, *args, **kwargs)
        return wrapper

    @is_connected
    def _api_request(self, api_method_url):
        self._get_token()
        headers = {'__RequestVerificationToken': self.token}

        try:
            r = self.session.get(url=self.api_url + api_method_url,
                                 headers=headers,
                                 allow_redirects=False, timeout=(0.5, 0.5))
        except requests.exceptions.RequestException as e:
            return False

        if r.status_code != 200:
            return False

        resp = xmltodict.parse(r.text).get('error', None)
        if resp is not None:
            self.error_code = resp['code']
            return False

        resp = xmltodict.parse(r.text).get('response', None)
        if resp is not None:
            self.data = resp
            for key in resp:
                setattr(self, key, resp[key])
            return True

    @is_connected
    def _api_post(self, api_method_url, data):
        self._get_token()
        headers = {'__RequestVerificationToken': self.token}
        request = {}
        request['request'] = data
        try:
            r = self.session.post(url=self.api_url + api_method_url,
                                  data=xmltodict.unparse(request, pretty=True),
                                  headers=headers, timeout=(0.5, 0.5))
        except requests.exceptions.RequestException as e:
            return False

        if r.status_code != 200:
            return False

        resp = xmltodict.parse(r.text).get('error', None)
        if resp is not None:
            self.error_code = resp['code']
            return False

        return True

    @is_connected
    def _get_token(self):
        api_method_url = 'webserver/SesTokInfo'
        try:
            r = self.session.get(url=self.api_url + api_method_url,
                                 allow_redirects=False, timeout=(0.5, 0.5))

            self.token = xmltodict.parse(r.text)['response']['TokInfo']

        except requests.exceptions.RequestException as e:
            return False

        if r.status_code != 200:
            return False

        return r

    def _get_connection_status(self, status):
        statu = {}
        statu['2'] = 'Connection failed, the profile is invalid'
        statu['3'] = 'Connection failed, the profile is invalid'
        statu['5'] = 'Connection failed, the profile is invalid'
        statu['8'] = 'Connection failed, the profile is invalid'
        statu['20'] = 'Connection failed, the profile is invalid'
        statu['21'] = 'Connection failed, the profile is invalid'
        statu['23'] = 'Connection failed, the profile is invalid'
        statu['27'] = 'Connection failed, the profile is invalid'
        statu['28'] = 'Connection failed, the profile is invalid'
        statu['29'] = 'Connection failed, the profile is invalid'
        statu['30'] = 'Connection failed, the profile is invalid'
        statu['31'] = 'Connection failed, the profile is invalid'
        statu['32'] = 'Connection failed, the profile is invalid'
        statu['7'] = 'Network access not allowed'
        statu['11'] = 'Network access not allowed'
        statu['14'] = 'Network access not allowed'
        statu['37'] = 'Network access not allowed'
        statu['12'] = 'Connection failed, roaming not allowed'
        statu['13'] = 'Connection failed, bandwidth exceeded'
        statu['201'] = 'Connection failed, bandwidth exceeded'
        statu['900'] = 'Connecting'
        statu['901'] = 'Connected'
        statu['902'] = 'Disconnected'
        statu['903'] = 'Disconnecting'
        statu['904'] = 'Connection failed or disabled'
        return statu.get(status, 'n/a')

    def _get_network_type(self, nt):
        ntype = {}
        ntype['0'] = 'No Service'
        ntype['1'] = 'GSM'
        ntype['2'] = 'GPRS (2.5G)'
        ntype['3'] = 'EDGE (2.75G)'
        ntype['4'] = 'WCDMA (3G)'
        ntype['5'] = ''
        ntype['6'] = ''
        ntype['7'] = ''
        ntype['8'] = ''
        ntype['9'] = 'HSPA+ (4G)'
        ntype['10'] = ''
        ntype['11'] = ''
        ntype['12'] = ''
        ntype['13'] = ''
        ntype['14'] = ''
        ntype['15'] = ''
        ntype['16'] = ''
        ntype['17'] = ''
        ntype['18'] = ''
        ntype['19'] = ''
        ntype['41'] = ''
        ntype['44'] = ''
        ntype['45'] = ''
        ntype['46'] = ''
        ntype['64'] = ''
        ntype['65'] = ''
        ntype['101'] = ''
        return ntype.get(nt, 'n/a')

    def _get_roaming_status(self, status):
        statu = {}
        statu['0'] = 'Disabled'
        statu['1'] = 'Enabled'
        return statu.get(status, 'n/a')

    @is_connected
    def is_hilink(self):
        return self._api_request('device/basic_information')

    @is_connected
    def basic_info(self):
        '''
        <productfamily>LTE</productfamily>
        <classify>hilink</classify>
        <multimode>0</multimode>
        <restore_default_status>1</restore_default_status>
        <sim_save_pin_enable>0</sim_save_pin_enable>
        <devicename>E3372</devicename>
        '''
        self._api_request('device/basic_information')
        return self

    @is_connected
    def module_switch(self):
        '''
        <ussd_enabled>1</ussd_enabled>
        <bbou_enabled>1</bbou_enabled>
        <sms_enabled>1</sms_enabled>
        <sdcard_enabled>0</sdcard_enabled>
        <wifi_enabled>0</wifi_enabled>
        <statistic_enabled>1</statistic_enabled>
        <help_enabled>0</help_enabled>
        <stk_enabled>0</stk_enabled>
        <pb_enabled>1</pb_enabled>
        <dlna_enabled></dlna_enabled>
        <ota_enabled>0</ota_enabled>
        <wifioffload_enabled>0</wifioffload_enabled>
        <cradle_enabled>0</cradle_enabled>
        <multssid_enable>0</multssid_enable>
        <ipv6_enabled>0</ipv6_enabled>
        <monthly_volume_enabled>1</monthly_volume_enabled>
        <powersave_enabled>0</powersave_enabled>
        <sntp_enabled>0</sntp_enabled>
        <encrypt_enabled>1</encrypt_enabled>
        <dataswitch_enabled>0</dataswitch_enabled>
        <poweroff_enabled>0</poweroff_enabled>
        <ecomode_enabled>1</ecomode_enabled>
        <zonetime_enabled>0</zonetime_enabled>
        <localupdate_enabled>0</localupdate_enabled>
        <cbs_enabled>0</cbs_enabled>
        <qrcode_enabled>0</qrcode_enabled>
        <charger_enbaled>0</charger_enbaled>
        '''
        self._api_request('global/module-switch')
        return self

    @is_connected
    def coverged_status(self):
        '''
        <SimState>257</SimState>
        <SimLockEnable>0</SimLockEnable>
        <CurrentLanguage>ru-ru</CurrentLanguage>
        '''
        self._api_request('monitoring/converged-status')
        return self

    @is_connected
    def pin_status(self):
        '''
        <SimState>257</SimState>
        <PinOptState>258</PinOptState>
        <SimPinTimes>3</SimPinTimes>
        <SimPukTimes>10</SimPukTimes>
        '''
        self._api_request('pin/status')
        return self

    @is_connected
    def sim_lock(self):
        '''
        <SimLockEnable>0</SimLockEnable>
        <SimLockRemainTimes>100</SimLockRemainTimes>
        <pSimLockEnable></pSimLockEnable>
        <pSimLockRemainTimes></pSimLockRemainTimes>
        '''
        self._api_request('pin/simlock')
        return self

    @is_connected
    def monitoring_status(self):
        '''
        <ConnectionStatus>901</ConnectionStatus>
        <WifiConnectionStatus></WifiConnectionStatus>
        <SignalStrength></SignalStrength>
        <SignalIcon>5</SignalIcon>
        <CurrentNetworkType>9</CurrentNetworkType>
        <CurrentServiceDomain>3</CurrentServiceDomain>
        <RoamingStatus>0</RoamingStatus>
        <BatteryStatus></BatteryStatus>
        <BatteryLevel></BatteryLevel>
        <BatteryPercent></BatteryPercent>
        <simlockStatus>0</simlockStatus>
        <WanIPAddress>10.115.89.118</WanIPAddress>
        <WanIPv6Address></WanIPv6Address>
        <PrimaryDns>192.168.104.3</PrimaryDns>
        <SecondaryDns>192.168.104.4</SecondaryDns>
        <PrimaryIPv6Dns></PrimaryIPv6Dns>
        <SecondaryIPv6Dns></SecondaryIPv6Dns>
        <CurrentWifiUser></CurrentWifiUser>
        <TotalWifiUser></TotalWifiUser>
        <currenttotalwifiuser>0</currenttotalwifiuser>
        <ServiceStatus>2</ServiceStatus>
        <SimStatus>1</SimStatus>
        <WifiStatus></WifiStatus>
        <CurrentNetworkTypeEx>46</CurrentNetworkTypeEx>
        <maxsignal>5</maxsignal>
        <wifiindooronly>-1</wifiindooronly>
        <wififrequence>0</wififrequence>
        <classify>hilink</classify>
        <flymode>0</flymode>
        <cellroam>0</cellroam>
        <ltecastatus>0</ltecastatus>
        '''
        self._api_request('monitoring/status')
        self.TextConnectionStatus = self._get_connection_status(
                                         self.data['ConnectionStatus'])
        self.data['TextConnectionStatus'] = self.TextConnectionStatus
        self.TextCurrentNetworkType = self._get_network_type(
                                           self.data['CurrentNetworkType'])
        self.data['TextCurrentNetworkType'] = self.TextCurrentNetworkType
        self.TextRoamingStatus = self._get_roaming_status(
                                      self.data['RoamingStatus'])
        self.data['TextRoamingStatus'] = self.TextRoamingStatus
        return self

    @is_connected
    def check_notifications(self):
        '''
        <UnreadMessage>0</UnreadMessage>
        <SmsStorageFull>0</SmsStorageFull>
        <OnlineUpdateStatus>10</OnlineUpdateStatus>
        '''
        self._api_request('monitoring/check-notifications')
        return self

    @is_connected
    def traffic_statistics(self):
        '''
        <CurrentConnectTime>120</CurrentConnectTime>
        <CurrentUpload>549080</CurrentUpload>
        <CurrentDownload>11407740</CurrentDownload>
        <CurrentDownloadRate>368020</CurrentDownloadRate>
        <CurrentUploadRate>10036</CurrentUploadRate>
        <TotalUpload>554013</TotalUpload>
        <TotalDownload>11429698</TotalDownload>
        <TotalConnectTime>3348</TotalConnectTime>
        <showtraffic>1</showtraffic>
        '''
        self._api_request('monitoring/traffic-statistics')
        return self

    @is_connected
    def device_information(self):
        '''
        <DeviceName>E3372</DeviceName>
        <SerialNumber>G4PDW16623003677</SerialNumber>
        <Imei>861821032479591</Imei>
        <Imsi>401015625704899</Imsi>
        <Iccid>8999701560257048991F</Iccid>
        <Msisdn></Msisdn>
        <HardwareVersion>CL2E3372HM</HardwareVersion>
        <SoftwareVersion>22.317.01.00.00</SoftwareVersion>
        <WebUIVersion>17.100.14.02.577</WebUIVersion>
        <MacAddress1>BA:AB:BE:34:00:00</MacAddress1>
        <MacAddress2></MacAddress2>
        <ProductFamily>LTE</ProductFamily>
        <Classify>hilink</Classify>
        <supportmode>LTE|WCDMA|GSM</supportmode>
        <workmode>WCDMA</workmode>
        '''
        self._api_request('device/information')
        return self

    @is_connected
    def current_plmn(self):
        '''
        <State>0</State>
        <FullName>Beeline KZ</FullName>
        <ShortName>Beeline KZ</ShortName>
        <Numeric>40101</Numeric>
        <Rat>2</Rat>
        '''
        self._api_request('net/current-plmn')
        return self

    @is_connected
    def plmn_list(self):
        '''
        <State>0</State>
        <FullName>Beeline KZ</FullName>
        <ShortName>Beeline KZ</ShortName>
        <Numeric>40101</Numeric>
        <Rat>2</Rat>
        '''
        self._api_request('net/plmn-list')
        return self

    @is_connected
    def device_signal(self):
        '''
        <pci></pci>
        <sc></sc>
        <cell_id></cell_id>
        <rsrq></rsrq>
        <rsrp></rsrp>
        <rssi></rssi>
        <sinr></sinr>
        <rscp></rscp>
        <ecio></ecio>
        <psatt>1</psatt>
        <mode>2</mode>
        <lte_bandwidth></lte_bandwidth>
        <lte_bandinfo></lte_bandinfo>
        '''
        self._api_request('device/signal')
        return self

    @is_connected
    def net_mode(self, set=None):
        '''
        <NetworkMode>01</NetworkMode>
        <NetworkBand>3FFFFFFF</NetworkBand>
        <LTEBand>7FFFFFFFFFFFFFFF</LTEBand>
        '''
        if set is None:
            self._api_request('net/net-mode')
            return self

        self._api_post('net/net-mode', set)
        return self

    @is_connected
    def net_mode_list(self, set=None):
        '''
        <AccessList>
        <Access>00</Access>
        <Access>01</Access>
        <Access>02</Access>
        <Access>03</Access>
        </AccessList>
        <BandList>
        <Band>
        <Name>GSM900&#x2F;GSM1800&#x2F;WCDMA BCVIII&#x2F;WCDMA BCI</Name>
        <Value>2000000400380</Value>
        </Band>
        </BandList>
        <LTEBandList>
        <LTEBand>
        <Name>LTE BC1&#x2F;LTE BC3&#x2F;LTE BC7&#x2F;
              LTE BC8&#x2F;LTE BC20</Name>
        <Value>800c5</Value>
        </LTEBand>
        <LTEBand>
        <Name>All bands</Name>
        <Value>7ffffffffffffff</Value>
        </LTEBand>
        </LTEBandList>
        '''
        if set is None:
            self._api_request('net/net-mode-list')
            return self

        self._api_post('net/net-mode-list', set)
        return self

    @is_connected
    def dialup_connection(self, set=None):
        '''
        <RoamAutoConnectEnable>0</RoamAutoConnectEnable>
        <MaxIdelTime>600</MaxIdelTime>
        <ConnectMode>0</ConnectMode>
        <MTU>1500</MTU>
        <auto_dial_switch>1</auto_dial_switch>
        <pdp_always_on>0</pdp_always_on>
        '''
        if set is None:
            self._api_request('dialup/connection')
            return self

        self._api_post('dialup/connection', set)
        return self


def main():
    c = Client()
    if c.is_hilink():
        # print c.basic_info().productfamily
        # print c.net_mode().NetworkMode
        #print c.plmn_list().data
        print (c.current_plmn().data)
        print (c.monitoring_status().data)
        # pass
        # print c.module_switch().ussd_enabled
        # dialup_connection = c.dialup_connection()
        # print dialup_connection.ConnectMode
        # print dialup_connection.data
        # d = dialup_connection.data
        # d['ConnectMode'] = 0
        # d['MaxIdelTime'] = 1200
        # print d
        # c.dialup_connection(set=d)

if __name__ == "__main__":
    main()