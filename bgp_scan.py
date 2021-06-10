import argparse
import db
import telnetlib
import re

from models import BGP
from utils import encode2ascii, decode2ascii, tokenizer


HOST = 'route-server.he.net'

_pattern = '(\d+.+) \| ((?:\d{1,3}\.){3}\d{1,3}) from ((?:\d{1,3}\.){3}\d{1,3}) '\
           '\(((?:\d{1,3}\.){3}\d{1,3})\) \| origin (\w{1,}), metric (\d+), localpref (\d+),'\
           ' (\w+), (\w+),? ?(\w+)? \| (originator: ((?:\d{1,3}\.){3}\d{1,3}), cluster list: '\
           '((?:\d{1,3}\.){3}\d{1,3}.+)+ \| )?last update: (\w{3} \w{3}  \d{1,2} \d{2}:\d{2}:\d{2} \d{4})'

_character_empty = ''
_character_new_line = '\n'
_characters_separator = '\n\r\n'
_characters_eof = 'route-server> '

_command_exec = 'show bgp ipv4 unicast '
_command_exit = 'exit'


def get_bgp(ip):
    bgps = []
    try:
        print('Connecting...')
        
        tn = telnetlib.Telnet(HOST)
        tn.read_until(encode2ascii(_characters_eof))
        
        print('Fetching....')
        tn.write(encode2ascii(_command_exec + ip + _character_new_line))
        tn.read_until(encode2ascii(_command_exec))
        
        response = tn.read_until(encode2ascii(_characters_eof))

        tn.write(encode2ascii(_command_exit + _character_new_line))
        
        print('Parsing....')
        
        response = decode2ascii(response)
        response = response.replace(_characters_separator + _characters_eof, _character_empty)
        response = response.split('\n\r\n')
        
        header = tokenizer(response[0])
        header = header.split(' | ')

        _network = header[0].strip().split(' ')[-1]
        del header[0] # remove network info
        del header[0] # remove path summary

        if 'Not advertised' in header[0]:
            del header[0] # remove message

        response[0] = '\r\n    '.join(header) # reverse
        for data in response[1:]:
            raw = tokenizer(data)
            try:
                match = re.match(_pattern, raw.lower())

                network = _network
                next_hop = match.group(2)
                origin = match.group(5)
                metric = match.group(6)
                locprof = match.group(7)
                path = match.group(1)
                last_update = match.group(14)
                cluster_list = ''

                try:
                    cluster_list = match.group(13)
                except: pass

                bgp = BGP(ip, network, next_hop, metric, locprof, path, cluster_list,
                          origin, last_update)
                bgps.append(bgp)
            except: pass
    except Exception as e: print(e)

    return bgps


def persist_bgp(bgps):
    if bgps:
        db.Base.metadata.create_all(db.engine)
        for bgp in bgps:
            db.session.add(bgp)
            db.session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BGP details by HERouter')
    parser.add_argument('--ip', help='single ip', required=True)
    
    args = parser.parse_args()

    print('----- Running BGP Scan -----')
    print('--- Written by Julio Realpe ---')

    if args.ip:
        bgp_list = get_bgp(args.ip)
        persist_bgp(bgp_list)

    print('Terminated Successfully!')
