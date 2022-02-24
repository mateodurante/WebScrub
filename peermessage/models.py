from django.db import models
from netblock.models import Netblock
import datetime
import json
import base64

class ConvertingDateTimeField(models.DateTimeField):

    def get_prep_value(self, value):
        if type(value) == float:
            return datetime.datetime.utcfromtimestamp(value)
        return value

class PeerMessage(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    time = ConvertingDateTimeField()
    counter = models.IntegerField()
    type = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    neighbor_address_local = models.CharField(max_length=255)
    neighbor_address_peer = models.CharField(max_length=255)
    neighbor_asn_local = models.CharField(max_length=255)
    neighbor_asn_peer = models.CharField(max_length=255)
    neighbor_direction = models.CharField(max_length=255)
    neighbor_state = models.CharField(max_length=255)
    related_asn = models.CharField(max_length=255)
    related_network = models.CharField(max_length=255)
    raw = models.TextField()


    def getLastState(address_peer):
        return PeerMessage.objects.filter(neighbor_address_peer=address_peer, type='state').order_by('-time')[0]


class PeerStatus(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    time = ConvertingDateTimeField()
    cmd = models.CharField(max_length=255)
    result_stdout = models.TextField()
    result_stderr = models.TextField()
    result_returncode = models.IntegerField()

    def getStdoutDecoded(self):
        return base64.b64decode(self.result_stdout).decode('utf-8')

    def getStderrDecoded(self):
        return base64.b64decode(self.result_stderr).decode('utf-8')

    def getLastStatus(address_peer, cmd):
        r = PeerStatus.objects.filter(address=address_peer, cmd=cmd).order_by('-time')
        return r[0] if len(r) > 0 else None

    def getCmds():
        return [v['cmd'] for v in PeerStatus.objects.values('cmd').distinct()]

    def getNodes():
        return [v['address'] for v in PeerStatus.objects.values('address').distinct()]

    def getAllStatus():
        # Esto se puede mejorar si no fuera sqlite3
        status = {}
        cmds = PeerStatus.getCmds()
        nodes = PeerStatus.getNodes()
        for node in nodes:
            for cmd in cmds:
                ps = PeerStatus.getLastStatus(node, cmd)
                if not node in status:
                    status[node] = {}
                status[node][cmd] = ps
        return status
    
    def getIPTables():
        """
        Chain INPUT (policy ACCEPT 8 packets, 684 bytes)
        pkts bytes target     prot opt in     out     source               destination         

        Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
        pkts bytes target     prot opt in     out     source               destination         
            0     0 DROP       tcp  --  *      *       0.0.0.0/0            182.23.0.10          multiport dports 80 /* Received from:  163.20.252.2 -I FORWARD -p tcp -s 0.0.0.0/0 -d 182.23.0.10/32 -m multiport --dport 80 */

        Chain OUTPUT (policy ACCEPT 10 packets, 635 bytes)
        pkts bytes target     prot opt in     out     source               destination         
        """
        tables = {}
        for node in PeerStatus.getNodes():
            ps = PeerStatus.getLastStatus(node, 'iptables -nvxL')
            if ps:
                tables[node] = {
                    'tables': PeerStatus._parseIPTables(ps.getStdoutDecoded()),
                    'raw': ps.result_stdout,
                    'time': ps.time,
                    'hostname': ps.hostname,
                }
        return tables

    def _parseIPTables(table):
        data = {}
        chain_lines = []
        chain_name = ''
        for line in table.split('\n'):
            if line.startswith('Chain'):
                if chain_lines:
                    data[chain_name] = PeerStatus._parseChain(chain_lines)
                chain_lines = [line]
                chain_name = line.split()[1]
            else:
                chain_lines.append(line)
        if chain_lines:
            data[chain_name] = PeerStatus._parseChain(chain_lines)
        return data

    def _parseChain(chain):
        data = []
        headers = chain[1].split() + ['extra', 'comments']
        for line in chain[2:]:
            if line:
                l = line.split()
                out = ' '.join(l[len(headers)-2:]).strip('*/').split('/*')
                if len(out) > 1:
                    extra = out[0]
                    comments = out[1]
                else:
                    extra = ''
                    comments = out[0]
                rl = l[:len(headers)-2] + [extra, comments]
                pline = dict(zip(headers, rl))
                if 'destination' in pline:
                    net = Netblock.findByIP(pline['destination'])
                    if net:
                        pline['asn'] = net.asn.asn
                data.append(pline)
        return data


class PeerIfaceStatus(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    time = ConvertingDateTimeField()
    name = models.CharField(max_length=255)
    data = models.TextField()

    def getLastStatus(address_peer, iface_name):
        r = PeerIfaceStatus.objects.filter(address=address_peer, name=iface_name).order_by('-time')
        return r[0] if len(r) > 0 else None

    def getLastStatusValues(address_peer, iface_name):
        r = PeerIfaceStatus.objects.filter(address=address_peer, name=iface_name).order_by('-time').values()
        if len(r) <= 0:
            return {}
        try:
            r[0]['time'] = r[0]['time'].strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        try:
            r[0]['data'] = json.loads(r[0]['data'])
        except:
            pass
        return r[0]

    def getIfaces():
        return [v['name'] for v in PeerIfaceStatus.objects.values('name').distinct()]

    def getNodes():
        return [v['address'] for v in PeerIfaceStatus.objects.values('address').distinct()]

    def getAllStatus():
        # Esto se puede mejorar si no fuera sqlite3
        status = {}
        ifaces = PeerIfaceStatus.getIfaces()
        nodes = PeerIfaceStatus.getNodes()
        for node in nodes:
            for name in ifaces:
                pis = PeerIfaceStatus.getLastStatus(node, name)
                if pis:
                    if not node in status:
                        status[node] = {}
                    status[node][name] = pis
        return status

    def getAllStatusValues():
        # Esto se puede mejorar si no fuera sqlite3
        status = {}
        ifaces = PeerIfaceStatus.getIfaces()
        nodes = PeerIfaceStatus.getNodes()
        for node in nodes:
            for name in ifaces:
                pis = PeerIfaceStatus.getLastStatusValues(node, name)
                if pis:
                    if not node in status:
                        status[node] = {}
                    status[node][name] = pis
        return status
