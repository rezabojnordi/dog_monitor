
import requests
from . import config

class DogMonitor():
    def __init__(self,instance_id=None,compute=None,start_date=None,start_time=None,end_date=None,end_time=None,metrics=[]):
        self.instance_id = instance_id
        self.compute = compute
        self.metrics = metrics
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        
    def request_metrics(self):
        
        #response=requests.get(config.PROMETHEUS + '/api/v1/query', params={'query': 'libvirt_domain_state_code and changes(libvirt_domain_state_code[10m]) > 0'})
        #total_cpu = "libvirt_domain_info_virtual_cpus{host=~"$compute", job=~"prometheus-libvirt-exporter"}"
        total_cpu = 'libvirt_domain_info_virtual_cpus{domain="%s"}'%(self.instance_id)
        cpu_usage = 'avg by (domain) (irate(libvirt_domain_info_cpu_time_seconds_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])) * 100'%(self.instance_id)
        total_mem = 'libvirt_domain_info_maximum_memory_bytes{domain="%s",job=~"prometheus-libvirt-exporter"}'%(self.instance_id)
        available_mem = 'libvirt_domain_stat_memory_unused_bytes{domain="%s", job=~"prometheus-libvirt-exporter"}'%(self.instance_id)
        mem_usage = 'libvirt_domain_info_maximum_memory_bytes{domain="%s", job=~"prometheus-libvirt-exporter"} - libvirt_domain_stat_memory_unused_bytes{domain="%s", job=~"prometheus-libvirt-exporter"}'%(self.instance_id,self.instance_id)
        iops_read_disk = 'rate(libvirt_domain_block_stats_read_requests_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        iops_write_disk = 'rate(libvirt_domain_block_stats_write_requests_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        troughput_read_disk = 'rate(libvirt_domain_block_stats_read_bytes_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        troughput_write_disk = 'rate(libvirt_domain_block_stats_write_bytes_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rtx_troughput = 'rate(libvirt_domain_interface_stats_receive_bytes_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_troughput = 'rate(libvirt_domain_interface_stats_transmit_bytes_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packets = 'rate(libvirt_domain_interface_stats_receive_packets_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet = 'rate(libvirt_domain_interface_stats_transmit_packets_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packet_error = 'rate(libvirt_domain_interface_stats_receive_errors_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet_error = 'rate(libvirt_domain_interface_stats_transmit_errors_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        rx_packet_drop = 'rate(libvirt_domain_interface_stats_receive_drops_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        tx_packet_drop = 'rate(libvirt_domain_interface_stats_transmit_drops_total{domain="%s", job=~"prometheus-libvirt-exporter"}[30s])'%(self.instance_id)
        querys = [total_cpu,cpu_usage,total_mem,available_mem,mem_usage,iops_read_disk,iops_write_disk,troughput_read_disk,troughput_write_disk,rtx_troughput
        ,tx_troughput,rx_packets,tx_packet,rx_packet_error,tx_packet_error,rx_packet_drop,tx_packet_drop]


        self.metrics=[]
        for i in querys:
#            print(config.PROMETHEUS + '/api/v1/query_range'+ '?start=' + self.start_date + 'T' + self.start_time + '.000Z&end=' + self.end_date + 'T' + self.end_time + '.000Z&step=60s&query=' + i )
            response=requests.get(config.PROMETHEUS + '/api/v1/query_range'+ '?start=' + self.start_date + 'T' + self.start_time + '.000Z&end=' + self.end_date + 'T' + self.end_time + '.000Z&step=60s&query='+ i)
            self.metrics.append(response.json()['data']['result'])
        
        # tresults = response.json()['data']['result']
 #       print("sss",self.metrics)
        return {
            "total_cpu":self.metrics[0],
            "cpu_usage":self.metrics[1],
            "total_mem":self.metrics[2],
            "available_mem":self.metrics[3],
            "mem_usage":self.metrics[4],
            "iops_read_disk":self.metrics[5],
            "iops_write_disk":self.metrics[6],
            "troughput_read_disk":self.metrics[7],
            "troughput_write_disk":self.metrics[8],
            "rtx_troughput":self.metrics[9],
            "tx_troughput":self.metrics[10],
            "rx_packets":self.metrics[11],
            "tx_packet":self.metrics[12],
            "rx_packet_error":self.metrics[13],
            "tx_packet_error":self.metrics[14],
            "rx_packet_drop":self.metrics[15],
            "tx_packet_drop":self.metrics[16],
        }

    def save_to_redis(self):
        pass






def preprocess():
    pass

